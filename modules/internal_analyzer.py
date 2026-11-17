
import re
from collections import Counter


INTERNAL_PATTERNS = {
    "Operational Issue": [
        "operational issue", "process failure", "workflow problem",
        "production delay", "system downtime", "operational delay",
        "inefficiency", "operational risk"
    ],
    "Employee & Workforce": [
        "employee", "workforce", "hiring", "recruitment",
        "resignation", "layoff", "staff", "team expansion",
        "employee satisfaction", "training"
    ],
    "Financial Performance": [
        "revenue", "profit", "loss", "budget", "expenses",
        "financial performance", "cash flow", "cost reduction",
        "financial results", "quarterly earnings"
    ],
    "Internal Processes": [
        "internal process", "workflow", "automation",
        "process improvement", "approval process",
        "documentation", "standard operating procedure",
        "process optimization"
    ],
    "Technology & Infrastructure": [
        "infrastructure", "server", "database", "cloud migration",
        "cybersecurity", "software upgrade", "technical issue",
        "IT system", "technology upgrade", "security breach"
    ],
    "Strategic Decisions": [
        "business strategy", "strategic decision", "restructuring",
        "new initiative", "company direction", "business expansion",
        "organizational change", "strategic planning"
    ],
    "Productivity & Performance": [
        "productivity", "performance", "KPI", "target achieved",
        "missed target", "team performance", "efficiency",
        "employee performance", "performance improvement"
    ],
    "Organizational Risk": [
        "compliance failure", "legal risk", "security risk",
        "data breach", "regulatory violation", "internal fraud",
        "business continuity", "organizational risk"
    ]
}


def extract_internal_text(signal):
    if isinstance(signal, dict):
        title = str(signal.get("title", ""))
        content = str(signal.get("content", ""))
        return f"{title} {content}".lower()

    return str(signal).lower()


def detect_internal_events(text):
    text = str(text).lower()
    detected = []

    for event, keywords in INTERNAL_PATTERNS.items():
        matched = [
            keyword for keyword in keywords
            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            )
        ]

        if matched:
            detected.append({
                "event": event,
                "matched_keywords": matched,
                "keyword_count": len(matched)
            })

    return detected


def analyze_internal_signal(signal):
    text = extract_internal_text(signal)

    events = detect_internal_events(text)

    return {
        "title": signal.get("title", "Untitled")
        if isinstance(signal, dict) else "Untitled",
        "category": "Internal",
        "events": events,
        "event_count": len(events),
        "matched_keywords": [
            keyword
            for event in events
            for keyword in event["matched_keywords"]
        ],
        "source": signal.get("source", "Unknown")
        if isinstance(signal, dict) else "Unknown"
    }


def analyze_internal(signals):
    internal_signals = [
        signal for signal in signals
        if str(signal.get("category", "")).lower() == "internal"
    ]

    activities = [
        analyze_internal_signal(signal)
        for signal in internal_signals
    ]

    event_counter = Counter()
    keyword_counter = Counter()

    for activity in activities:
        for event in activity["events"]:
            event_counter[event["event"]] += 1
            keyword_counter.update(event["matched_keywords"])

    return {
        "total_signals": len(internal_signals),
        "total_events": sum(event_counter.values()),
        "event_distribution": [
            {"event": event, "count": count}
            for event, count in event_counter.most_common()
        ],
        "keyword_distribution": [
            {"keyword": keyword, "count": count}
            for keyword, count in keyword_counter.most_common()
        ],
        "activities": activities
    }


def get_internal_summary(signals):
    report = analyze_internal(signals)

    return {
        "total_signals": report["total_signals"],
        "total_events": report["total_events"],
        "event_distribution": report["event_distribution"],
        "top_events": report["event_distribution"][:5],
        "top_keywords": report["keyword_distribution"][:10]
    }
