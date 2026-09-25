"""
Tests for LLMAnalyzer.

The LLM is mocked so no real API key is required.
"""
from unittest.mock import MagicMock, patch
import json

import pytest


SAMPLE_EVIDENCE = [
    {
        "title": "Scientific Article",
        "url": "https://example.com/article",
        "content": "Scientists confirmed water boils at 100 degrees Celsius at sea level.",
        "source": "web",
        "published_at": None,
    },
    {
        "title": "News Article",
        "url": "https://example.com/news",
        "content": "Researchers discussed the boiling point of water under standard atmospheric pressure.",
        "source": "news",
        "published_at": "2026-08-07T10:00:00Z",
    },
]

MOCK_VERDICT = {"verdict": "true", "explanation": "Supported by evidence.", "confidence": 0.95}


@pytest.fixture
def mock_llm_analyzer():
    """Return an LLMAnalyzer with the Gemini client fully mocked."""
    with patch.dict("os.environ", {"GEMINI_API_KEY": "mock-key"}):
        with patch("app.llm.analyze.genai") as mock_genai:
            mock_response = MagicMock()
            mock_response.text = json.dumps(MOCK_VERDICT)
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_genai.Client.return_value = mock_client

            from app.llm.analyze import LLMAnalyzer
            analyzer = LLMAnalyzer()
            yield analyzer


def test_analyze_returns_verdict(mock_llm_analyzer):
    result = mock_llm_analyzer.analyze(
        claim="Water boils at 100 degrees Celsius at sea level.",
        evidence=SAMPLE_EVIDENCE,
        model_prediction="true",
        confidence=0.95,
    )
    assert result["verdict"] == "true"


def test_analyze_returns_explanation(mock_llm_analyzer):
    result = mock_llm_analyzer.analyze(
        claim="Water boils at 100 degrees Celsius at sea level.",
        evidence=SAMPLE_EVIDENCE,
        model_prediction="true",
        confidence=0.95,
    )
    assert isinstance(result["explanation"], str)
    assert len(result["explanation"]) > 0


def test_analyze_returns_confidence_float(mock_llm_analyzer):
    result = mock_llm_analyzer.analyze(
        claim="Water boils at 100 degrees Celsius at sea level.",
        evidence=SAMPLE_EVIDENCE,
        model_prediction="true",
        confidence=0.95,
    )
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 1.0


def test_analyze_echoes_claim(mock_llm_analyzer):
    claim = "Water boils at 100 degrees Celsius at sea level."
    result = mock_llm_analyzer.analyze(
        claim=claim,
        evidence=SAMPLE_EVIDENCE,
        model_prediction="true",
        confidence=0.95,
    )
    assert result["claim"] == claim