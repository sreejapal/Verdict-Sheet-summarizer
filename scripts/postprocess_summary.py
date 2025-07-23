import re
import sys
from typing import List

# Define the required sections in order
SECTIONS = [
    "Title",
    "Citation",
    "Court",
    "Date of Judgement",
    "Bench",
    "Parties Involved",
    "Background / Facts of the Case",
    "Legal Issues",
    "Judgement / Holding",
    "Judgement",
    "Case Timeline",
    "Relevant Legal Provisions & Articles",
    "Conclusion"
]

SECTION_PATTERN = re.compile(r"^(%s):" % "|".join([re.escape(s) for s in SECTIONS]), re.MULTILINE)

def split_sections(text: str) -> dict:
    """Split the summary into sections based on headings."""
    matches = list(SECTION_PATTERN.finditer(text))
    sections = {}
    for i, match in enumerate(matches):
        section = match.group(1)
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections[section] = content
    return sections

def postprocess_summary(summary: str) -> str:
    """Ensure all sections are present and in order, fill missing with 'Not found'."""
    sections = split_sections(summary)
    output = []
    for section in SECTIONS:
        output.append(f"{section}:")
        content = sections.get(section, "Not found")
        output.append(content)
        output.append("")
    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Read summary from file
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            summary = f.read()
    else:
        # Read summary from stdin
        summary = sys.stdin.read()
    cleaned = postprocess_summary(summary)
    print(cleaned) 