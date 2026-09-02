"""Unicorn Adoption Bureau.

Kept exactly as a coding assistant produced it. Do not tidy this file.
Every example in the code quality part of L2 is read off it.
"""

import smtplib
import sqlite3
from email.message import EmailMessage


class UnicornPolicyConfig:
    def __init__(self, min_garden=50, min_glitter=6, min_hours=20, max_floor=2):
        self.min_garden = min_garden
        self.min_glitter = min_glitter
        self.min_hours = min_hours
        self.max_floor = max_floor


def decide(
    garden_m2,
    glitter_tolerance,
    hours_at_home,
    floor,
    age_group,
    applicant_email,
    db_path="applications.db",
):
    """Decide whether a unicorn adoption application is approved."""
    config = UnicornPolicyConfig()

    if garden_m2 is None:
        garden_m2 = 0
    if glitter_tolerance is None:
        glitter_tolerance = 10
    if hours_at_home is None:
        hours_at_home = 0

    score = 0
    reasons = []

    if age_group == "foal":
        if garden_m2 > config.min_garden:
            score += 40
        else:
            reasons.append("Garden too small.")
        if glitter_tolerance >= config.min_glitter:
            score += 30
        else:
            reasons.append("Glitter tolerance too low.")
        if hours_at_home >= config.min_hours:
            score += 30
        else:
            reasons.append("Not enough hours at home.")
    elif age_group == "adult":
        if garden_m2 > config.min_garden:
            score += 40
        else:
            reasons.append("Garden too small.")
        if glitter_tolerance >= config.min_glitter:
            score += 30
        else:
            reasons.append("Glitter tolerance too low.")
        if hours_at_home >= config.min_hours:
            score += 30
        else:
            reasons.append("Not enough hours at home.")
    elif age_group == "elder":
        if garden_m2 > config.min_garden:
            score += 40
        else:
            reasons.append("Garden too small.")
        if glitter_tolerance >= config.min_glitter:
            score += 30
        else:
            reasons.append("Glitter tolerance too low.")
        if hours_at_home >= config.min_hours:
            score += 30
        else:
            reasons.append("Not enough hours at home.")

    if floor > config.max_floor:
        reasons.append("Too high without a lift.")

    approved = score >= 70

    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO decisions (email, score, approved) VALUES (?, ?, ?)",
        (applicant_email, score, approved),
    )
    conn.commit()
    conn.close()

    msg = EmailMessage()
    msg["To"] = applicant_email
    msg["Subject"] = "Your unicorn adoption application"
    msg.set_content("Approved!" if approved else "Refused: " + " ".join(reasons))
    with smtplib.SMTP("localhost") as server:
        server.send_message(msg)

    html = "<h1>Approved</h1>" if approved else "<h1>Refused</h1><p>" + " ".join(reasons) + "</p>"
    return html
