import webbrowser
import time

dress_data = {
    "western": [
        "A-line dress", "Wrap dress", "Fit and flare dress", "Peplum outfit",
        "High waist jeans with top", "Blazer dress", "Off shoulder dress",
        "Maxi dress", "Bodycon dress", "Shirt dress",
        "Jumpsuit", "Skater dress", "Pencil skirt outfit",
        "Wide leg pants outfit", "Crop jacket dress", "Midi dress",
        "Empire waist dress", "Ruffle dress", "Bootcut pants outfit", "Layered western outfit"
    ],
    "traditional": [
        "A-line kurti", "Anarkali suit", "Straight cut suit", "Umbrella kurti",
        "Lehenga", "Classic saree", "Belted saree", "Salwar suit",
        "Patiala suit", "Palazzo kurti set", "Floor length anarkali",
        "Half saree", "Sharara set", "Embroidered kurti",
        "Jacket style kurti", "Cotton kurti", "Silk saree",
        "Festive lehenga", "Straight kurta set", "Ethnic gown"
    ],
    "casual": [
        "T-shirt and jeans", "Kurti with leggings", "Tunic with pants",
        "Casual maxi dress", "Shirt with jeans", "Long top with leggings",
        "Denim jacket outfit", "Cotton casual dress", "Oversized top outfit",
        "Casual coord set", "Casual kurti", "Flared top with jeans",
        "Midi casual dress", "Comfort wear set", "Palazzo casual set",
        "Summer dress", "Layered casual outfit", "Straight pants outfit",
        "Printed casual dress", "Soft fabric casual set"
    ],
    "party_wear": [
        "Sequin gown", "Party anarkali", "Mermaid gown", "Off shoulder gown",
        "Party saree", "Cocktail dress", "Glitter dress", "Party lehenga",
        "One shoulder gown", "Velvet gown", "Party jumpsuit",
        "Ruffle party dress", "Embellished gown", "Fish cut skirt set",
        "Long trail gown", "Shimmer saree", "Evening dress",
        "Reception lehenga", "Party peplum set", "Fusion party outfit"
    ]
}

base_url = "https://www.bing.com/images/create?q="

for category, dresses in dress_data.items():
    print(f"\n🔹 {category.upper()}")

    for i, dress in enumerate(dresses, start=1):
        prompt = f"A realistic fashion catalog photo of a woman wearing {dress}, full body, front view, white background, professional lighting"
        
        url = base_url + prompt.replace(" ", "%20")

        print(f"Opening: {category}_{i:02d}")
        webbrowser.open(url)

        time.sleep(5)  # wait before opening next