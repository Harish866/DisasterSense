
from ml_models.information_extractor import extract_information


test_reports = [
    (
        "A building has collapsed. Several people are trapped "
        "inside, three are injured, and rescue teams are urgently needed."
    ),
    (
        "A fire broke out in a warehouse. No one is trapped "
        "and no injuries have been reported."
    ),
    (
        "Flood water is rising rapidly near residential houses."
    ),
    (
        "Four people are injured after a road accident. "
        "Evacuation is required."
    ),
]


for index, report in enumerate(test_reports, start=1):

    print("\n" + "=" * 60)
    print(f"TEST REPORT {index}")
    print("=" * 60)

    print("Description:")
    print(report)

    result = extract_information(report)

    print("\nExtracted Intelligence:")
    print(result["summary"])

    print("\nRaw Result:")
    print(result)
