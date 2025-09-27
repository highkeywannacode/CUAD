import os
from datasets import load_dataset
from docling_parse.pdf_parser import pdf_parser  # ✅ correct import for docling

# Output folder
OUT_FOLDER = "data/raw_cuad_docling"
os.makedirs(OUT_FOLDER, exist_ok=True)

print("Loading CUAD in streaming mode (PDFs with Docling)...")

# Load CUAD dataset in streaming mode
dataset = load_dataset("TheAtticusProject/cuad", split="train", streaming=True)

count = 0

for example in dataset:
    pdf_file = example["pdf"]

    # Get local file path
    pdf_path = pdf_file.path  

    # Parse with Docling
    parsed_doc = pdf_parser.parse(pdf_path)
    text = parsed_doc.text

    # Save
    count += 1
    outpath = os.path.join(OUT_FOLDER, f"contract_{count}.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Saved contract_{count}.txt with {len(text)} characters")

    if count >= 12:  # limit for testing
        break

print(f"🎉 Done! {count} contracts saved in {OUT_FOLDER}")
