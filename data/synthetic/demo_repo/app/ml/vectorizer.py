from sklearn.feature_extraction.text import TfidfVectorizer


def create_vectorizer():
    """
    Create a TF-IDF Vectorizer.
    """

    vectorizer = TfidfVectorizer()

    return vectorizer