from app.ml.model import FactCheckModel

model = FactCheckModel()

claims = [
    "Water boils at 100 degrees Celsius.",
    "The Earth is flat.",
    "Aliens definitely exist."
]

for claim in claims:
    result = model.predict(claim)

    print("=" * 50)
    print("Claim:", claim)
    print("Prediction:", result["label"])
    print("Confidence:", round(result["confidence"], 3))