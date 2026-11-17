
# ==========================================
# SIGNAL STACK AI
# Step 33: Customer Intelligence Analyzer
# ==========================================

from collections import Counter
import re


CUSTOMER_PATTERNS = {

    "Complaint": [
        "complaint", "unhappy", "dissatisfied",
        "poor service", "bad experience",
        "not working", "broken", "disappointed"
    ],

    "Positive Feedback": [
        "excellent service", "great experience",
        "love the product", "highly recommend",
        "satisfied", "amazing service", "thank you"
    ],

    "Feature Request": [
        "feature request", "please add",
        "need a feature", "wish it had",
        "would like to see", "suggestion"
    ],

    "Pricing Concern": [
        "too expensive", "overpriced",
        "high price", "pricing issue",
        "cost too much", "expensive"
    ],

    "Support Issue": [
        "customer support", "support ticket",
        "not responding", "slow response",
        "help desk", "technical support"
    ],

    "Product Issue": [
        "bug", "crash", "error",
        "performance issue", "not loading",
        "not functioning", "glitch"
    ],

    "Purchase Intent": [
        "want to buy", "ready to purchase",
        "looking to buy", "interested in buying",
        "planning to purchase"
    ],

    "Churn Risk": [
        "cancel subscription", "switching provider",
        "leaving the platform", "stop using",
        "unsubscribe", "moving to competitor"
    ]
}


def get_signal_text(signal):

    title = str(signal.get("title", ""))

    content = str(
        signal.get("content", signal.get("description", ""))
    )

    return f"{title} {content}".lower()


def detect_customer_events(text):

    """
    Identify customer-related events.
    """

    text = str(text).lower()

    detected = []

    for event, keywords in CUSTOMER_PATTERNS.items():

        if any(keyword in text for keyword in keywords):
            detected.append(event)

    return detected


def calculate_customer_sentiment(events):

    """
    Rule-based sentiment indicator.
    This is not a trained sentiment model.
    """

    positive = "Positive Feedback" in events

    negative_events = [
        "Complaint",
        "Pricing Concern",
        "Support Issue",
        "Product Issue",
        "Churn Risk"
    ]

    negative = any(
        event in events for event in negative_events
    )

    if positive and negative:
        return "Mixed"

    if positive:
        return "Positive"

    if negative:
        return "Negative"

    return "Neutral"


def analyze_customer_signal(signal):

    text = get_signal_text(signal)

    events = detect_customer_events(text)

    return {
        "title": signal.get("title", ""),
        "customer_events": events,
        "sentiment": calculate_customer_sentiment(events),
        "event_count": len(events),
        "priority": signal.get("priority", "Low"),
        "relevance_score": signal.get("relevance_score", 0),
        "source": signal.get("source", "Unknown")
    }


def analyze_customers(signals):

    """
    Generate customer intelligence report.
    """

    customer_signals = []

    event_counter = Counter()
    sentiment_counter = Counter()

    for signal in signals:

        category = str(
            signal.get("category", "")
        ).lower()

        if category != "customers":
            continue

        result = analyze_customer_signal(signal)

        customer_signals.append(result)

        event_counter.update(result["customer_events"])

        sentiment_counter.update([result["sentiment"]])

    return {

        "total_customer_signals": len(customer_signals),

        "event_distribution": dict(event_counter),

        "sentiment_distribution": dict(sentiment_counter),

        "customer_activities": customer_signals
    }


def get_customer_summary(signals):

    report = analyze_customers(signals)

    summary = [
        f"Customer intelligence signals: {report['total_customer_signals']}"
    ]

    if report["sentiment_distribution"]:

        dominant_sentiment = max(
            report["sentiment_distribution"],
            key=report["sentiment_distribution"].get
        )

        summary.append(
            f"Dominant sentiment indicator: {dominant_sentiment}"
        )

    if report["event_distribution"]:

        top_event = max(
            report["event_distribution"],
            key=report["event_distribution"].get
        )

        summary.append(
            f"Most common customer activity: {top_event}"
        )

    return summary
