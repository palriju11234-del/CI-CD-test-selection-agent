import pytest

from app.ml.model import FactCheckModel



@pytest.mark.parametrize(
    "claim",
    [
        "Water boils at 100 degrees Celsius.",
        "The Earth is flat.",
        "Aliens definitely exist.",
    ],
)
def test_trained_model_predicts_for_claim(claim):
    result = FactCheckModel().predict(claim)

    assert result["label"]
    assert 0.0 <= result["confidence"] <= 1.0