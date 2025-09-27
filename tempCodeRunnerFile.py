import os
import pandas as pd

# Folders
processed_folder = "data/processed_cuad/"
output_excel_long = "data/processed_cuad/contracts_clauses_long.xlsx"
output_excel_pivot = "data/processed_cuad/contracts_clauses_pivot.xlsx"

results = []  # store rows

# Loop through all processed text files
for file in os.listdir(processed_folder):
    if file.endswith(".txt"):
        contract_name = file.replace(".txt", "")
        filepath = os.path.join(processed_folder, file)

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Extract clause info
        for line in lines:
            if line.startswith("Clause:"):
                parts = line.strip().split("->")
                if len(parts) == 2:
                    clause = parts[0].replace("Clause:", "").strip()
                    found_status = parts[1].strip()
                else:
                    clause = parts[0].replace("Clause:", "").strip()
                    found_status = "UNKNOWN"

                results.append({
                    "contract": contract_name,
                    "clause": clause,
                    "found": found_status
                })

# ✅ Make sure we got something
if not results:
    raise ValueError("⚠️ No clause data extracted. Check your processed files format.")

# ✅ Long format
df_long = pd.DataFrame(results)
df_long.to_excel(output_excel_long, index=False)
print(f"📊 Saved detailed results to {output_excel_long}")

# ✅ Pivot format
df_pivot = df_long.copy()
if "found" in df_pivot.columns:
    df_pivot["found_binary"] = df_pivot["found"].apply(lambda x: 1 if "FOUND" in x.upper() else 0)

    pivot_table = df_pivot.pivot_table(
        index="contract",
        columns="clause",
        values="found_binary",
        aggfunc="max",
        fill_value=0
    ).reset_index()

    pivot_table.to_excel(output_excel_pivot, index=False)
    print(f"📊 Saved pivoted results to {output_excel_pivot}")
else:
    print("⚠️ No 'found' column available, skipping pivot table.")
