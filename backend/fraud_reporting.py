from flask import Blueprint, request, jsonify
import database

report_blueprint = Blueprint("report", __name__)

@report_blueprint.route("/report", methods=["POST"])
def report_fraud():
    data = request.json
    transaction_id = data.get("transaction_id")
    reporting_entity = data.get("reporting_entity_id")
    fraud_details = data.get("fraud_details")

    if not transaction_id or not fraud_details:
        return jsonify({"error": "Missing transaction_id or fraud_details"}), 400

    # Check if transaction exists in the fraud detection database
    transaction = database.transactions_collection.find_one({"transaction_id": transaction_id})
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    # Store the fraud report in the fraud_reports collection
    fraud_report = {
        "transaction_id": transaction_id,
        "reporting_entity": reporting_entity,
        "fraud_details": fraud_details,
        "is_fraud_reported": True
    }
    database.fraud_reports_collection.insert_one(fraud_report)

    # Update the fraud detection database to mark this transaction as reported
    database.transactions_collection.update_one(
        {"transaction_id": transaction_id},
        {"$set": {"is_fraud_reported": True}}
    )

    return jsonify({"transaction_id": transaction_id, "reporting_acknowledged": True}), 200
