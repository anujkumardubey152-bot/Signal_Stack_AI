
def generate_interview_questions(profile):

    company = profile.get("company_name", "the company")
    description = profile.get("website_description", "")

    questions = [
        f"What are the main products or services offered by {company}?",

        "Which products or services generate the most revenue?",

        "Who are your highest-value customer segments?",

        "What are the biggest problems your customers face?",

        "Why do customers choose your company over alternatives?",

        "Which competitors or substitutes do you consider most important?",

        "What major changes in your industry could affect your business?",

        "What are your most important growth priorities for the next 6–12 months?",

        "Which internal business information should influence intelligence decisions?",

        "What important decisions should this intelligence system help you make?"
    ]

    return questions


def save_interview_answer(answers, question, answer):

    answers[question] = answer

    return answers
