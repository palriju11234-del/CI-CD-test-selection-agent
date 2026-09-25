"""
Simple in-memory cache.

Stores:
Question -> Answer
"""

cache = {}

def get(query: str):
    """
    Return cached answer if present.
    """
    return cache.get(query)


def save(query: str, answer: str):
    """
    Save answer in cache.
    """
    cache[query] = answer