import joblib
import numpy as np

from app.ml.preprocess import clean_text


class FactCheckModel:

    def __init__(self):

        # Load trained model
        self.model = joblib.load(
            "app/models/model.joblib"
        )

        # Load TF-IDF vectorizer
        self.vectorizer = joblib.load(
            "app/models/vectorizer.joblib"
        )

    def predict(self, query: str):

        # Clean input
        query = clean_text(query)

        # Convert text to TF-IDF
        vector = self.vectorizer.transform([query])

        # Predict label
        label = self.model.predict(vector)[0]

        # Get SVM decision scores
        scores = self.model.decision_function(vector)[0]

        # Convert scores to approximate probabilities
        exp_scores = np.exp(scores - np.max(scores))
        probabilities = exp_scores / exp_scores.sum()

        # Confidence of predicted class
        confidence = float(np.max(probabilities))

       