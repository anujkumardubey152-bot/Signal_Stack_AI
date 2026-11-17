
def generate_signal_stack(profile):

    company = profile.get("company_name", "Company")

    signal_stack = {

        "Customers": {
            "description": "Understand customer problems, expectations and complaints.",
            "sources": [
                {
                    "name": "Reddit",
                    "url": "https://www.reddit.com/",
                    "reason": "Discover genuine customer discussions and unmet needs."
                },
                {
                    "name": "Quora",
                    "url": "https://www.quora.com/",
                    "reason": "Identify questions and problems related to education services."
                },
                {
                    "name": "Google Reviews",
                    "url": "https://www.google.com/maps",
                    "reason": "Understand customer experiences and complaints."
                }
            ]
        },

        "Competitors": {
            "description": "Monitor alternatives and competitor developments.",
            "sources": [
                {
                    "name": "Competitor Websites",
                    "url": "https://www.google.com/",
                    "reason": f"Discover competitors offering alternatives to {company}."
                },
                {
                    "name": "Competitor News",
                    "url": "https://news.google.com/",
                    "reason": "Monitor competitor launches, partnerships and expansion."
                }
            ]
        },

        "Market": {
            "description": "Monitor education industry and regulatory changes.",
            "sources": [
                {
                    "name": "UGC",
                    "url": "https://www.ugc.gov.in/",
                    "reason": "Monitor higher education regulatory developments."
                },
                {
                    "name": "Ministry of Education",
                    "url": "https://www.education.gov.in/",
                    "reason": "Track education policies and government announcements."
                },
                {
                    "name": "Google News",
                    "url": "https://news.google.com/",
                    "reason": "Discover major education industry developments."
                }
            ]
        },

        "Internal": {
            "description": "Understand internal business performance and feedback.",
            "sources": [
                {
                    "name": "CRM Data",
                    "url": "",
                    "reason": "Identify sales patterns and lost-deal reasons."
                },
                {
                    "name": "Customer Feedback",
                    "url": "",
                    "reason": "Identify recurring complaints and product requests."
                },
                {
                    "name": "Sales Transcripts",
                    "url": "",
                    "reason": "Discover customer objections and buying motivations."
                }
            ]
        }
    }

    return signal_stack
