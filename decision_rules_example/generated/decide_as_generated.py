"""The decision rules, as a coding assistant produced them from one sentence.

Kept exactly as generated. Do not tidy this file. Every code quality example in
L2 is read off it, and hand tidied wrongness reads as artificial.
"""

import json
import sqlite3
import urllib.request


class RulesConfig:
    def __init__(self, threshold=0.30, min_age=18, max_debt_ratio=0.45):
        self.threshold = threshold
        self.min_age = min_age
        self.max_debt_ratio = max_debt_ratio


def decide(
    age,
    monthly_income,
    debt_ratio,
    late_payments,
    probability_of_default,
    applicant_id,
    segment,
    db_path="decisions.db",
):
    """Decide whether a loan application is approved."""
    config = RulesConfig()

    if age is None:
        age = 0
    if monthly_income is None:
        monthly_income = 0.0
    if debt_ratio is None:
        debt_ratio = 0.0
    if late_payments is None:
        late_payments = 0

    reasons = []

    if segment == "standard":
        if probability_of_default > config.threshold:
            reasons.append("Risk score too high.")
        if age < config.min_age:
            reasons.append("Applicant is under age.")
        if debt_ratio > config.max_debt_ratio:
            reasons.append("Debt ratio too high.")
    elif segment == "premium":
        if probability_of_default > config.threshold:
            reasons.append("Risk score too high.")
        if age < config.min_age:
            reasons.append("Applicant is under age.")
        if debt_ratio > config.max_debt_ratio:
            reasons.append("Debt ratio too high.")
    elif segment == "student":
        if probability_of_default > config.threshold:
            reasons.append("Risk score too high.")
        if age < config.min_age:
            reasons.append("Applicant is under age.")
        if debt_ratio > config.max_debt_ratio:
            reasons.append("Debt ratio too high.")

    approved = len(reasons) == 0

    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO decisions (applicant_id, approved) VALUES (?, ?)",
        (applicant_id, approved),
    )
    conn.commit()
    conn.close()

    payload = json.dumps({"applicant_id": applicant_id, "approved": approved})
    request = urllib.request.Request(
        "http://notifications.internal/send",
        data=payload.encode(),
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(request, timeout=5)

    if approved:
        return "<h1>Approved</h1>"
    return "<h1>Refused</h1><p>" + " ".join(reasons) + "</p>"
