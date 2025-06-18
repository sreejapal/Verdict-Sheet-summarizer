import os
import re
from transformers import pipeline

# Load BART summarizer model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# --- Extract case metadata ---
def extract_case_info(text):
    case_title_match = re.search(r'(.+vs\.?.+?)\s+on\s+\d{1,2}\s+\w+,\s+\d{4}', text)
    case_title = case_title_match.group(1) if case_title_match else "Not found"

    date_match = re.search(r'on\s+(\d{1,2}\s+\w+,\s+\d{4})', text)
    date = date_match.group(1) if date_match else "Not found"

    citations = ", ".join(re.findall(r'[A-Z][\w().,\s-]{5,}', text))[:150] or "Not found"

    jury_matches = re.findall(r'(?:Justice|Judge)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?', text)
    jury_set = set(jury_matches)
    jury_count = len(jury_set)

    return case_title, date, citations, jury_set, jury_count

# --- Extract structured summary sections ---
def extract_summary_sections(text):
    prompt = f"""
Summarize the following legal case by extracting:
1. Key Facts
2. Legal Issue

Format:
Facts: ...
Issue: ...
"""
    input_text = prompt + "\n" + text[:1024]
    summary = summarizer(input_text, max_length=300, min_length=100, do_sample=False)[0]['summary_text']
    return summary

# --- Extract final verdict using keyword patterns ---
def extract_verdict(text):
    verdict_patterns = [
        r"petition (is )?dismissed",
        r"appeal (is )?allowed",
        r"in favor of (the )?(petitioner|respondent|defendant|plaintiff)",
        r"case (is )?closed",
        r"detention (is )?upheld",
        r"conviction (is )?quashed",
        r"granted (bail|release)",
        r"acquitted",
        r"guilty"
    ]
    for pattern in verdict_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).capitalize()
    return "Not clearly mentioned"

# --- Final output format ---
def create_structured_summary(text):
    title, date, citations, jury, jury_count = extract_case_info(text)
    summary = extract_summary_sections(text)
    verdict = extract_verdict(text)

    return f"""Case Title: {title}
Date: {date}
Equivalent Citations: {citations}
Jury Members Count: {jury_count}
Jury Members: {', '.join(jury) if jury else 'Not found'}

Summary:
{summary}

Final Verdict (extracted): {verdict}
"""

# --- Process multiple text files ---
input_folder = "./data/texts"
output_folder = "./data/structured_summaries"
os.makedirs(output_folder, exist_ok=True)

processed = 0
for file_name in sorted(os.listdir(input_folder)):
    if file_name.endswith(".txt") and processed < 200:
        file_path = os.path.join(input_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            case_text = f.read()

        structured = create_structured_summary(case_text)
        out_path = os.path.join(output_folder, file_name.replace(".txt", "_summary.txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(structured)

        print(f"✅ Saved: {file_name}")
        processed += 1

print(f"✅ Done. {processed} summaries saved to structured_summaries/")
