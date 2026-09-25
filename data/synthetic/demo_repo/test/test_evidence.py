from app.evidence.extractor import EvidenceExtractor


search_results = [
    {
        "title": "Scientific Article",
        "url": "https://example.com/article",
        "content": "Scientists have published new research.",
        "source": "web",
        "published_at": None
    },
    {
        "title": "News Article",
        "url": "https://example.com/news",
        "content": "Researchers announced new findings.",
        "source": "news",
        "published_at": "2026-08-07T10:00:00Z"
    }
]


extractor = EvidenceExtractor()

evidence = extractor.extract(search_results)

print("\nExtracted Evidence:")
print(evidence)