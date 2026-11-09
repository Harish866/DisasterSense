
import re


NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}


def split_sentences(description):
    """Split text into simple sentence-like units."""
    return [
        sentence.strip()
        for sentence in re.split(
            r"(?<=[.!?;])\s+",
            description,
        )
        if sentence.strip()
    ]


def is_negated(sentence, match_start):
    """
    Detect nearby negation before a positive keyword.

    This is a basic pattern-based check, not full
    natural-language understanding.
    """
    preceding_text = sentence[:match_start]

    return bool(
        re.search(
            r"\b(?:no|not|never|without|neither)\b"
            r"(?:\W+\w+){0,3}\W*$",
            preceding_text,
        )
    )


def find_status(description, positive_patterns, negative_patterns):
    """
    Return:
        True  = positive evidence found
        False = explicit negative evidence found
        None  = no clear evidence found

    A negated positive keyword is not automatically treated
    as explicit evidence that the condition is absent.
    """

    positive_found = False
    negative_found = False

    for sentence in split_sentences(description):

        # Check explicit negative statements.
        for pattern in negative_patterns:
            if re.search(pattern, sentence):
                negative_found = True
                break

        # Check positive evidence that is not negated.
        for pattern in positive_patterns:
            for match in re.finditer(pattern, sentence):

                if not is_negated(sentence, match.start()):
                    positive_found = True
                    break

            if positive_found:
                break

    if positive_found:
        return True

    if negative_found:
        return False

    return None


def extract_injured_count(description):
    """Extract a simple numeric or number-word injury count."""

    number_pattern = (
        r"(\d+|"
        + "|".join(NUMBER_WORDS.keys())
        + r")"
    )

    patterns = [
        number_pattern
        + r"\s+(?:people\s+)?(?:are\s+)?injured\b",

        number_pattern + r"\s+injuries\b",

        r"injured\s+(?:people\s+)?[:=]\s*"
        + number_pattern,

        r"injuries\s*[:=]\s*"
        + number_pattern,

        r"(?:injured|injury)\s+count\s*[:=]\s*"
        + number_pattern,
    ]

    for pattern in patterns:
        match = re.search(pattern, description)

        if match:
            value = match.group(1)

            if value.isdigit():
                return int(value)

            return NUMBER_WORDS.get(value)

    return None


def extract_information(description):

    if not isinstance(description, str) or not description.strip():
        raise ValueError(
            "Incident description cannot be empty."
        )

    text = description.lower().strip()

    # --------------------------------------------------
    # 1. PEOPLE TRAPPED
    # --------------------------------------------------

    people_trapped = find_status(
        text,
        [
            r"\btrapped\b",
            r"\bburied\b",
            r"\bstuck inside\b",
            r"\bunable to escape\b",
            r"\bpeople are stuck\b",
        ],
        [
            r"\bno (?:one|people|person) "
            r"(?:is |are )?trapped\b",
            r"\bnot trapped\b",
            r"\bno one is buried\b",
            r"\bno people are buried\b",
            r"\bno one is stuck\b",
        ],
    )

    # --------------------------------------------------
    # 2. INJURIES
    # --------------------------------------------------

    injuries_reported = find_status(
        text,
        [
            r"\binjured\b",
            r"\binjuries\b",
            r"\bwounded\b",
            r"\bcasualties\b",
            r"\bsevere bleeding\b",
        ],
        [
            r"\bno injuries\b",
            r"\bno one is injured\b",
            r"\bno people are injured\b",
            r"\bno casualties\b",
            r"\bno one is hurt\b",
            r"\bno one was hurt\b",
            r"\bnot injured\b",
        ],
    )

    injured_count = extract_injured_count(text)

    # A positive injury count confirms reported injuries.
    if injured_count is not None and injured_count > 0:
        injuries_reported = True

    elif injured_count == 0 and injuries_reported is None:
        injuries_reported = False

    # --------------------------------------------------
    # 3. RESCUE REQUIRED
    # --------------------------------------------------

    rescue_required = find_status(
        text,
        [
            r"\brescue (?:teams?|workers?|operation|operations)"
            r"(?:\s+\w+){0,3}\s+(?:needed|required|requested)\b",

            r"\bneed(?:s|ed)? rescue\b",
            r"\brescue is required\b",
            r"\brescue is urgently needed\b",
            r"\bpeople need rescuing\b",
            r"\bemergency rescue\b",
            r"\btrapped\b",
            r"\bburied\b",
        ],
        [
            r"\bno rescue (?:is )?(?:needed|required)\b",
            r"\brescue is not required\b",
            r"\bno rescue operation needed\b",
        ],
    )

    # --------------------------------------------------
    # 4. EVACUATION REQUIRED
    # --------------------------------------------------

    evacuation_required = find_status(
        text,
        [
            r"\bevacuate\b",
            r"\bevacuates?\b",
            r"\bevacuation\b",
            r"\bevacuating\b",

            r"\bevacuations?\s+(?:are\s+)?"
            r"(?:needed|required|ordered|requested)\b",

            r"\bevacuations?\s+(?:is\s+)?"
            r"(?:necessary|mandatory)\b",

            r"\bevacuations?\s+(?:must|should)\s+"
            r"(?:be\s+)?(?:carried out|conducted)\b",

            r"\bpeople must leave\b",
            r"\bmove people to safety\b",
        ],
        [
            r"\bno evacuation (?:is )?(?:needed|required)\b",
            r"\bevacu(?:ation|ate) is not required\b",
            r"\bno need to evacuate\b",
            r"\bevacuations? (?:are )?not necessary\b",
        ],
    )

    # --------------------------------------------------
    # 5. BUILD INTELLIGENCE SUMMARY
    # --------------------------------------------------

    findings = []

    def describe_status(label, value):
        if value is True:
            findings.append(f"{label}: Yes")

        elif value is False:
            findings.append(f"{label}: No")

        else:
            findings.append(f"{label}: Unknown")

    describe_status(
        "People trapped",
        people_trapped,
    )

    describe_status(
        "Injuries reported",
        injuries_reported,
    )

    if injured_count is not None:
        findings.append(
            f"Injured count: {injured_count}"
        )
    else:
        findings.append(
            "Injured count: Unknown"
        )

    describe_status(
        "Rescue required",
        rescue_required,
    )

    describe_status(
        "Evacuation required",
        evacuation_required,
    )

    # --------------------------------------------------
    # 6. RETURN EXTRACTED INFORMATION
    # --------------------------------------------------

    return {
        "people_trapped": people_trapped,
        "injuries_reported": injuries_reported,
        "injured_count": injured_count,
        "rescue_required": rescue_required,
        "evacuation_required": evacuation_required,
        "summary": "\n".join(findings),
    }
