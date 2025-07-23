import os
import re

# Directories
pdf_dir = 'data/train_files'
docx_dir = 'data/train_summaries'

# Regex to extract case name and year from PDF filenames
pdf_pattern = re.compile(r'^(.*?)(_on_)?(\d{1,2}_\w+_\d{4}|\d{4})')

# Helper to normalize case name

def normalize_case_name(name):
    # Remove trailing underscores, numbers, and extra suffixes
    name = re.sub(r'_on_\d{1,2}_\w+_\d{4}', '', name)
    name = re.sub(r'_\d{4}$', '', name)
    name = re.sub(r'_1$', '', name)
    name = name.replace('__', '_')
    return name.strip('_')

# Step 1: Rename PDFs
pdf_renames = []
for fname in os.listdir(pdf_dir):
    if not fname.lower().endswith('.pdf'):
        continue
    base = fname[:-4]
    # Try to extract year
    m = re.search(r'(\d{4})', base)
    if not m:
        print(f"Skipping {fname}: no year found")
        continue
    year = m.group(1)
    # Remove trailing _on_date or _1
    case_name = normalize_case_name(base)
    new_name = f"{case_name}_{year}.pdf"
    src = os.path.join(pdf_dir, fname)
    dst = os.path.join(pdf_dir, new_name)
    if fname != new_name:
        os.rename(src, dst)
        pdf_renames.append((fname, new_name))
    else:
        pdf_renames.append((fname, fname))

# Step 2: Rename DOCX summaries
# Try to match to the new PDF names
for fname in os.listdir(docx_dir):
    if not fname.lower().endswith('.docx'):
        continue
    base = fname[:-5]
    # Try to extract year
    m = re.search(r'(\d{4})', base)
    if not m:
        print(f"Skipping {fname}: no year found")
        continue
    year = m.group(1)
    # Remove trailing _Summary, _Final, etc.
    case_name = re.sub(r'_Summary.*$', '', base, flags=re.IGNORECASE)
    case_name = re.sub(r'_Legal_Summary.*$', '', case_name, flags=re.IGNORECASE)
    case_name = re.sub(r'_SupremeCourtSummary.*$', '', case_name, flags=re.IGNORECASE)
    case_name = re.sub(r'_Case_Summary.*$', '', case_name, flags=re.IGNORECASE)
    case_name = re.sub(r'_Final$', '', case_name, flags=re.IGNORECASE)
    case_name = re.sub(r'_summary$', '', case_name, flags=re.IGNORECASE)
    case_name = case_name.replace('__', '_')
    case_name = case_name.strip('_')
    new_name = f"{case_name}_{year}_summary.docx"
    src = os.path.join(docx_dir, fname)
    dst = os.path.join(docx_dir, new_name)
    if fname != new_name:
        os.rename(src, dst)
        print(f"Renamed: {fname} -> {new_name}")
    else:
        print(f"Unchanged: {fname}")

print("\nPDF Renames:")
for old, new in pdf_renames:
    print(f"{old} -> {new}") 