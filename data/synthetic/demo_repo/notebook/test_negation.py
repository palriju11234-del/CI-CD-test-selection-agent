import joblib
from scipy.sparse import hstack

from app.ml.preprocess import clean_text


class NegationTestModel:

    def __init__(self):
        self.model = joblib.load(
            "models/sentence_lr/classifier.joblib"
        )

        self.word_vectorizer = joblib.load(
            "models/sentence_lr/word_vectorizer.joblib"
        )

        self.char_vectorizer = joblib.load(
            "models/sentence_lr/char_vectorizer.joblib"
        )

    def predict(self, text):

        text = clean_text(text)

        word_vector = self.word_vectorizer.transform([text])
        char_vector = self.char_vectorizer.transform([text])

        vector = hstack([
            word_vector,
            char_vector
        ])

        return self.model.predict(vector)[0]


model = NegationTestModel()


tests = [
    ("The sun does not revolve around Earth.", "true"),
    ("Dogs and humans do not have tails.", "true"),
    ("Water does not boil at 50 degrees Celsius at sea level.", "true"),
    ("The Earth is not flat.", "true"),
    ("The sun revolves around Earth.", "false"),
    ("Dogs and humans have tails.", "false"),
    ("Water boils at 50 degrees Celsius at sea level.", "false"),
    ("The Earth is flat.", "false"),
    ("The moon does not produce its own light.", "true"),
    ("The moon produces its own light.", "false"),
    ("Humans cannot breathe underwater without equipment.", "true"),
    ("Humans can breathe underwater without equipment.", "false"),
]


print("=" * 70)
print("NEGATION TEST — WORD + CHARACTER TF-IDF")
print("=" * 70)

correct = 0

for claim, expected in tests:

    predicted = model.predict(claim)

    status = "PASS" if predicted == expected else "FAIL"

    if status == "PASS":
        correct += 1

    print()
    print("Claim:   ", claim)
    print("Expected:", expected)
    print("Predicted:", predicted)
    print(status)


print()
print("=" * 70)
print(f"Negation accuracy: {correct}/{len(tests)}")
print("=" * 70)