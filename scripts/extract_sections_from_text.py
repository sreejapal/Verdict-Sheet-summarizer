import re
import sys

# Define section headings and their variants
SECTION_HEADINGS = [
    ("Title", [r"case\s+title", r"title", r"case\s*name"]),
    ("Citation", [r"citation", r"citations?"]),
    ("Court", [r"in the\s+supreme court", r"supreme court", r"high court", r"court of [\w\s]+", r"tribunal", r"bench"]),
    ("Date of Judgement", [r"date of (?:judgment|judgement|order)", r"judgment date", r"date"]),
    ("Bench", [r"bench", r"coram", r"justices?"]),
    ("Parties Involved", [r"parties involved", r"appellant[s]?:", r"respondent[s]?:", r"petitioner[s]?:", r"defendant[s]?:", r"plaintiff[s]?:"]),
    ("Background / Facts of the Case", [r"facts", r"background", r"factual background", r"case background", r"facts of the case"]),
    ("Legal Issues", [r"legal issues?", r"issues? for consideration", r"questions? of law", r"points for determination"]),
    ("Judgement / Holding", [r"judgment", r"judgement", r"holding", r"decision", r"order"]),
    ("Judgement", [r"final judgment", r"final judgement", r"order"]),
    ("Case Timeline", [r"timeline", r"chronology", r"case timeline"]),
    ("Relevant Legal Provisions & Articles", [r"relevant legal provisions", r"provisions", r"articles", r"sections"]),
    ("Conclusion", [r"conclusion", r"summary", r"final remarks"]),
]

SECTION_NAMES = [name for name, _ in SECTION_HEADINGS]

# Build a regex to match any section heading
HEADING_REGEX = re.compile(r"^\s*(%s)\s*[:\-]?\s*$" % "|".join(
    [variant for _, variants in SECTION_HEADINGS for variant in variants]
), re.IGNORECASE | re.MULTILINE)

def extract_sections_with_context(text):
    # Find all section headings and their positions
    headings = []
    for i, (section, variants) in enumerate(SECTION_HEADINGS):
        for variant in variants:
            for match in re.finditer(r"^\s*(%s)\s*[:\-]?\s*$" % variant, text, re.IGNORECASE | re.MULTILINE):
                headings.append((match.start(), match.end(), section))
    # Sort by position
    headings.sort()
    # Extract content for each section
    output = {}
    for idx, (start, end, section) in enumerate(headings):
        next_start = headings[idx + 1][0] if idx + 1 < len(headings) else len(text)
        content = text[end:next_start].strip()
        if section not in output or len(content) > len(output[section]):
            output[section] = content
    # Fill missing sections with 'Not found'
    for section, _ in SECTION_HEADINGS:
        if section not in output:
            output[section] = "Not found"
    return output

def format_sections_dict(sections_dict):
    result = []
    for section, _ in SECTION_HEADINGS:
        value = sections_dict.get(section, "Not found")
        result.append(f"{section}:\n{value}\n")
    return "\n".join(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    sections = extract_sections_with_context(text)
    print(format_sections_dict(sections))

# For import
extract_all_sections = extract_sections_with_context
format_sections = format_sections_dict 