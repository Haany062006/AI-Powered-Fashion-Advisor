import os
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "llama3-8b-8192").strip()

DATA_DIR = os.path.join(BASE_DIR, "data")
COLOR_RULES_FILE = os.path.join(DATA_DIR, "color_rules.json")
DRESS_RULES_FILE = os.path.join(DATA_DIR, "dress_rules.json")


def load_json_file(path):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
    return {}


COLOR_RULES = load_json_file(COLOR_RULES_FILE)
DRESS_RULES = load_json_file(DRESS_RULES_FILE)


def build_fashion_context():
    return """
You are an AI fashion assistant for women's styling.

You should answer only fashion-related questions such as:
- skin tone colors
- undertone colors
- body shape styling
- casual wear
- party wear
- traditional wear
- western wear
- office wear
- matching colors
- outfit combinations
- jeans, kurti, saree, dresses, tops, skirts, gowns, lehengas, blazers

Important behavior:
- Give practical, stylish, easy-to-understand answers
- Keep answers concise but useful
- If the user asks something unrelated to fashion, politely say you only help with fashion and styling
- If the user asks broad questions, give 4 to 8 useful suggestions
- If body shape, skin tone, or undertone are mentioned, tailor the answer accordingly

Body shape guidance:
- pear: A-line dresses, wrap dresses, fit and flare dresses, high-waist skirts, structured tops, flared kurtis
- apple: empire waist dresses, V-neck tops, straight kurtis, flowy dresses, long shrugs
- hourglass: bodycon dresses, belted outfits, fitted kurtis, sarees, wrap dresses
- rectangle: peplum dresses, skater dresses, layered styles, ruffle tops, belted outfits
- inverted_triangle: A-line skirts, fit and flare dresses, wide-leg bottoms, flared kurtis, softer lower silhouettes

Undertone guidance:
- Warm: mustard, olive, coral, rust, peach, camel, terracotta
- Cool: lavender, navy blue, plum, berry, rose pink, emerald, cool blue shades
- Neutral: teal, mauve, burgundy, dusty rose, cream, sage green, soft coral

Skin tone guidance:
- light: emerald green, navy blue, burgundy, lavender, rose pink, coral, soft peach
- medium: mustard, teal, olive green, coral, maroon, forest green, rust, royal blue
- dark: white, gold, bright yellow, royal blue, emerald green, magenta, coral, burgundy

Category guidance:
- party wear: satin gowns, cocktail dresses, embellished lehengas, party sarees, stylish jumpsuits
- casual wear: jeans with tops, midi dresses, relaxed kurtis, co-ord sets, flats, sneakers
- traditional wear: sarees, anarkalis, straight kurtis, lehengas, sharara sets, jacket kurtis
- western wear: A-line dresses, bodycon dresses, wrap dresses, blazers, skirts, jumpsuits
- office wear: straight pants, blazers, midi dresses, simple kurtis, solid shirts, neutral tones
""".strip()


def format_color_rules():
    if not COLOR_RULES:
        return "No color rules loaded."

    lines = ["Color rules:"]
    for tone, undertones in COLOR_RULES.items():
        lines.append(f"- {tone}:")
        for undertone, colors in undertones.items():
            color_names = []
            for color in colors[:8]:
                if isinstance(color, dict):
                    color_names.append(color.get("name", "Unknown"))
                else:
                    color_names.append(str(color))
            lines.append(f"  - {undertone}: {', '.join(color_names)}")
    return "\n".join(lines)


def format_dress_rules():
    if not DRESS_RULES:
        return "No dress rules loaded."

    lines = ["Dress rules:"]
    for shape, categories in DRESS_RULES.items():
        lines.append(f"- {shape}:")
        for category, items in categories.items():
            names = []
            for item in items[:6]:
                if isinstance(item, dict):
                    names.append(item.get("name", "Dress"))
                else:
                    names.append(str(item))
            lines.append(f"  - {category}: {', '.join(names)}")
    return "\n".join(lines)


SYSTEM_PROMPT = f"""
{build_fashion_context()}

Use the following project knowledge when useful.

{format_color_rules()}

{format_dress_rules()}
""".strip()


def is_fashion_related(message: str) -> bool:
    msg = message.lower().strip()

    fashion_keywords = [
        "fashion", "style", "styling", "outfit", "dress", "dresses", "wear", "clothes", "clothing",
        "top", "tops", "jeans", "kurti", "saree", "lehenga", "gown", "blazer", "skirt", "jumpsuit",
        "body shape", "pear", "apple", "hourglass", "rectangle", "inverted triangle",
        "skin tone", "undertone", "warm", "cool", "neutral", "light skin", "medium skin", "dark skin",
        "party", "casual", "traditional", "western", "office", "formal", "college",
        "match", "matching", "color", "colour", "heels", "shoes", "bag", "jewelry", "accessories"
    ]

    return any(keyword in msg for keyword in fashion_keywords)


def call_llm(user_message: str):
    if not LLM_API_KEY:
        print("LLM_API_KEY not found in .env")
        return None

    print("Using LLM_API_URL:", LLM_API_URL)
    print("Using LLM_MODEL:", LLM_MODEL)
    print("LLM key loaded:", LLM_API_KEY[:10] + "..." if len(LLM_API_KEY) > 10 else "short_key")

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=30)

        print("LLM status code:", response.status_code)
        print("LLM raw text:", response.text)

        response.raise_for_status()
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()

        print("No choices found in LLM response")
        return None

    except Exception as e:
        print("LLM ERROR:", str(e))
        return None

