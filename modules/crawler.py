
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlparse
import hashlib
import time

HEADERS = {
    "User-Agent": "SignalStackAI/1.0 (public research bot)"
}

def crawl_source(url):

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return {"status": "Rejected", "error": "Invalid URL scheme"}

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "text/html" not in content_type:
            return {
                "status": "Skipped",
                "error": "Not an HTML page"
            }

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script", "style", "nav",
            "footer", "header", "noscript"
        ]):
            tag.decompose()

        title = (
            soup.title.get_text(strip=True)
            if soup.title else ""
        )

        text = soup.get_text(" ", strip=True)

        # Generate content fingerprint
        fingerprint = hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

        return {
            "url": url,
            "title": title,
            "content": text[:12000],
            "content_hash": fingerprint,
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "status": "Success"
        }

    except Exception as error:

        return {
            "url": url,
            "status": "Failed",
            "error": str(error)
        }
