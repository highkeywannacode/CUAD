from datasets import load_dataset
import os
import pdfplumber

print("Loading CUAD in streaming mode (PDFs)...")
dataset = load_dataset("TheAtticusProject/cuad", split="train", streaming=True)



#  12 contracts
for i, example in enumerate(dataset):
    pdf_obj = example["pdf"]  # pdfplumber PDF object

    # Extract text
    text_content = ""
    for page in pdf_obj.pages:
        text_content += page.extract_text() or ""  # add each page's text

    # Save each contract into a .txt file
    with open(f"data/raw_cuad/contract_{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(text_content)

    print(f"\n Saved contract_{i+1}.txt with {len(text_content)} characters")

    if i == 11:  
        break

print("\n 12 contracts saved in data")
