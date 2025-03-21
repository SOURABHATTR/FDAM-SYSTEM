from flask import Blueprint, jsonify
from database import sqlite_cursor

dashboard_blueprint = Blueprint("dashboard", __name__)

# ✅ Get Fraud & Transaction Statistics
@dashboard_blueprint.route("/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    try:
        # ✅ Query total transactions
        sqlite_cursor.execute("SELECT COUNT(*) FROM transactions")
        total_transactions = sqlite_cursor.fetchone()[0]

        # ✅ Query total fraud cases
        sqlite_cursor.execute("SELECT COUNT(*) FROM transactions WHERE is_fraud = 1")
        total_fraud_cases = sqlite_cursor.fetchone()[0]

        # ✅ Query fraud percentage
        fraud_percentage = (total_fraud_cases / total_transactions) * 100 if total_transactions > 0 else 0

        return jsonify({
            "total_transactions": total_transactions,
            "total_fraud_cases": total_fraud_cases,
            "fraud_percentage": round(fraud_percentage, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
