
# ==========================================
# SIGNAL STACK AI
# Step 26: Signal Prioritization Engine
# ==========================================

def calculate_priority(signal):

    """
    Calculate the priority of an intelligence signal.
    """

    title = str(signal.get("title", "")).lower()
    content = str(signal.get("content", "")).lower()
    description = str(signal.get("description", "")).lower()

    text = f"{title} {content} {description}"

    relevance = int(signal.get("relevance_score", 0) or 0)

    priority_score = relevance

    # Urgency keywords
    critical_keywords = [
        "security breach",
        "data breach",
        "lawsuit",
        "bankruptcy",
        "major failure",
        "critical vulnerability",
        "regulatory action"
    ]

    high_keywords = [
        "acquisition",
        "funding",
        "partnership",
        "product launch",
        "expansion",
        "price change",
        "leadership change",
        "market disruption"
    ]

    medium_keywords = [
        "update",
        "announcement",
        "new feature",
        "research",
        "industry report",
        "customer feedback"
    ]

    # Priority scoring
    if any(keyword in text for keyword in critical_keywords):
        priority_score += 40

    elif any(keyword in text for keyword in high_keywords):
        priority_score += 25

    elif any(keyword in text for keyword in medium_keywords):
        priority_score += 10

    # Category weighting
    category = str(signal.get("category", "")).lower()

    if category == "competitors":
        priority_score += 10

    elif category == "customers":
        priority_score += 8

    elif category == "market":
        priority_score += 7

    elif category == "internal":
        priority_score += 5

    # Priority classification
    if priority_score >= 90:
        priority = "Critical"

    elif priority_score >= 70:
        priority = "High"

    elif priority_score >= 40:
        priority = "Medium"

    else:
        priority = "Low"

    return {
        "priority": priority,
        "priority_score": priority_score
    }


def prioritize_signal(signal):

    """
    Add priority information to a signal.
    """

    result = calculate_priority(signal)

    signal["priority"] = result["priority"]
    signal["priority_score"] = result["priority_score"]

    return signal


def prioritize_signals(signals):

    """
    Prioritize a collection of signals.
    """

    prioritized = [
        prioritize_signal(signal.copy())
        for signal in signals
    ]

    return sorted(
        prioritized,
        key=lambda x: x["priority_score"],
        reverse=True
    )
