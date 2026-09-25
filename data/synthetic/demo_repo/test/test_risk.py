from app.risk.risk import RiskAssessment

risk = RiskAssessment()

print(risk.assess(0.95))
print(risk.assess(0.82))
print(risk.assess(0.79))
print(risk.assess(0.32))