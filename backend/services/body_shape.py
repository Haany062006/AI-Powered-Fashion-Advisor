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

MODEL_ID = "woman-body-shape-nwnj8-nnrmu/1"


def normalize_label(label):
    label = label.strip().lower()

    mapping = {
        "pear": "pear",
        "triangle": "triangle",
        "apple": "apple",
        "hourglass": "hourglass",
        "rectangle": "rectangle",
        "inverted triangle": "inverted_triangle",
        "inverted_triangle": "inverted_triangle"
    }

    return mapping.get(label, label)


def detect_body_shape(image_path):
    try:
        result = CLIENT.infer(image_path, model_id=MODEL_ID)

        print("RAW RESULT:", result)

        preds = result.get("predictions", [])

        if not preds:
            return {
                "body_shape": "unknown",
                "confidence": 0
            }

        top = max(preds, key=lambda x: x["confidence"])

        label = normalize_label(top["class"])
        confidence = round(top["confidence"] * 100, 2)

        return {
            "body_shape": label,
            "confidence": confidence
        }

    except Exception as e:
        return {
            "body_shape": "error",
            "confidence": 0,
            "message": str(e)
        }