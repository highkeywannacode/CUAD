import os

FOLDER = "data/processed_cuad"

for file in os.listdir(FOLDER):
    if "summary" in file.lower():
        path = os.path.join(FOLDER, file)
        os.remove(path)
        print(f" Deleted {path}")

print(" Cleaned all summary files")
