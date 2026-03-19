import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # backend/services
BACKEND_DIR = os.path.dirname(BASE_DIR)                 # backend
PROJECT_DIR = os.path.dirname(BACKEND_DIR)              # project root
DRESS_RULES_PATH = os.path.join(PROJECT_DIR, "data", "dress_rules.json")


def normalize_body_shape_for_rules(body_shape):
    if not body_shape:
        return ""

    shape = body_shape.strip().lower().replace(" ", "_")

    mapping = {
        "pear": "pear",
        "triangle": "triangle",
        "apple": "apple",
        "hourglass": "hourglass",
        "rectangle": "rectangle",
        "inverted_triangle": "inverted_triangle",
        "inverted triangle": "inverted_triangle"
    }

    return mapping.get(shape, shape)


def get_dress_recommendations(body_shape, category):
    try:
        if not os.path.exists(DRESS_RULES_PATH):
            return {"error": "dress_rules.json file not found"}

        with open(DRESS_RULES_PATH, "r", encoding="utf-8") as file:
            dress_rules = json.load(file)

        normalized_shape = normalize_body_shape_for_rules(body_shape)
        normalized_category = category.strip().lower()

        print("Detected body shape:", body_shape)
        print("Normalized body shape:", normalized_shape)
        print("Available dress rule keys:", list(dress_rules.keys()))

        matched_shape_key = None
        for key in dress_rules.keys():
            if key.strip().lower().replace(" ", "_") == normalized_shape:
                matched_shape_key = key
                break

        if not matched_shape_key:
            return {"error": f"Body shape '{body_shape}' not found in dress rules"}

        matched_category_key = None
        for key in dress_rules[matched_shape_key].keys():
            if key.strip().lower() == normalized_category:
                matched_category_key = key
                break

        if not matched_category_key:
            return {
                "error": f"Category '{category}' not found for body shape '{matched_shape_key}'"
            }

        recommendations = dress_rules[matched_shape_key][matched_category_key]

        fixed_recommendations = []
        for item in recommendations:
            if isinstance(item, dict):
                name = item.get("name", "Dress")
                image = item.get("image", "")

                if (
                    image
                    and not image.startswith("http://")
                    and not image.startswith("https://")
                    and not image.startswith("/images/")
                ):
                    image = f"/images/{image}"

                fixed_recommendations.append({
                    "name": name,
                    "image": image
                })

            elif isinstance(item, str):
                fixed_recommendations.append({
                    "name": item,
                    "image": ""
                })

        return {
            "body_shape": matched_shape_key,
            "category": matched_category_key,
            "recommendations": fixed_recommendations
        }

    except Exception as e:
        return {"error": str(e)}