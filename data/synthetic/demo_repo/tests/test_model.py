from app.ml.model import FactCheckModel



def test_fact_check_model_returns_prediction_fields():
    result = FactCheckModel().predict(
        "india's prime minister is Narendra Modi."
    )

    assert set(result) == {"label", "confidence", "scores"}
    assert isinstance(result["label"], str)
    assert 0.0 <= result["confidence"] <= 1.0
    assert isinstance(result["scores"], list)