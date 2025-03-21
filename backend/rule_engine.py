def rule_based_detection(transaction):
    """
    Implements rule-based fraud detection.
    Returns True if fraud is detected, else False.
    """
    rules_triggered = []

    # Rule 1: Large transaction amount (above $10,000)
    if transaction["amount"] > 10000:
        rules_triggered.append("High transaction amount")

    # Rule 2: International transaction without user history
    if transaction["country"] != "US" and transaction["user_history"]["international_txns"] < 3:
        rules_triggered.append("Unusual international transaction")

    # Rule 3: Transaction happening at unusual hours (e.g., midnight)
    if transaction["timestamp"].hour < 5:
        rules_triggered.append("Transaction at unusual hours")

    # Return result
    is_fraud = len(rules_triggered) > 0
    return is_fraud, rules_triggered
