import os
import shutil

source_folder = r"C:\Users\Dell\Downloads\dresses"
target_folder = r"C:\Users\Dell\Desktop\AI-Fashion-Advisor\AI-Fashion-Advisor\frontend\images\dress_examples"

os.makedirs(target_folder, exist_ok=True)

# put your downloaded filenames on the left
# put required project filenames on the right
mapping = {
    "img1.png": "a_line_kurti.png",
    "img2.png": "anarkali.png",
    "img3.png": "jacket_kurti.png",
    "img4.png": "wrap_dress.png",
    "img5.png": "fit_flare_dress.png",
    "img6.png": "skater_dress.png",
    "img7.png": "party_gown.png",
    "img8.png": "soft_saree.png"
}

for old_name, new_name in mapping.items():
    old_path = os.path.join(source_folder, old_name)
    new_path = os.path.join(target_folder, new_name)

    if os.path.exists(old_path):
        shutil.copy(old_path, new_path)
        print(f"Copied: {old_name} -> {new_name}")
    else:
        print(f"Missing: {old_name}")

print("Done.")