from app.ml.model import FactCheckModel

model = FactCheckModel()

result = model.predict(
    "india's prime minister is Narendra Modi."
)

print(result)