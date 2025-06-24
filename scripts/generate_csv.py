import os
import pandas as pd
from docx import Document
import re

# Folder paths
texts_folder = "./data/texts"
summaries_folder = "./data/structured_summaries"
output_csv = "./data/train.csv"

# Convert Word summaries to plain text if needed
word_summary_dir = "./data/train_summaries"
plain_summary_dir = summaries_folder
os.makedirs(plain_summary_dir, exist_ok=True)
for fname in os.listdir(word_summary_dir):
    if fname.endswith(".docx"):
        docx_path = os.path.join(word_summary_dir, fname)
        txt_name = fname.replace(".docx", ".txt")
        txt_path = os.path.join(plain_summary_dir, txt_name)
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Converted {fname} to {txt_name}")

def normalize_name(name):
    # Remove extension, underscores, '_summary', and lower the case
    base = os.path.splitext(name)[0]
    base = re.sub(r'_summary', '', base, flags=re.IGNORECASE)
    return re.sub(r'[_\W]+', '', base).lower()

data = []
max_pairs = 200  # Maximum number of pairs to process
pair_count = 0

# List all files from texts folder
text_files = sorted([f for f in os.listdir(texts_folder) if f.endswith(".pdf") or f.endswith(".txt")])
summary_files = sorted([f for f in os.listdir(summaries_folder) if f.endswith(".txt")])

# Build a mapping from normalized summary base name to filename
summary_map = {normalize_name(f): f for f in summary_files}

for filename in text_files:
    if pair_count >= max_pairs:
        break
    text_path = os.path.join(texts_folder, filename)
    base_norm = normalize_name(filename)
    # Try to find a matching summary
    summary_filename = summary_map.get(base_norm)
    if summary_filename:
        summary_path = os.path.join(summaries_folder, summary_filename)
        with open(text_path, "r", encoding="utf-8") as tf, open(summary_path, "r", encoding="utf-8") as sf:
            text = tf.read().strip()
            summary = sf.read().strip()
            if text and summary:
                data.append({"text": text, "summary": summary})
                pair_count += 1
            else:
                print(f"⚠️ Skipping empty content in: {filename}")
    else:
        print(f"❌ Summary not found for: {filename}")

# Save to CSV
if data:
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"✅ CSV saved! {len(df)} valid rows in train.csv")
else:
    print("❌ No valid text-summary pairs found.")
