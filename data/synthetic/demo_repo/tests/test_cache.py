from app.cache.cache import get, save

print(get("Hello"))

save("Hello", "Hi there!")

print(get("Hello"))
