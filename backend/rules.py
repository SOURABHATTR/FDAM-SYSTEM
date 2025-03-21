# rules.py - Rule-Based Fraud Detection System

# ✅ Define Static Rules for Fraud Detection
FRAUD_RULES = {
    "high_transaction_limit": 10000,  # Transactions above this amount are flagged
    "high_frequency": 5,  # More than 5 transactions in a short period
    "blacklisted_users": [999, 888],  # List of known fraudsters (user IDs)
    "suspicious_countries": ["North Korea", "Iran"],  # Blocked countries
}

def check_transaction_rules(transaction):
    """
    Apply rule-based fraud detection.
    Returns: True if transaction is fraudulent, False otherwise.
    """

    # ✅ 1. Rule: Large Transactions
    if transaction["transaction_amount"] > FRAUD_RULES["high_transaction_limit"]:
        return True  # Fraud detected

    # ✅ 2. Rule: Blacklisted Users
    if transaction["sender_id"] in FRAUD_RULES["blacklisted_users"]:
        return True  # Fraud detected

    # ✅ 3. Rule: Suspicious Country Transactions
    if transaction.get("country") in FRAUD_RULES["suspicious_countries"]:
        return True  # Fraud detected

    return False  # Transaction passed the rules
