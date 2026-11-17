
# ==========================================
# SIGNAL STACK AI
# Step 35: Market Intelligence Analyzer
# ==========================================

from collections import Counter


MARKET_PATTERNS = {

    "Emerging Technology": [
        "artificial intelligence", "generative ai",
        "machine learning", "blockchain",
        "robotics", "quantum computing",
        "automation", "large language model"
    ],

    "Market Opportunity": [
        "market opportunity", "untapped market",
        "growing demand", "market gap",
        "new opportunity", "business opportunity",
        "increasing demand"
    ],

    "Market Growth": [
        "market growth", "revenue growth",
        "industry growth", "rapid growth",
        "market expansion", "growing industry"
    ],

    "Market Risk": [
        "market decline", "economic slowdown",
        "market uncertainty", "recession",
        "regulatory risk", "supply chain disruption"
    ],

    "Industry Innovation": [
        "innovation", "breakthrough",
        "new technology", "research breakthrough",
        "digital transformation", "disruptive technology"
    ],

    "Investment Activity": [
        "venture capital", "investment",
        "funding round", "investor interest",
        "capital investment"
    ],

    "Consumer Trends": [
        "consumer behavior", "customer demand",
        "consumer preference", "buying behavior",
        "shopping trends", "user adoption"
    ],

    "Regulatory Changes": [
        "new regulation", "government policy",
        "compliance requirement", "regulatory framework",
        "legal framework", "policy change"
    ]
}


def extract_market_text(signal):

    title = str(signal.get("title", ""))

    content = str(
        signal.get("content", signal.get("description", ""))
    )

    return f"{title} {content}".lower()


def detect_market_events(text):

    """
    Detect market-related developments.
    """

    text = str(text).lower()

    detected = []

    for event, keywords in MARKET_PATTERNS.items():

        if any(keyword in text for keyword in keywords):
            detected.append(event)

    return detected


def analyze_market_signal(signal):

    text = extract_market_text(signal)

    events = detect_market_events(text)

    opportunities = [
        event for event in events
        if event in [
            "Market Opportunity",
            "Market Growth",
            "Emerging Technology",
            "Industry Innovation"
        ]
    ]

    risks = [
        event for event in events
        if event in [
            "Market Risk",
            "Regulatory Changes"
        ]
    ]

    return {

        "title": signal.get("title", ""),

        "market_events": events,

        "opportunities": opportunities,

        "risks": risks,

        "priority": signal.get("priority", "Low"),

        "relevance_score": signal.get("relevance_score", 0),

        "source": signal.get("source", "Unknown")
    }


def analyze_market(signals):

    """
    Generate a comprehensive market intelligence report.
    """

    market_signals = []

    event_counter = Counter()
    opportunity_counter = Counter()
    risk_counter = Counter()

    for signal in signals:

        category = str(
            signal.get("category", "")
        ).lower()

        if category != "market":
            continue

        result = analyze_market_signal(signal)

        market_signals.append(result)

        event_counter.update(result["market_events"])

        opportunity_counter.update(result["opportunities"])

        risk_counter.update(result["risks"])

    return {

        "total_market_signals": len(market_signals),

        "event_distribution": dict(event_counter),

        "opportunity_distribution": dict(opportunity_counter),

        "risk_distribution": dict(risk_counter),

        "market_activities": market_signals
    }


def get_market_summary(signals):

    report = analyze_market(signals)

    summary = [
        f"Market intelligence signals: {report['total_market_signals']}"
    ]

    if report["opportunity_distribution"]:

        top_opportunity = max(
            report["opportunity_distribution"],
            key=report["opportunity_distribution"].get
        )

        summary.append(
            f"Most frequently detected opportunity: {top_opportunity}"
        )

    if report["risk_distribution"]:

        top_risk = max(
            report["risk_distribution"],
            key=report["risk_distribution"].get
        )

        summary.append(
            f"Most frequently detected risk: {top_risk}"
        )

    return summary
