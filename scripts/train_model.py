from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration, TrainingArguments, Trainer
import torch

# Load dataset
dataset = load_dataset("csv", data_files={"train": "./data/train.csv"})
dataset = dataset["train"].train_test_split(test_size=0.1)

# Tokenizer and model
model_name = "facebook/bart-base"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Tokenization function
def tokenize(batch):
    inputs = tokenizer(batch["text"], max_length=1024, truncation=True, padding="max_length")
    outputs = tokenizer(batch["summary"], max_length=128, truncation=True, padding="max_length")
    inputs["labels"] = outputs["input_ids"]
    return inputs

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text", "summary"])

# Training args
args = TrainingArguments(
    output_dir="./my_custom_summarizer",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    logging_dir="./logs",
    save_total_limit=2,
    save_strategy="epoch",
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"]
)

# Train
trainer.train()
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")
print("✅ Model training complete and saved to './model'")