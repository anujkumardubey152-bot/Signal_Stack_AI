
# ==========================================
# SIGNAL STACK AI
# Step 27: Intelligent Pipeline Integration
# ==========================================

from modules.classifier import classify_signal, calculate_relevance
from modules.database import save_signal, get_all_signals
from modules.prioritizer import prioritize_signal


def process_signal(signal):

    """
    Process one intelligence signal through
    classification, enrichment, prioritization
    and database storage.
    """

    # Step 1: Prepare signal text
    title = str(signal.get("title", ""))
    content = str(
        signal.get("content", signal.get("description", ""))
    )

    combined_text = f"{title} {content}"

    # Step 2: Classify signal
    signal["category"] = classify_signal(combined_text)

    # Step 3: Calculate relevance
    signal["relevance_score"] = calculate_relevance(combined_text)

    # Step 4: Prioritize signal
    signal = prioritize_signal(signal)

    # Step 5: Save signal to database
    saved = save_signal(signal)

    if saved:
        signal["status"] = "Saved"
    else:
        signal["status"] = "Duplicate"

    return signal


def process_signals(signals):

    """
    Process multiple intelligence signals.
    """

    results = []

    for signal in signals:

        processed = process_signal(signal)

        results.append(processed)

    return results


def get_prioritized_signals():

    """
    Retrieve stored signals and sort them
    by their priority score.
    """

    signals = get_all_signals()

    prioritized = []

    for signal in signals:

        # Recalculate priority using stored information
        signal = prioritize_signal(dict(signal))

        prioritized.append(signal)

    return sorted(
        prioritized,
        key=lambda x: x.get("priority_score", 0),
        reverse=True
    )
