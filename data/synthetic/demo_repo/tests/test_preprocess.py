from app.ml.preprocess import clean_text


def test_clean_text_lowercases_and_removes_punctuation():
    assert clean_text("Water BOILS at 100 Degrees Celsius!!!") == (
        "water boils at 100 degrees celsius"
    )


def test_clean_text_collapses_whitespace():
    assert clean_text("Python   is    AWESOME!!!") == "python is awesome"