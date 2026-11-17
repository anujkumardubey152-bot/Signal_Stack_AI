
# ==========================================
# SIGNAL STACK AI
# Step 29: Intelligence Trend Analysis
# ==========================================

from collections import Counter
from datetime import datetime, timezone
import re


STOPWORDS = {
    "the", "and", "for", "are", "was", "were",
    "with", "this", "that", "from", "have",
    "has", "had", "will", "would", "could",
    "should", "their", "there", "about", "into",
    "your", "you", "our", "they", "them",
    "its", "not", "but", "all", "can", "may",
    "more", "than", "also", "new", "how",
    "what", "when", "where", "which", "who",
    "why", "been", "being", "after", "before",
    "over", "under", "between", "while", "through",
    "company", "companies", "business"
}


def extract_text(signal):

    title = str(signal.get("title", ""))
    content = str(
        signal.get("content", signal.get("description", ""))
    )

    return f"{title} {content}".lower()


def extract_keywords(signals):

    """
    Extract frequently occurring meaningful keywords.
    """

    words = []

    for signal in signals:

        text = extract_text(signal)

        tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b", text)

        words.extend(
            word for word in tokens
            if word not in STOPWORDS
        )

    return Counter(words)


def analyze_categories(signals):

    """
    Calculate the distribution of intelligence categories.
    """

    categories = Counter()

    for signal in signals:

        category = str(
            signal.get("category", "Uncategorized")
        )

        categories[category] += 1

    return dict(categories)


def parse_signal_date(signal):

    """
    Read a date from commonly used timestamp fields.
    """

    date_fields = [
        "created_at",
        "timestamp",
        "published_at",
        "date",
        "collected_at"
    ]

    for field in date_fields:

        value = signal.get(field)

        if not value:
            continue

        if isinstance(value, datetime):
            return value.replace(tzinfo=None)

        if isinstance(value, (int, float)):

            try:
                return datetime.fromtimestamp(
                    value, tz=timezone.utc
                ).replace(tzinfo=None)

            except (ValueError, OSError, OverflowError):
                continue

        try:

            parsed = datetime.fromisoformat(
                str(value).replace("Z", "+00:00")
            )

            return parsed.replace(tzinfo=None)

        except (ValueError, TypeError):
            continue

    return None


def analyze_timeline(signals):

    """
    Group intelligence signals by collection date.
    """

    timeline = Counter()

    for signal in signals:

        date = parse_signal_date(signal)

        if date:
            timeline[date.strftime("%Y-%m-%d")] += 1

    return dict(sorted(timeline.items()))


def analyze_rising_topics(signals):

    """
    Compare keyword frequency in recent and previous
    periods to identify rising topics.
    """

    dated_signals = []

    for signal in signals:

        date = parse_signal_date(signal)

        if date:
            dated_signals.append((date, signal))

    if len(dated_signals) < 2:
        return []

    latest_date = max(date for date, _ in dated_signals)

    recent = []
    previous = []

    for date, signal in dated_signals:

        days_old = (latest_date - date).days

        if days_old <= 7:
            recent.append(signal)

        elif days_old <= 14:
            previous.append(signal)

    if not recent or not previous:
        return []

    recent_words = extract_keywords(recent)
    previous_words = extract_keywords(previous)

    rising_topics = []

    for word, count in recent_words.most_common(20):

        old_count = previous_words.get(word, 0)

        if count > old_count:

            rising_topics.append({
                "topic": word,
                "recent_mentions": count,
                "previous_mentions": old_count,
                "change": count - old_count
            })

    return sorted(
        rising_topics,
        key=lambda x: x["change"],
        reverse=True
    )


def generate_trend_report(signals):

    """
    Generate a complete intelligence trend report.
    """

    keywords = extract_keywords(signals)

    return {
        "total_signals": len(signals),

        "top_keywords": dict(
            keywords.most_common(15)
        ),

        "category_distribution": analyze_categories(signals),

        "timeline": analyze_timeline(signals),

        "rising_topics": analyze_rising_topics(signals)
    }


def get_trend_summary(signals):

    """
    Generate a simple human-readable trend summary.
    """

    report = generate_trend_report(signals)

    summary = []

    summary.append(
        f"Total intelligence signals analyzed: {report['total_signals']}"
    )

    if report["top_keywords"]:

        top_topic = next(iter(report["top_keywords"]))

        summary.append(
            f"Most frequently mentioned topic: {top_topic}"
        )

    if report["category_distribution"]:

        top_category = max(
            report["category_distribution"],
            key=report["category_distribution"].get
        )

        summary.append(
            f"Most active category: {top_category}"
        )

    if report["rising_topics"]:

        rising = report["rising_topics"][0]["topic"]

        summary.append(
            f"Top rising topic: {rising}"
        )

    else:

        summary.append(
            "Insufficient dated intelligence for rising-topic comparison."
        )

    return summary
