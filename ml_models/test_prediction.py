
from predict import predict_incident

test_reports = [
    "Heavy rainfall has flooded several streets and trapped residents.",
    "A building is burning and thick smoke is spreading.",
    "Several people are injured in a road collision.",
    "A strong earthquake has damaged houses and buildings.",
    "A person is unconscious and needs immediate medical assistance.",
]

for report in test_reports:
    result = predict_incident(report)

    print("\nReport:", report)
    print("AI prediction:", result["predicted_type"])
    print("Model score:", f'{result["model_score"] * 100:.2f}%')
