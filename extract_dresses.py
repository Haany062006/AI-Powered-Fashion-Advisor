import zipfile
import shutil
from pathlib import Path
import re

# 👇 CHANGE THIS PATH if needed
ZIP_FILE = Path(r"C:\Users\Dell\Downloads\dress-dataset.zip")

# Project folder (auto-detect)
PROJECT_ROOT = Path(__file__).resolve().parent

# Where images will go
TARGET_ROOT = PROJECT_ROOT / "frontend" / "images" / "dresses"

def slugify(name: str) -> str:
    name = Path(name).stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
    return name + ".png"

if not ZIP_FILE.exists():
    raise FileNotFoundError(f"Zip file not found: {ZIP_FILE}")

print("📦 Extracting from Downloads...")

# Clear old images
if TARGET_ROOT.exists():
    shutil.rmtree(TARGET_ROOT)

TARGET_ROOT.mkdir(parents=True, exist_ok=True)

count = 0

with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
    for member in zip_ref.namelist():

        if member.endswith("/") or not member.lower().endswith(".png"):
            continue

        parts = Path(member).parts

        if len(parts) < 2:
            continue

        category = parts[-2].lower()
        original_name = parts[-1]
        clean_name = slugify(original_name)

        category_folder = TARGET_ROOT / category
        category_folder.mkdir(parents=True, exist_ok=True)

        temp_path = zip_ref.extract(member, PROJECT_ROOT / "_temp_extract")
        final_path = category_folder / clean_name

        shutil.move(temp_path, final_path)
        count += 1

# Remove temp folder
shutil.rmtree(PROJECT_ROOT / "_temp_extract", ignore_errors=True)

print(f"✅ Done! {count} images copied to:")
print(TARGET_ROOT)