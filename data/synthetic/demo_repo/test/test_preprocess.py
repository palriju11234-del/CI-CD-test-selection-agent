from app.ml.preprocess import clean_text

samples = [
    "Water BOILS at 100 Degrees Celsius!!!",
    "The Earth is Flat???",
    "Python   is    AWESOME!!!"
]

for text in samples:
    print("=" * 50)
    print("Original :", text)
    print("Cleaned  :", clean_text(text))