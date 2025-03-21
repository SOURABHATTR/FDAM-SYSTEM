from flask import Blueprint, request, jsonify, make_response
import bcrypt
import jwt
import datetime
from database import sqlite_conn, sqlite_cursor

auth_blueprint = Blueprint("auth", __name__)
SECRET_KEY = "your_secret_key_here"

# ✅ Force CORS Headers
@auth_blueprint.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# ✅ Register User (Fixed Hashing)
@auth_blueprint.route("/register", methods=["POST", "OPTIONS"])
def register_user():
    if request.method == "OPTIONS":
        return make_response("", 200)

    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")  

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if user exists
        sqlite_cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if sqlite_cursor.fetchone():
            return jsonify({"error": "User already exists"}), 409

        # ✅ Ensure password is stored correctly as a byte string
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Insert user into DB with default balance
        sqlite_cursor.execute(
            "INSERT INTO users (username, password, role, balance, last_login) VALUES (?, ?, ?, ?, ?)",
            (username, hashed_pw, role, 1000, None),
        )
        sqlite_conn.commit()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"❌ Registration Error: {e}")
        return jsonify({"error": str(e)}), 500

# ✅ Login User (Fixed Hash Check)
@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Fetch user from DB
        sqlite_cursor.execute("SELECT id, username, password, role, balance FROM users WHERE username = ?", (username,))
        user = sqlite_cursor.fetchone()

        if not user:
            print(f"❌ DEBUG: User '{username}' not found")
            return jsonify({"error": "Invalid credentials (User not found)"}), 401

        user_id, username, stored_hashed_pw, role, balance = user

        print(f"🔍 DEBUG: Stored Hashed Password -> {stored_hashed_pw}")
        print(f"🔍 DEBUG: Entered Password -> {password}")

        # ✅ Check password properly
        if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_pw.encode("utf-8")):
            print("✅ DEBUG: Password matched successfully!")

            # ✅ Store last login timestamp
            login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlite_cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (login_time, user_id))
            sqlite_conn.commit()

            # ✅ Generate JWT Token
            token = jwt.encode(
                {
                    "user_id": user_id,
                    "username": username,
                    "role": role,
                    "balance": balance,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                SECRET_KEY, algorithm="HS256"
            )

            return jsonify({"message": "Login successful", "token": token, "user": {"username": username, "balance": balance}}), 200
        else:
            print("❌ DEBUG: Password mismatch detected")
            return jsonify({"error": "Invalid credentials (Wrong password)"}), 401
    except Exception as e:
        print(f"❌ Login Error: {e}")
        return jsonify({"error": str(e)}), 500



# ✅ Protected Route (User Dashboard - Only Accessible After Login)
@auth_blueprint.route("/dashboard", methods=["GET"])
def user_dashboard():
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            username = decoded_token["username"]
            role = decoded_token["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # Fetch user details from DB
        sqlite_cursor.execute("SELECT username, role, balance, last_login FROM users WHERE id = ?", (user_id,))
        user = sqlite_cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        username, role, balance, last_login = user

        return jsonify({
            "message": "Welcome to the dashboard!",
            "user": {
                "username": username,
                "role": role,
                "balance": balance,
                "last_login": last_login
            }
        }), 200
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")
        return jsonify({"error": str(e)}), 500
