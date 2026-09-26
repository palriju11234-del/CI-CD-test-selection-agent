"""
LLM Analysis Module

Uses Gemini to analyze a claim against collected evidence.
"""

import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


class LLMAnalyzer:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-3.1-flash-lite"

    def analyze(
        self,
        claim: str,
        evidence: list,
        model_prediction: str,
        confidence: float
    ):

        evidence_text = "\n\n".join(
            [
                f"Title: {item.get('title')}\n"
                f"Source: {item.get('source')}\n"
                f"Published: {item.get('published_at')}\n"
                f"Content: {item.get('content')}\n"
                f"URL: {item.get('url')}"
                for item in evidence
            ]
        )

        prompt = f"""
You are a fact-checking assistant.

Claim:
{claim}

Local ML model prediction:
{model_prediction}

Local ML model confidence:
{confidence}

Evidence collected from web and news sources:

{evidence_text}

Analyze the claim using ONLY the provided evidence.

Return a JSON object:

{{
    "verdict": "true" | "false" | "uncertain",
    "explanation": "short explanation based on the evidence",
    "confidence": 0.0
}}

Rules:

1. Do not invent evidence.
2. Do not use information that is not supported by the provided evidence.
3. If evidence is insufficient or contradictory, return "uncertain".
4. Confidence must be between 0 and 1.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        text = response.text

        # Remove markdown code fences if Gemini returns them
        text = text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        result = json.loads(text)
