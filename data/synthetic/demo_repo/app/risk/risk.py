
"""
Risk Assessment Module

This module decides whether the prediction from our
trained model is reliable enough.
"""

class RiskAssessment:

    def __init__(self, threshold=0.95):
        self.threshold = threshold

    def assess(self, label, confidence):
        """
        Decide whether a prediction is safe to trust.
        """

        # If the model itself is uncertain, always verify online
        if label == "uncertain":
            return "HIGH_RISK"

        # High confidence + definite label
        if confidence >= self.threshold:
            return "LOW_RISK"

        return "HIGH_RISK"

