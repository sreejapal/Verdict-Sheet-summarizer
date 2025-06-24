import os

pdf_root_folder = "data/train_files"
output_folder = "data/texts"
os.makedirs(output_folder, exist_ok=True)

print("✅ Folder found:", pdf_root_folder)

pdf_found = False  # To track if any PDFs are processed
pdf_count = 0  # Counter for processed PDFs
max_pdfs = 200  # Maximum number of PDFs to process

def extract_text_from_pdf(pdf_path):
    import fitz  # PyMuPDF
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"❌ Failed to extract text from {pdf_path}: {e}")
    return text

# Go inside all subfolders
for root, dirs, files in os.walk(pdf_root_folder):
    for file in files:
        if file.lower().endswith(".pdf"):
            if pdf_count >= max_pdfs:
                break  # Stop after 200 PDFs
            pdf_found = True
            pdf_path = os.path.join(root, file)

            try:
                full_text = extract_text_from_pdf(pdf_path)

                # Save as a .txt file
                relative_path = os.path.relpath(pdf_path, pdf_root_folder)
                safe_filename = relative_path.replace(os.sep, "_").replace(".PDF", ".txt")

                output_path = os.path.join(output_folder, safe_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_text)

                print(f"✅ Extracted: {pdf_path} -> {output_path}")
                pdf_count += 1  # Increment counter

            except Exception as e:
                print(f"❌ Failed to process {pdf_path}: {e}")
    if pdf_count >= max_pdfs:
        break  # Stop outer loop as well

if not pdf_found:
    print("⚠️ Still no PDF files found inside subfolders of:", pdf_root_folder)