def fallback_fashion_reply(message: str) -> str:
    msg = message.lower().strip()

    if any(word in msg for word in ["hi", "hello", "hey", "hii", "hy"]):
        return "Hi! I can help with fashion questions about skin tone, undertone, body shape, colors, casual wear, party wear, traditional wear, western wear, and styling tips."

    if "warm undertone" in msg or ("warm" in msg and "undertone" in msg):
        return "Warm undertones usually suit mustard, olive, coral, rust, peach, camel, terracotta, and warm beige shades."

    if "cool undertone" in msg or ("cool" in msg and "undertone" in msg):
        return "Cool undertones usually suit lavender, navy blue, plum, berry shades, rose pink, emerald green, and cool blue tones."

    if "neutral undertone" in msg or ("neutral" in msg and "undertone" in msg):
        return "Neutral undertones usually suit both warm and cool shades like teal, mauve, burgundy, dusty rose, cream, and sage green."

    if "light skin" in msg or "light skin tone" in msg:
        return "Light skin tone usually suits emerald green, navy blue, burgundy, lavender, rose pink, coral, and soft peach."

    if "medium skin" in msg or "medium skin tone" in msg:
        return "Medium skin tone usually suits mustard, teal, olive green, coral, maroon, forest green, rust, and royal blue."

    if "dark skin" in msg or "dark skin tone" in msg:
        return "Dark skin tone usually looks great in white, gold, bright yellow, royal blue, emerald green, magenta, coral, and burgundy."

    if "pear" in msg:
        if "party" in msg:
            return "For a pear body shape in party wear, try A-line dresses, wrap dresses, flared gowns, embellished lehengas, and fit-and-flare outfits."
        if "traditional" in msg:
            return "For a pear body shape in traditional wear, Anarkali, A-line kurti, flared lehenga, soft saree draping, and jacket kurtis usually work well."
        if "casual" in msg:
            return "For a pear body shape in casual wear, try high-waist jeans, peplum tops, skater dresses, casual midi dresses, and shrugs with fitted tops."
        if "western" in msg:
            return "For a pear body shape in western wear, A-line dresses, wrap dresses, fit-and-flare dresses, structured jackets, and high-waist skirts suit well."
        return "Pear body shape usually suits A-line dresses, wrap dresses, fit-and-flare dresses, high-waist skirts, flared kurtis, and structured tops."

    if "apple" in msg:
        return "Apple body shape often suits empire waist dresses, V-neck tops, straight kurtis, flowy dresses, and long shrugs."

    if "hourglass" in msg:
        return "Hourglass body shape usually suits bodycon dresses, belted outfits, fitted kurtis, sarees, and wrap dresses."

    if "rectangle" in msg:
        return "Rectangle body shape usually suits peplum dresses, skater dresses, layered styles, ruffle tops, and belted outfits."

    if "inverted triangle" in msg or ("inverted" in msg and "triangle" in msg):
        return "Inverted triangle body shape usually suits A-line skirts, fit-and-flare dresses, flared kurtis, wide-leg bottoms, and softer lower silhouettes."

    if "party wear" in msg or "party outfit" in msg or "party" in msg:
        return "For party wear, try satin gowns, cocktail dresses, embellished lehengas, party sarees, stylish jumpsuits, or statement skirts."

    if "casual" in msg:
        return "For casual wear, go for jeans with tops, casual midi dresses, relaxed kurtis, co-ord sets, and comfortable flats or sneakers."

    if "traditional" in msg:
        return "Traditional wear options include sarees, anarkalis, straight kurtis, lehengas, sharara sets, peplum kurtis, and jacket-style kurtis."

    if "western" in msg:
        return "Western wear options include A-line dresses, bodycon dresses, wrap dresses, blazers, skirts with tops, jumpsuits, and fit-and-flare outfits."

    if "office wear" in msg or "formal wear" in msg or "office" in msg or "formal" in msg:
        return "For office wear, choose straight pants, blazers, midi dresses, simple kurtis, solid shirts, neutral tones, and elegant minimal styling."

    if "what color goes with" in msg or "match with" in msg or "matching colors" in msg:
        return "Neutral shades like white, black, beige, denim blue, brown, and grey usually match well with many colors."

    if "jeans" in msg:
        return "Jeans go well with fitted tops, peplum tops, crop tops, shrugs, blazers, kurtis, and casual shirts depending on the look."

    if "kurti" in msg:
        return "A kurti can be styled with leggings, palazzos, straight pants, jeans, dupattas, belts, and statement earrings."

    if "saree" in msg:
        return "Sarees can be styled with contrast blouses, belts, minimal jewelry, elegant heels, and neat draping styles."

    if "college" in msg:
        return "For college wear, go for casual kurtis, jeans with tops, midi dresses, simple co-ord sets, and comfortable sneakers or flats."

    return "I can help with fashion questions about colors, undertones, skin tone, body shape, traditional wear, western wear, casual outfits, party wear, office wear, and styling tips."


def get_fashion_chatbot_response(message: str) -> str:
    if not message or not message.strip():
        return "Please ask a fashion-related question."

    if not is_fashion_related(message):
        return "I currently help only with fashion and styling questions like outfits, colors, body shape, skin tone, and styling tips."

    llm_reply = call_llm(message)
    if llm_reply:
        return llm_reply

    return fallback_fashion_reply(message)