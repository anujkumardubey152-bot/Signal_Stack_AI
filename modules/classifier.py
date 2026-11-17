
def classify_signal(text):

    text = text.lower()

    categories = {
        "Customers": [
            "student", "customer", "user", "review",
            "complaint", "feedback", "parent", "learner"
        ],

        "Competitors": [
            "competitor", "rival", "alternative",
            "pricing", "launch", "product", "platform"
        ],

        "Market": [
            "industry", "market", "regulation",
            "trend", "policy", "funding", "technology"
        ],

        "Internal": [
            "employee", "hiring", "team", "leadership",
            "company culture", "layoff", "internal"
        ]
    }

    scores = {} 

    for category, keywords in categories.items():
        scores[category] = sum(
            1 for keyword in keywords if keyword in text
        )

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        best_category = "Market"

    return best_category


def calculate_relevance(text):

    text = text.lower()

    important_terms = [
        "major", "urgent", "growth", "decline",
        "funding", "acquisition", "launch",
        "partnership", "regulation", "risk",
        "revenue", "expansion"
    ]

    matches = sum(
        1 for term in important_terms if term in text
    )

    return min(100, 30 + matches * 10)


def enrich_signal(signal):

    text = (
        str(signal.get("title", "")) + " " +
        str(signal.get("content", "")) + " " +
        str(signal.get("description", ""))
    )

    signal["category"] = classify_signal(text)
    signal["relevance_score"] = calculate_relevance(text)

    return signal
