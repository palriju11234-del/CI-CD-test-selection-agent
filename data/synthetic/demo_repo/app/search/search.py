"""
Search Module

Performs both web search and news search.
"""

import os
import httpx
from dotenv import load_dotenv


load_dotenv()


class SearchEngine:

    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")

        if not self.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not set")

        if not self.news_api_key:
            raise ValueError("NEWS_API_KEY is not set")

        self.tavily_url = "https://api.tavily.com/search"
        self.news_url = "https://newsapi.org/v2/everything"

    def search_web(self, query: str):

        response = httpx.post(
            self.tavily_url,
            json={
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": 5
            },
            timeout=30.0
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
                "source": "web",
                "published_at": None
            })

        return results

    def search_news(self, query: str):

        response = httpx.get(
            self.news_url,
            params={
                "q": query,
                "apiKey": self.news_api_key,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5
            },
            timeout=30.0
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for article in data.get("articles", []):
            results.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "content": article.get("description"),
                "source": "news",
                "published_at": article.get("publishedAt")
            })

        return results

    def search(self, query: str):

        web_results = self.search_web(query)
        news_results = self.search_news(query)

        return web_results + news_results