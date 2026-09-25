from app.search.search import SearchEngine

from app.search.search import SearchEngine



def test_search_combines_web_and_news_results(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
    monkeypatch.setenv("NEWS_API_KEY", "test-news-key")

    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            pass

        def json(self):
            return self.payload

    monkeypatch.setattr(
        "app.search.search.httpx.post",
        lambda *args, **kwargs: FakeResponse(
            {"results": [{"title": "Web result", "url": "https://web.test", "content": "Web"}]}
        ),
    )
    monkeypatch.setattr(
        "app.search.search.httpx.get",
        lambda *args, **kwargs: FakeResponse(
            {"articles": [{"title": "News result", "url": "https://news.test", "description": "News"}]}
        ),
    )

    results = SearchEngine().search("example query")

    assert [result["source"] for result in results] == ["web", "news"]
    assert [result["title"] for result in results] == ["Web result", "News result"]