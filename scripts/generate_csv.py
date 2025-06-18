import os
import pandas as pd

# Folder paths
texts_folder = "./data/texts"
summaries_folder = "./data/structured_summaries"
output_csv = "./data/train.csv"

data = []
max_pairs = 200  # Maximum number of pairs to process
pair_count = 0

# List all .txt files from texts folder
text_files = sorted([f for f in os.listdir(texts_folder) if f.endswith(".txt")])

for filename in text_files:
    if pair_count >= max_pairs:
        break
    text_path = os.path.join(texts_folder, filename)
    
    # summary file should follow the same filename pattern with _summary added before .txt
    summary_filename = filename.replace(".txt", "_summary.txt")
    summary_path = os.path.join(summaries_folder, summary_filename)

    if os.path.exists(summary_path):
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
