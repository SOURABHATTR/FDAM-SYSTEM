from flask import Blueprint, request, jsonify
from database import sqlite_conn, sqlite_cursor
import fraud_detection  # ✅ Correctly Import the Module

transactions_blueprint = Blueprint("transactions", __name__)

# ✅ API to Transfer Money (with Fraud Detection)
@transactions_blueprint.route("/transfer", methods=["POST"])
def transfer():
    try:
        data = request.json
        sender_username = data.get("sender")
        receiver_username = data.get("receiver")
        amount = float(data.get("amount"))

        # ✅ Fetch sender balance
        sqlite_cursor.execute("SELECT id, balance FROM users WHERE username = ?", (sender_username,))
        sender = sqlite_cursor.fetchone()
        if not sender or sender[1] < amount:
            return jsonify({"error": "Insufficient funds"}), 400

        # ✅ Fetch receiver
        sqlite_cursor.execute("SELECT id FROM users WHERE username = ?", (receiver_username,))
        receiver = sqlite_cursor.fetchone()
        if not receiver:
            return jsonify({"error": "Receiver does not exist"}), 404

        sender_id, sender_balance = sender
        receiver_id = receiver[0]

        # ✅ Pass through ML fraud detection
        is_fraud = fraud_detection.check_fraud(sender_id, receiver_id, amount)  # ✅ Use Correct Import
        fraud_status = "fraud" if is_fraud else "legit"

        if is_fraud:
            return jsonify({"error": "Transaction flagged as fraud"}), 403

        # ✅ Update balances
        sqlite_cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, sender_id))
        sqlite_cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, receiver_id))
        
        # ✅ Store transaction
        sqlite_cursor.execute(
            "INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type, fraud_status) VALUES (?, ?, ?, ?, ?)",
            (sender_id, receiver_id, amount, "transfer", fraud_status)
        )

        sqlite_conn.commit()
        return jsonify({"message": "Transaction successful!", "fraud_status": fraud_status}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API to Fetch All Transactions
@transactions_blueprint.route("/all", methods=["GET"])
def get_all_transactions():
    try:
        sqlite_cursor.execute("SELECT * FROM transactions")
        transactions = sqlite_cursor.fetchall()

        transactions_list = [
            {
                "id": row[0],
                "sender_id": row[1],
                "receiver_id": row[2],
                "amount": row[3],
                "transaction_type": row[4],
                "timestamp": row[5],
                "fraud_status": row[6]
            }
            for row in transactions
        ]

        return jsonify(transactions_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
