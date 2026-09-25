from app.evidence.extractor import EvidenceExtractor


def test_extract_keeps_results_with_content():
    search_results = [
        {
            "title": "Scientific Article",
            "url": "https://example.com/article",
            "content": "Scientists have published new research.",
            "source": "web",
            "published_at": None,
        },
        {"title": "Empty result", "content": ""},
    ]

    evidence = EvidenceExtractor().extract(search_results)

    assert evidence == [search_results[0]]


def test_extract_returns_empty_list_without_content():
    assert EvidenceExtractor().extract([{"title": "No content"}]) == []