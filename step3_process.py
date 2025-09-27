import os
import difflib

# raw
RAW_FOLDER = "data/raw_cuad"
OUT_FOLDER = "data/processed_cuad"
os.makedirs(OUT_FOLDER, exist_ok=True)

# cat
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

def find_clauses(text, keywords):
    found = []
    text_lower = text.lower()
    for kw in keywords:
        kw_lower = kw.lower()
        # exact or fuzzy match
        if kw_lower in text_lower:
            found.append(kw)
        else:
            # fuzzy match threshold 0.75
            close_matches = difflib.get_close_matches(kw_lower, text_lower.split(), n=1, cutoff=0.75)
            if close_matches:
                found.append(kw)
    return list(set(found))

# Process each contract
for filename in os.listdir(RAW_FOLDER):
    if filename.endswith(".txt"):
        filepath = os.path.join(RAW_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        clauses = find_clauses(text, CLAUSE_KEYWORDS)

        # Save results
        outpath = os.path.join(OUT_FOLDER, filename.replace(".txt", "_clauses.txt"))
        with open(outpath, "w", encoding="utf-8") as f:
            f.write("Clauses found:\n")
            for c in clauses:
                f.write(f"- {c}\n")

        print(f" Processed {filename}: found {len(clauses)} clauses")

print(" All contracts processed ")
