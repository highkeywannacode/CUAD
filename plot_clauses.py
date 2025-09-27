import os
import pandas as pd
import matplotlib.pyplot as plt


EXCEL_FOLDER = "data/excel_exports"
files = [f for f in os.listdir(EXCEL_FOLDER) if f.startswith("contracts_clauses_pivot")]
latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(EXCEL_FOLDER, f)))
excel_path = os.path.join(EXCEL_FOLDER, latest_file)

print(f" Using {excel_path}")


df_pivot = pd.read_excel(excel_path, index_col=0)


plt.figure(figsize=(12, 6))
df_pivot["Total Clauses Found"].plot(kind="bar", color="skyblue")

plt.title("Clauses Found per Contract")
plt.xlabel("Contract")
plt.ylabel("Number of Clauses Found")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()
