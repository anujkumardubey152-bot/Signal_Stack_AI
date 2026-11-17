
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def research_company(website):

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; SignalStackAI/1.0)"
    }

    try:
        response = requests.get(
            website,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        title = soup.title.get_text(strip=True) if soup.title else ""

        description_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        description = (
            description_tag.get("content", "")
            if description_tag else ""
        )

        headings = [
            h.get_text(" ", strip=True)
            for h in soup.find_all(["h1", "h2", "h3"])
        ]

        paragraphs = [
            p.get_text(" ", strip=True)
            for p in soup.find_all("p")
            if len(p.get_text(strip=True)) > 40
        ]

        links = [
            urljoin(website, a.get("href"))
            for a in soup.find_all("a", href=True)
        ]

        return {
            "website": website,
            "title": title,
            "description": description,
            "headings": headings[:20],
            "paragraphs": paragraphs[:30],
            "links": links[:30],
            "status": "Success"
        }

    except Exception as e:

        return {
            "website": website,
            "status": "Failed",
            "error": str(e)
        }
