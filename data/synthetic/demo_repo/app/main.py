from fastapi import FastAPI
from urllib.parse import unquote

from app.cache.cache import get, save
from app.ml.model import FactCheckModel
from app.risk.risk import RiskAssessment
from app.search.search import SearchEngine
from app.evidence.extractor import EvidenceExtractor
from app.llm.analyze import LLMAnalyzer


app = FastAPI()


# Initialize modules
model = FactCheckModel()
risk_assessor = RiskAssessment()
search_engine = SearchEngine()
evidence_extractor = EvidenceExtractor()
llm_analyzer = LLMAnalyzer()


@app.get("/")
def home():
    return {
        "message": "AI Fact Verification Engine is running!"
    }


@app.get("/verify")
def verify_claim(claim: str):

    # 1. Check cache
    cached_result = get(claim)

    if cached_result:
        return {
            "source": "cache",
            "result": cached_result
        }

    # 2. Get prediction from ML model
    prediction = model.predict(claim)

    label = prediction["label"]
    confidence = prediction["confidence"]

    # 3. Risk assessment
    risk = risk_assessor.assess(label, confidence)
    
    # 4. If confidence is high, return directly
    if risk == "LOW_RISK":

        result = {
            "claim": claim,
            "verdict": label,
            "confidence": confidence,
            "risk": risk,
            "source": "local_model"
        }

        save(claim, result)

        return result

    # 5. If confidence is low, search for evidence
    search_results = search_engine.search(claim)

    # 6. Extract evidence
    evidence = evidence_extractor.extract(search_results)

    # 7. Analyze evidence with LLM
    final_result = llm_analyzer.analyze(
        claim=claim,
        evidence=evidence,
        model_prediction=label,
        confidence=confidence
    )

    final_result["risk"] = risk
    final_result["source"] = "web_search_and_llm"

    # 8. Save final result in cache
    save(claim, final_result)

    return final_result