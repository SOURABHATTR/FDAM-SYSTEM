from flask import Flask
from flask_cors import CORS
from auth import auth_blueprint
from transactions import transactions_blueprint
from fraud_detection import fraud_blueprint
from dashboard_api import dashboard_blueprint
from database import initialize_db

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Enable CORS for All Routes (TEMPORARY FIX)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now

# ✅ Initialize Database
initialize_db()

# ✅ Register Blueprints (APIs)
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(transactions_blueprint, url_prefix="/transactions")
app.register_blueprint(fraud_blueprint, url_prefix="/fraud")
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")

if __name__ == "__main__":
    print("🚀 FDAM System Backend Running on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
