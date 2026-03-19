import os
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("ROBOFLOW_API_KEY")
print("Loaded API Key:", API_KEY)

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key=API_KEY
)

MODEL_ID = "skin-tone-bd9ko/1"  


def normalize_skin_tone_label(label):
    if not label:
        return "unknown"

    label = label.strip().lower()

    mapping = {
        "white": "light",
        "light": "light",
        "fair": "light",
        "brown": "medium",
        "medium": "medium",
        "black": "dark",
        "dark": "dark"
    }

    return mapping.get(label, label)


def detect_skin_tone(image_path):
    try:
        print("Using MODEL_ID:", MODEL_ID)
        print("Image path sent to model:", image_path)

        result = CLIENT.infer(image_path, model_id=MODEL_ID)

        print("RAW SKIN RESULT:", result)

        preds = result.get("predictions", [])

        if not preds:
            return {
                "skin_tone": "unknown",
                "confidence": 0,
                "message": "No predictions returned by model"
            }

        top = max(preds, key=lambda x: x["confidence"])
        print("TOP PREDICTION:", top)

        label = normalize_skin_tone_label(top["class"])
        confidence = round(top["confidence"] * 100, 2)

        return {
            "skin_tone": label,
            "confidence": confidence
        }

    except Exception as e:
        print("SKIN MODEL ERROR:", str(e))
        return {
            "error": str(e)
        }