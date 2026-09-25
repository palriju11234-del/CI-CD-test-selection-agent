"""
Evidence Extraction Module

Converts raw search results into a clean evidence format
for the next stage of the fact-checking pipeline.
"""


class EvidenceExtractor:

    def extract(self, search_results: list):

        evidence = []

        for result in search_results:

            content = result.get("content")

            # Skip results without useful content
            if not content:
                continue

            evidence.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content": content,
                "source": result.get("source"),
                "published_at": result.get("published_at")
            })

        return evidence