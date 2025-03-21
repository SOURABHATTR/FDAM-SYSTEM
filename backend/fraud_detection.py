from flask import Blueprint, request, jsonify
import pickle
import numpy as np
from rules import check_transaction_rules  # ✅ Import Rule-Based Detection
from database import sqlite_cursor, sqlite_conn

fraud_blueprint = Blueprint("fraud", __name__)

# ✅ Load Pre-trained ML Model
model = pickle.load(open("fraud_model.pkl", "rb"))

def check_fraud(sender_id, receiver_id, amount, transaction_type="transfer"):
    """
    Function to check if a transaction is fraudulent.
    - Uses rule-based detection first.
    - Uses ML model if rules are not triggered.
    """
    transaction_data = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "transaction_amount": amount,
        "transaction_type": transaction_type
    }

    # ✅ Step 1: Apply Rule-Based Fraud Detection
    if check_transaction_rules(transaction_data):
        return True  # Rule-based fraud detected

    # ✅ Step 2: Use ML Model to Predict Fraud
    features = np.array([[amount, 1 if transaction_type == "transfer" else 0]])  # Convert transaction type to numeric
    prediction = model.predict(features)

    return bool(prediction[0])  # Return True if fraud detected, False otherwise

@fraud_blueprint.route("/predict", methods=["POST"])
def predict_fraud():
    """
    API Route to Predict if a Transaction is Fraudulent.
    """
    try:
        data = request.json
        is_fraud = check_fraud(data["sender_id"], data["receiver_id"], data["transaction_amount"], data["transaction_type"])

        # ✅ Step 3: Store transaction in the database
        sqlite_cursor.execute(
            "INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type, fraud_status) VALUES (?, ?, ?, ?, ?)",
            (data["sender_id"], data["receiver_id"], data["transaction_amount"], data["transaction_type"], "fraud" if is_fraud else "legit")
        )
        sqlite_conn.commit()

        return jsonify({"fraudulent": is_fraud, "reason": "Fraud detected" if is_fraud else "Transaction is Safe"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
