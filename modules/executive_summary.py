
from collections import Counter


def safe_number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0


def generate_executive_summary(signals):

    signals = signals or []

    total_signals = len(signals)

    category_counts = Counter()
    priority_counts = Counter()

    critical_signals = []
    high_priority_signals = []

    opportunities = []
    risks = []

    for signal in signals:

        category = str(
            signal.get("category", "Unknown")
        ).strip().title()

        priority = str(
            signal.get("priority", "Normal")
        ).strip().lower()

        category_counts[category] += 1
        priority_counts[priority.title()] += 1

        if priority in ["critical", "urgent"]:
            critical_signals.append(signal)

        elif priority == "high":
            high_priority_signals.append(signal)

        text = (
            str(signal.get("title", ""))
            + " "
            + str(signal.get("content", ""))
        ).lower()

        opportunity_keywords = [
            "opportunity", "growth", "expansion",
            "partnership", "innovation", "demand",
            "investment", "potential"
        ]

        risk_keywords = [
            "risk", "threat", "fraud", "loss",
            "decline", "failure", "breach",
            "complaint", "churn", "delay"
        ]

        if any(word in text for word in opportunity_keywords):
            opportunities.append(signal)

        if any(word in text for word in risk_keywords):
            risks.append(signal)

    category_summary = [
        {
            "category": category,
            "signal_count": count,
            "percentage": round(
                (count / total_signals) * 100, 2
            ) if total_signals else 0
        }
        for category, count in category_counts.most_common()
    ]

    recommendations = []

    if critical_signals:
        recommendations.append(
            "Immediately review critical and urgent signals "
            "and assign responsible owners."
        )

    if high_priority_signals:
        recommendations.append(
            "Prioritize high-priority signals in the next "
            "business review."
        )

    if risks:
        recommendations.append(
            "Investigate detected business risks and develop "
            "appropriate mitigation plans."
        )

    if opportunities:
        recommendations.append(
            "Evaluate identified growth opportunities for "
            "potential business value."
        )

    if category_counts.get("Customers", 0):
        recommendations.append(
            "Review customer feedback, complaints, and churn "
            "indicators to improve customer experience."
        )

    if category_counts.get("Competitors", 0):
        recommendations.append(
            "Monitor competitor activities and evaluate "
            "their possible impact on business strategy."
        )

    if category_counts.get("Market", 0):
        recommendations.append(
            "Track market developments, emerging trends, "
            "and regulatory changes."
        )

    if category_counts.get("Internal", 0):
        recommendations.append(
            "Review internal operational performance and "
            "organizational issues."
        )

    if not recommendations:
        recommendations.append(
            "Continue collecting relevant business signals "
            "to strengthen intelligence coverage."
        )

    return {
        "total_signals": total_signals,
        "category_counts": dict(category_counts),
        "priority_counts": dict(priority_counts),
        "category_summary": category_summary,
        "critical_signals": critical_signals,
        "high_priority_signals": high_priority_signals,
        "total_critical": len(critical_signals),
        "total_high_priority": len(high_priority_signals),
        "opportunities": opportunities,
        "total_opportunities": len(opportunities),
        "risks": risks,
        "total_risks": len(risks),
        "recommendations": recommendations
    }


def get_executive_report(signals):

    report = generate_executive_summary(signals)

    return {
        "overview": {
            "total_signals": report["total_signals"],
            "critical_signals": report["total_critical"],
            "high_priority_signals": report["total_high_priority"],
            "opportunities": report["total_opportunities"],
            "risks": report["total_risks"]
        },
        "category_summary": report["category_summary"],
        "priority_distribution": report["priority_counts"],
        "recommendations": report["recommendations"]
    }
