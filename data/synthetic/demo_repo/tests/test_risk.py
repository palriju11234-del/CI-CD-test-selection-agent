from app.risk.risk import RiskAssessment


def test_low_risk_when_high_confidence():
    risk = RiskAssessment(threshold=0.95)
    result = risk.assess(label="true", confidence=0.95)
    assert result == "LOW_RISK"


def test_high_risk_when_low_confidence():
    risk = RiskAssessment(threshold=0.95)
    result = risk.assess(label="true", confidence=0.82)
    assert result == "HIGH_RISK"


def test_high_risk_when_uncertain_label():
    risk = RiskAssessment(threshold=0.95)
    result = risk.assess(label="uncertain", confidence=0.99)
    assert result == "HIGH_RISK"


def test_high_risk_when_below_threshold():
    risk = RiskAssessment(threshold=0.95)
    result = risk.assess(label="false", confidence=0.79)
    assert result == "HIGH_RISK"


def test_low_risk_exactly_at_threshold():
    risk = RiskAssessment(threshold=0.80)
    result = risk.assess(label="true", confidence=0.80)
    assert result == "LOW_RISK"