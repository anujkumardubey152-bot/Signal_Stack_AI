
from duckduckgo_search import DDGS

def discover_sources(company_name, industry="education"):

    queries = [
        f"{company_name} competitors {industry}",
        f"{industry} industry news",
        f"{industry} customer reviews complaints",
        f"{industry} market trends regulations"
    ]

    discovered = []

    with DDGS() as ddgs:

        for query in queries:

            try:
                results = ddgs.text(
                    query,
                    max_results=5
                )

                for result in results:

                    discovered.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                        "query": query
                    })

            except Exception as error:
                print("Search error:", error)

    # Remove duplicate URLs
    unique_sources = {}
    
    for source in discovered:
        url = source["url"]

        if url and url not in unique_sources:
            unique_sources[url] = source

    return list(unique_sources.values())
