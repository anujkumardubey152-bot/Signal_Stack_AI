
# ==========================================
# SIGNAL STACK AI
# Step 31: Competitor Intelligence Analyzer
# ==========================================

import re
from collections import Counter


COMPETITOR_EVENTS = {
    "Product Launch": [
        "launched", "launching", "new product",
        "released", "release", "introduced"
    ],
    "Funding": [
        "funding", "raised", "investment",
        "investor", "series a", "series b",
        "venture capital"
    ],
    "Acquisition": [
        "acquisition", "acquired", "merger",
        "bought", "takeover"
    ],
    "Partnership": [
        "partnership", "partnered", "collaboration",
        "strategic alliance"
    ],
    "Expansion": [
        "expansion", "expanded", "entered market",
        "new market", "global expansion"
    ],
    "Pricing Change": [
        "price increase", "price reduction",
        "pricing", "subscription price",
        "free plan", "premium plan"
    ],
    "Leadership Change": [
        "appointed ceo", "new ceo",
        "resigned", "chief executive",
        "leadership change"
    ],
    "Technology": [
        "artificial intelligence", "machine learning",
        "ai model", "automation", "technology"
    ]
}


def detect_competitor_events(text):

    text = str(text).lower()

    detected = []

    for event, keywords in COMPETITOR_EVENTS.items():

        if any(keyword in text for keyword in keywords):
            detected.append(event)

    return detected


def extract_competitor_names(signals):

    """
    Extract explicitly named competitors from signal metadata.

    Supports competitor_name and competitors fields.
    Does not guess company identities from article text.
    """

    names = []

    for signal in signals:

        name = signal.get("competitor_name")

        if isinstance(name, str) and name.strip():
            names.append(name.strip())

        competitors = signal.get("competitors", [])

        if isinstance(competitors, str):
            competitors = [competitors]

        if isinstance(competitors, (list, tuple, set)):

            for competitor in competitors:

                if isinstance(competitor, str) and competitor.strip():
                    names.append(competitor.strip())

    return sorted(set(names), key=str.lower)


def analyze_competitor_signal(signal):

    title = str(signal.get("title", ""))

    content = str(
        signal.get("content", signal.get("description", ""))
    )

    text = f"{title} {content}"

    events = detect_competitor_events(text)

    return {
        "title": title,
        "competitor_name": signal.get("competitor_name", "Unspecified"),
        "events": events,
        "event_count": len(events),
        "priority": signal.get("priority", "Low"),
        "relevance_score": signal.get("relevance_score", 0),
        "source": signal.get("source", "Unknown")
    }


def analyze_competitors(signals):

    """
    Generate a complete competitor intelligence report.
    """

    competitor_signals = []

    event_counter = Counter()

    for signal in signals:

        category = str(signal.get("category", "")).lower()

        if category != "competitors":
            continue

        result = analyze_competitor_signal(signal)

        competitor_signals.append(result)

        event_counter.update(result["events"])

    return {
        "total_competitor_signals": len(competitor_signals),
        "competitor_names": extract_competitor_names(signals),
        "event_distribution": dict(event_counter),
        "competitor_activities": competitor_signals
    }


def get_competitor_summary(signals):

    report = analyze_competitors(signals)

    summary = [
        f"Competitor intelligence signals: {report['total_competitor_signals']}"
    ]

    if report["event_distribution"]:

        top_event = max(
            report["event_distribution"],
            key=report["event_distribution"].get
        )

        summary.append(
            f"Most common competitor activity: {top_event}"
        )

    else:

        summary.append(
            "No recognizable competitor events identified yet."
        )

    if report["competitor_names"]:

        summary.append(
            "Named competitors: " + ", ".join(report["competitor_names"])
        )

    return summary
