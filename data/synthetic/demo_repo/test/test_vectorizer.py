from app.ml.dataset import load_dataset
from app.ml.vectorizer import create_vectorizer

# Load dataset
X, y = load_dataset("data/claims.csv")

# Create vectorizer
vectorizer = create_vectorizer()

# Convert text into vectors
X_vectors = vectorizer.fit_transform(X)

print("Vocabulary:\n")
print(vectorizer.vocabulary_)

print("\n----------------------------")

print("Vector Shape:")
print(X_vectors.shape)

print("\n----------------------------")

print("First Sentence Vector:")

print(X_vectors[0].toarray())