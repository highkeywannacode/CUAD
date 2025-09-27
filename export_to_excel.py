import os
import pandas as pd

PROCESSED_FOLDER = "data/processed_cuad"
EXCEL_FOLDER = "data/excel_exports"
os.makedirs(EXCEL_FOLDER, exist_ok=True)

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

records = []

for file in os.listdir(PROCESSED_FOLDER):
    if file.endswith("_clauses.txt"):
        filepath = os.path.join(PROCESSED_FOLDER, file)

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        found_clauses = [line.strip("- \n") for line in lines if line.startswith("-")]

        # Record for each clause with frequency count (0/1 now)
        for clause in CLAUSE_KEYWORDS:
            records.append({
                "contract": file.replace("_clauses.txt", ""),
                "clause": clause,
                "frequency": found_clauses.count(clause)
            })

df = pd.DataFrame(records)

# Pivot format (contracts x clauses, showing frequency)
df_pivot = df.pivot(index="contract", columns="clause", values="frequency")

# Add total clauses found column
df_pivot["Total Clauses Found"] = df_pivot.sum(axis=1)

# Save pivot table
excel_pivot = os.path.join(EXCEL_FOLDER, "contracts_clauses_pivot.xlsx")
df_pivot.to_excel(excel_pivot)
print(f"📊 Saved pivot table with frequency + totals to {excel_pivot}")
