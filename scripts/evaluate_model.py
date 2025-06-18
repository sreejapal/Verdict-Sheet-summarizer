import os
from transformers import BartTokenizer, BartForConditionalGeneration
from evaluate import load

# Load ROUGE metric
rouge = load("rouge")

# Paths
model_path = "./model"
texts_folder = "./data/texts"
gold_summaries_folder = "./data/structured_summaries"
predicted_summaries_folder = "./data/generated_summaries"

# Create folder if not exists
os.makedirs(predicted_summaries_folder, exist_ok=True)

# Load tokenizer and model
tokenizer = BartTokenizer.from_pretrained(model_path)
model = BartForConditionalGeneration.from_pretrained(model_path)

# Helper function to generate summary
def generate_summary(text):
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=300, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Lists to store gold and predicted summaries
gold_summaries = []
predicted_summaries = []

# Loop through text files
for filename in os.listdir(texts_folder):
    if filename.endswith(".txt"):
        base_name = filename.replace(".txt", "")
        text_path = os.path.join(texts_folder, filename)
        gold_summary_path = os.path.join(gold_summaries_folder, base_name + "_summary.txt")

        # Print paths for debugging
        print(f"🔍 Checking summary for: {filename}")

        # Skip if no gold summary exists
        if not os.path.exists(gold_summary_path):
            print(f"⚠️ Skipped (no summary): {gold_summary_path}")
            continue

        # Read text and gold summary
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read()

        with open(gold_summary_path, "r", encoding="utf-8") as f:
            gold_summary = f.read()

        # Generate model summary
        predicted_summary = generate_summary(text)

        # Save predicted summary (optional)
        predicted_file_path = os.path.join(predicted_summaries_folder, base_name + "_predicted.txt")
        with open(predicted_file_path, "w", encoding="utf-8") as f:
            f.write(predicted_summary)

        # Append to lists for evaluation
        gold_summaries.append(gold_summary)
        predicted_summaries.append(predicted_summary)

# Evaluate using ROUGE
if gold_summaries and predicted_summaries:
    results = rouge.compute(predictions=predicted_summaries, references=gold_summaries)
    print("\n📊 Evaluation Results (ROUGE scores):")
    for key, value in results.items():
        print(f"{key}: {value:.4f}")
else:
    print("⚠️ No valid summaries to evaluate.")
