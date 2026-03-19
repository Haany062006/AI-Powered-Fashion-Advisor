from PIL import Image, ImageDraw
import os

# Folder where images will be saved
output_dir = os.path.join("frontend", "images", "dress_examples")
os.makedirs(output_dir, exist_ok=True)

dress_files = [
"a_line_dress.jpg",
"wrap_dress.jpg",
"high_waist_skirt.jpg",
"fit_flare_dress.jpg",
"off_shoulder_skirt.jpg",
"structured_jacket_dress.jpg",
"anarkali.jpg",
"a_line_kurti.jpg",
"flared_lehenga.jpg",
"jacket_kurti.jpg",
"pleated_salwar.jpg",
"soft_saree.jpg",
"high_waist_jeans.jpg",
"peplum_top_pants.jpg",
"casual_midi.jpg",
"skater_dress.jpg",
"wide_leg_pants.jpg",
"shrug_tank_jeans.jpg",
"one_shoulder_dress.jpg",
"ruffle_dress.jpg",
"sequin_a_line.jpg",
"party_gown.jpg",
"embellished_lehenga.jpg",
"cocktail_wrap.jpg",
"empire_waist_dress.jpg",
"v_neck_dress.jpg",
"straight_fit_dress.jpg",
"flowy_tunic.jpg",
"a_line_top_jeans.jpg",
"blazer_dress.jpg",
"straight_kurti.jpg",
"empire_cut_kurti.jpg",
"flowy_saree.jpg",
"long_straight_suit.jpg",
"panel_kurti.jpg",
"lightweight_lehenga.jpg",
"vneck_straight_pants.jpg",
"relaxed_tunic.jpg",
"long_shrug_jeans.jpg",
"midi_shirt_dress.jpg"
]

bg_colors = [
(236,240,255),
(255,240,236),
(240,255,243),
(255,250,230),
(245,240,255)
]

for i, filename in enumerate(dress_files):

    # create blank image
    img = Image.new("RGB", (600,700), bg_colors[i % len(bg_colors)])
    draw = ImageDraw.Draw(img)

    # dress card background
    draw.rectangle((80,80,520,620), outline=(120,120,120), width=3, fill=(255,255,255))

    # head
    draw.ellipse((240,120,360,240), outline=(100,100,100), width=3, fill=(220,220,220))

    # body
    draw.rectangle((270,240,330,420), outline=(100,100,100), fill=(200,200,240))

    # skirt
    draw.polygon([(300,240),(180,520),(420,520)], outline=(100,100,100), fill=(210,210,240))

    # arms
    draw.line((270,280,180,380), fill=(100,100,100), width=6)
    draw.line((330,280,420,380), fill=(100,100,100), width=6)

    # text
    text = filename.replace(".jpg","").replace("_"," ").title()
    draw.text((120,650), text, fill=(50,50,50))

    # save
    img.save(os.path.join(output_dir, filename))

print("Dress images created successfully!")
print("Saved in:", output_dir)