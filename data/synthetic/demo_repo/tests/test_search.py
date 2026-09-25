from app.search.search import SearchEngine


search_engine = SearchEngine()

results = search_engine.search(
    "When will be under 15 football world cup hosted?"
)

print("\nNumber of results:", len(results))

for result in results:
    print("\n----------------------------")
    print("Title:", result.get("title"))
    print("URL:", result.get("url"))
    print("Source:", result.get("source"))
    print("Published:", result.get("published_at"))
    print("Content:", result.get("content", "")[:200])