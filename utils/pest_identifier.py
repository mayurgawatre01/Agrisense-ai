"""
CropSense v3.1 — Pest / Disease Identifier
Primary  : Google Gemini API (vision) — free tier available, no card needed
           for basic use. Needs GEMINI_API_KEY set in .env.
Fallback : Anthropic Claude API (vision) — used automatically if Gemini's
           key is missing or the Gemini call fails. Needs ANTHROPIC_API_KEY.
If NEITHER key works, a clear message is shown to the farmer
(no fake AI result is ever invented).
"""
import os
import base64
import json
import re
import urllib.request
import urllib.error

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MODEL = "gemini-2.0-flash"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-sonnet-4-6"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MEDIA_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".webp": "image/webp"
}

SYSTEM_PROMPT = (
    "You are an expert Indian agricultural extension officer who identifies crop pests "
    "and diseases from photographs for small and marginal farmers. "
    "Look carefully at the uploaded photo of a crop leaf/stem/fruit. "
    "Respond ONLY with a single JSON object (no markdown, no preamble, no code fences) "
    "with exactly these keys:\n"
    '{"is_plant": true/false, "crop_guess": "string or null", '
    '"problem_name_en": "string", "problem_name_hi": "string (Hindi/Hinglish name)", '
    '"confidence": "High/Medium/Low", '
    '"symptoms_hi": "1-2 sentences in simple Hindi describing what is visible", '
    '"cause": "Fungal/Bacterial/Viral/Pest/Nutrient Deficiency/Healthy/Unclear", '
    '"organic_treatment_hi": "1-2 practical organic/cultural remedies in simple Hindi", '
    '"chemical_treatment_hi": "1-2 common chemical treatment names in simple Hindi, or empty string if not needed", '
    '"prevention_hi": "1 sentence prevention tip in simple Hindi"}\n'
    "If the image does not clearly show a plant/crop, set is_plant to false and explain "
    "briefly in symptoms_hi. Keep all Hindi text simple enough for a farmer with basic "
    "literacy to read — short sentences, common words, Devanagari script. "
    "Never invent a diagnosis you are not reasonably confident about — if unclear, say so "
    "and set confidence to 'Low'."
)


def _strip_code_fences(text: str) -> str:
    return re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()


def _call_gemini(image_path: str, ext: str, key: str):
    """Calls Google Gemini's vision API. Returns dict: success, data/error."""
    media_type = MEDIA_TYPES[ext]
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "contents": [{
            "parts": [
                {"text": SYSTEM_PROMPT + "\n\nIs crop photo mein kya problem hai? JSON format mein batao."},
                {"inline_data": {"mime_type": media_type, "data": img_b64}}
            ]
        }],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 700}
    }

    url = GEMINI_API_URL.format(model=GEMINI_MODEL)
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    candidates = result.get("candidates", [])
    if not candidates:
        raise ValueError("Gemini returned no candidates")

    parts = candidates[0].get("content", {}).get("parts", [])
    raw_text = "\n".join(p.get("text", "") for p in parts).strip()
    raw_text = _strip_code_fences(raw_text)
    parsed = json.loads(raw_text)
    return {"success": True, "data": parsed, "provider": "Gemini"}


def _call_claude(image_path: str, ext: str, key: str):
    """Calls Anthropic Claude's vision API. Returns dict: success, data/error."""
    media_type = MEDIA_TYPES[ext]
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 700,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": img_b64}},
                {"type": "text", "text": "Is crop photo mein kya problem hai? JSON format mein batao."}
            ]
        }]
    }

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text_blocks = [b["text"] for b in result.get("content", []) if b.get("type") == "text"]
    raw_text = _strip_code_fences("\n".join(text_blocks).strip())
    parsed = json.loads(raw_text)
    return {"success": True, "data": parsed, "provider": "Claude"}


