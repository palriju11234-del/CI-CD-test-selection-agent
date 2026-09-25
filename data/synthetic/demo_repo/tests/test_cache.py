import app.cache.cache as cache_module


def test_get_returns_none_for_missing_query(monkeypatch):
	monkeypatch.setattr(cache_module, "cache", {})
	assert cache_module.get("missing") is None


def test_save_and_get_round_trip(monkeypatch):
	monkeypatch.setattr(cache_module, "cache", {})
	cache_module.save("Hello", "Hi there!")
	assert cache_module.get("Hello") == "Hi there!"
