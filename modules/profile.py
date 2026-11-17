
def generate_company_profile(research_data):

    if research_data.get("status") != "Success":
        return {
            "status": "Failed",
            "message": "Website research was unsuccessful."
        }

    profile = {
        "company_name": "MeetUniversity",
        "website": research_data["website"],
        "website_title": research_data.get("title", ""),
        "website_description": research_data.get("description", ""),
        "observed_headings": research_data.get("headings", []),
        "observed_content": research_data.get("paragraphs", []),
        "research_status": "Website content extracted",
        "verification_note": (
            "This profile contains website observations. "
            "Business claims require independent verification."
        )
    }

    return profile
