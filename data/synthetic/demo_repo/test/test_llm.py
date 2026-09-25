from app.llm.analyze import LLMAnalyzer


analyzer = LLMAnalyzer()


evidence = [
    {
        "title": "Scientific Article",
        "url": "https://example.com/article",
        "content": "Scientists published research confirming that water boils at approximately 100 degrees Celsius at sea level.",
        "source": "web",
        "published_at": None
    },
    {
        "title": "News Article",
        "url": "https://example.com/news",
        "content": "Researchers discussed the boiling point of water under standard atmospheric pressure.",
        "source": "news",
        "published_at": "2026-08-07T10:00:00Z"
    }
]


result = analyzer.analyze(
    claim="Water boils at 100 degrees Celsius at sea level.",
    evidence=evidence,
    model_prediction="true",
    confidence=0.95
)


print("\n========== LLM RESULT ==========")

print("Verdict:", result["verdict"])
print("Explanation:", result["explanation"])
print("Confidence:", result["confidence"])