def identify_pest_disease(image_path: str, gemini_key: str = "", anthropic_key: str = ""):
    """
    Tries Google Gemini first (free-tier friendly), then falls back to
    Anthropic Claude if Gemini's key is missing or the call fails.
    Returns dict: success, data (parsed JSON) + provider, OR error message.
    """
    gkey = gemini_key or os.environ.get("GEMINI_API_KEY", "")
    akey = anthropic_key or os.environ.get("ANTHROPIC_API_KEY", "")

    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return {"success": False, "error": "Sirf JPG, PNG ya WEBP photo upload karein."}

    if not gkey and not akey:
        return {
            "success": False,
            "error": "AI photo analysis abhi configure nahi hai. Admin ko GEMINI_API_KEY "
                     "ya ANTHROPIC_API_KEY (.env file mein) set karna hoga is feature ko enable karne ke liye."
        }

    last_error = None

    # 1. Try Gemini first
    if gkey:
        try:
            return _call_gemini(image_path, ext, gkey)
        except urllib.error.HTTPError as e:
            last_error = f"Gemini error ({e.code})"
        except json.JSONDecodeError:
            last_error = "Gemini response samajh nahi aaya"
        except Exception as e:
            last_error = f"Gemini error: {str(e)}"

    # 2. Fallback to Claude
    if akey:
        try:
            return _call_claude(image_path, ext, akey)
        except urllib.error.HTTPError as e:
            last_error = f"Claude error ({e.code})"
        except json.JSONDecodeError:
            last_error = "Claude response samajh nahi aaya"
        except Exception as e:
            last_error = f"Claude error: {str(e)}"

    return {
        "success": False,
        "error": f"Photo analyze nahi ho payi ({last_error}). Thodi der baad dobara try karein, "
                 "ya clear photo upload karein."
    }


# ── Offline quick-reference guide (shown alongside the upload tool) ───────
COMMON_PROBLEMS = [
    {
        "name_hi": "Patti Jhulsa (Leaf Blight)",
        "crops": "Dhaan, Gehu, Aalu",
        "symptoms": "Pattiyon par bhure/kale dhabbe, kinare jalein hue jaise dikhte hain.",
        "treatment": "Copper oxychloride 0.3% spray karein, khet mein paani jamne na dein."
    },
    {
        "name_hi": "Safed Makkhi (Whitefly)",
        "crops": "Kapas, Tamatar, Mirch",
        "symptoms": "Patton ke neeche chhote safed kide, patte peele padna shuru hote hain.",
        "treatment": "Neem oil spray (5ml/litre paani) har 7 din mein, yellow sticky traps lagayein."
    },
    {
        "name_hi": "Tana Chedak (Stem Borer)",
        "crops": "Dhaan, Maize",
        "symptoms": "Beech ka tana sookh jaata hai (dead heart), pौधा murjha jaata hai.",
        "treatment": "Trichogramma card lagayein ya recommended insecticide (Cartap Hydrochloride) use karein."
    },
    {
        "name_hi": "Powdery Mildew (Sufedi)",
        "crops": "Sabzi, Angoor, Gehu",
        "symptoms": "Pattiyon par safed powder jaisi parat dikhti hai.",
        "treatment": "Sulphur dust ya wettable sulphur spray karein, hawa-dar jagah par lagayein."
    },
    {
        "name_hi": "Aphids (Mahu)",
        "crops": "Sarson, Gehu, Sabzi",
        "symptoms": "Choti hari/kali kide nayi patti aur tane par jhund mein milti hain.",
        "treatment": "Neem oil ya soap solution spray, ladybird beetle predator ko protect karein."
    },
    {
        "name_hi": "Nitrogen Deficiency",
        "crops": "Sabhi fasal",
        "symptoms": "Purani pattiyan halki peeli padna shuru hoti hain, growth slow ho jaati hai.",
        "treatment": "Urea ki top dressing karein recommended matra mein."
    },
]
