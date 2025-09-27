from datasets import load_dataset
import os
import pdfplumber
import io


OUT_FOLDER = "data/markdown_cuad"
os.makedirs(OUT_FOLDER, exist_ok=True)


CLAUSE_KEYWORDS = [
    "Affiliate License/Trademark",
    "Anti-assignment",
    "Anti-diversion",
    "Anti-sandbagging",
    "Audit Rights",
    "Change of Control",
    "Confidentiality",
    "Covenant Not to Sue",
    "Covenants",
    "Dispute Resolution",
    "Exclusivity",
    "Expansion Options",
    "Financial Obligations",
    "Force Majeure",
    "Governing Law",
    "Indemnification",
    "Insurance",
    "Intellectual Property",
    "Joint IP Ownership",
    "License Grant",
    "Liquidated Damages",
    "Most Favored Nation",
    "Non-compete",
    "Non-disparagement",
    "Notice Period",
    "Option to Renew/Extend",
    "Payment Terms",
    "Publicity",
    "Remedies",
    "Representations & Warranties",
    "Restrictive Covenants",
    "Right of First Offer",
    "Right of First Refusal",
    "Source Code Escrow",
    "Standstill",
    "Subcontracting",
    "Termination",
    "Termination for Convenience",
    "Use of Name/Logo",
    "Waiver"
]


dataset = load_dataset("TheAtticusProject/cuad", split="train", streaming=True)


def highlight_keywords(text, keywords):
    for kw in keywords:
        text = text.replace(kw, f"**{kw}**")
        text = text.replace(kw.lower(), f"**{kw.lower()}**")
    return text

for i, example in enumerate(dataset):
    if i >= 12:
        break

    # raww PDF bytes from huggingface
    pdf_bytes = example["pdf"]["bytes"]
    pdf_stream = io.BytesIO(pdf_bytes)

    outpath = os.path.join(OUT_FOLDER, f"contract_{i+1}.md")

    with pdfplumber.open(pdf_stream) as pdf, open(outpath, "w", encoding="utf-8") as f:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = highlight_keywords(text, CLAUSE_KEYWORDS)

            # Markdown 
            f.write(f"# Page {page_num}\n")
            f.write(text + "\n\n")
            f.write("---\n\n")

    print(f"Saved {outpath}")

print("FINALLY saved in data/markdown_cuad/")

