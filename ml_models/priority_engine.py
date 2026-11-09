
import re


def _safe_integer(value, default=0):
    """Convert a value to a non-negative integer safely."""
    try:
        number = int(value)
        return max(0, number)
    except (TypeError, ValueError):
        return default


def _split_sentences(description):
    """Split a report into simple sentence-like units."""
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?;])\s+", description)
        if sentence.strip()
    ]


def _is_negated(sentence, match_start):
    """
    Check whether a danger indicator is preceded by a nearby
    negation. This is a simple rule, not full language understanding.
    """
    preceding_text = sentence[:match_start]

    return bool(
        re.search(
            r"\b(?:no|not|never|without|neither)\b"
            r"(?:\W+\w+){0,3}\W*$",
            preceding_text,
        )
    )


def _contains_current_danger(description, keywords):
    """Find at least one non-negated danger indicator."""
    for sentence in _split_sentences(description):
        for keyword in keywords:
            pattern = re.compile(
                r"(?<!\w)" + re.escape(keyword) + r"(?!\w)",
                re.IGNORECASE,
            )

            for match in pattern.finditer(sentence):
                if not _is_negated(sentence, match.start()):
                    return True

    return False


def assess_priority(incident):
    """
    Calculate an explainable, rule-based priority recommendation.

    This is advisory only. It does not change the coordinator's
    operational priority and is not a validated triage system.
    """

    description = str(
        getattr(incident, "description", "") or ""
    ).lower()

    incident_type = str(
        getattr(incident, "incident_type", "OTHER") or "OTHER"
    ).upper()

    severity = _safe_integer(
        getattr(incident, "severity", 0)
    )
    severity = min(severity, 5)

    affected = _safe_integer(
        getattr(incident, "people_affected", 0)
    )

    score = 0
    reasons = []

    # 1. Reported severity: 0–40 points
    severity_points = severity * 8
    score += severity_points

    reasons.append(
        f"Reported severity {severity}/5: "
        f"+{severity_points} points"
    )

    # 2. Number of people affected: 0–25 points
    if affected > 100:
        affected_points = 25
    elif affected > 50:
        affected_points = 20
    elif affected > 20:
        affected_points = 15
    elif affected > 5:
        affected_points = 10
    elif affected > 0:
        affected_points = 5
    else:
        affected_points = 0

    score += affected_points

    reasons.append(
        f"{affected} people reported affected: "
        f"+{affected_points} points"
    )

    # 3. Danger indicators
    danger_groups = {
        "Life-threatening medical condition": (
            "unconscious",
            "not breathing",
            "no pulse",
            "severe bleeding",
            "life-threatening",
        ),
        "People trapped or unable to escape": (
            "trapped",
            "stuck inside",
            "unable to escape",
            "buried",
        ),
        "Major immediate hazard": (
            "explosion",
            "gas leak",
            "building collapse",
            "collapsed building",
            "building has collapsed",
            "building collapsed",
            "structure has collapsed",
            "structure collapsed",
            "spreading fire",
            "fire spreading",
            "chemical spill",
        ),
        "Rapidly developing danger": (
            "water rising",
            "rapidly rising",
            "swept away",
            "structural instability",
        ),
        "Reported injuries or casualties": (
            "injured",
            "injuries",
            "wounded",
            "casualties",
        ),
    }

    danger_points = {
        "Life-threatening medical condition": 12,
        "People trapped or unable to escape": 12,
        "Major immediate hazard": 10,
        "Rapidly developing danger": 8,
        "Reported injuries or casualties": 5,
    }

    detected_dangers = []

    for danger, keywords in danger_groups.items():
        if _contains_current_danger(description, keywords):
            points = danger_points[danger]
            score += points
            detected_dangers.append(danger)

            reasons.append(
                f"{danger}: +{points} points"
            )

    # 4. Incident category adjustment
    high_risk_types = {
        "FIRE",
        "FLOOD",
        "EARTHQUAKE",
        "BUILDING_COLLAPSE",
        "LANDSLIDE",
    }

    category_points = (
        5 if incident_type in high_risk_types else 0
    )

    score += category_points

    if category_points:
        reasons.append(
            f"High-risk incident category ({incident_type}): "
            f"+{category_points} points"
        )

    # 5. Keep score within 0–100
    score = min(score, 100)

    # 6. Determine advisory priority
    if score >= 75:
        priority = "CRITICAL"
    elif score >= 55:
        priority = "HIGH"
    elif score >= 30:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    explanation = (
        f"Recommended priority: {priority}. "
        f"Assessment score: {score}/100.\n\n"
        "Assessment factors:\n"
        + "\n".join(f"- {reason}" for reason in reasons)
        + "\n\nThis is an experimental, advisory rule-based "
          "assessment. It may miss context or misinterpret "
          "reported information. A human coordinator must "
          "verify the report and confirm operational priority."
    )

    return {
        "priority": priority,
        "score": score,
        "explanation": explanation,
        "detected_dangers": detected_dangers,
    }
