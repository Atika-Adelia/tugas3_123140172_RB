import os
import requests
from dotenv import load_dotenv
from google import genai

# =======================
# ENV & CONFIG
# =======================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_TOKEN = os.getenv("HF_TOKEN")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di .env")

if not HF_API_TOKEN:
    raise ValueError("HF_TOKEN tidak ditemukan di .env")

# Init Gemini Client (SDK BARU)
client = genai.Client(api_key=GEMINI_API_KEY)

# Hugging Face Sentiment Model (router terbaru)
HF_API_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
)

HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json",
}

# =======================
# SENTIMENT ANALYSIS
# =======================
def analyze_sentiment(review_text: str) -> str:
    payload = {"inputs": review_text}

    try:
        response = requests.post(
            HF_API_URL,
            headers=HF_HEADERS,
            json=payload,
            timeout=15
        )

        if response.status_code == 401:
            return "NEUTRAL (INVALID TOKEN)"

        if response.status_code in (429, 503):
            return "NEUTRAL (MODEL BUSY)"

        if response.status_code != 200:
            return "NEUTRAL (API ERROR)"

        result = response.json()

        if isinstance(result, list):
            scores = result[0] if isinstance(result[0], list) else result
            best = max(scores, key=lambda x: x["score"])
            return best["label"].upper()

        return "NEUTRAL"

    except requests.exceptions.RequestException:
        # =======================
        # 🔥 FALLBACK SENTIMENT LOKAL
        # =======================
        text = review_text.lower()

        positive_words = [
            "bagus", "puas", "ngebut", "cepat",
            "awet", "mantap", "keren", "oke"
        ]
        negative_words = [
            "mahal", "buruk", "jelek", "lambat", "kecewa"
        ]

        score = 0
        for w in positive_words:
            if w in text:
                score += 1
        for w in negative_words:
            if w in text:
                score -= 1

        if score > 0:
            return "POSITIVE"
        elif score < 0:
            return "NEGATIVE"
        return "NEUTRAL"


# =======================
# KEY POINT EXTRACTION
# =======================
def extract_key_points(review_text: str):
    prompt = f"""
    Dari ulasan produk berikut, ambil maksimal 3 poin kunci terpenting.
    Tulis dalam bentuk bullet point singkat berbahasa Indonesia.

    Ulasan:
    {review_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        raw_text = response.text.strip()
        points = []

        for line in raw_text.split("\n"):
            clean = line.strip().lstrip("-•").strip()
            if clean:
                points.append(clean)

        if points:
            return points[:3]

        raise ValueError("Empty Gemini response")

    except Exception:
        # =======================
        # 🔥 FALLBACK KEY POINT LOKAL
        # =======================
        text = review_text.lower()
        points = []

        if "performa" in text or "ngebut" in text:
            points.append("Performa produk dinilai sangat baik")

        if "baterai" in text or "awet" in text:
            points.append("Daya tahan baterai memuaskan untuk penggunaan harian")

        if "harga" in text or "mahal" in text:
            points.append("Harga relatif mahal dengan beberapa kekurangan minor")

        if not points:
            points.append("Ulasan bersifat umum tanpa poin dominan")

        return points[:3]


# =======================
# MAIN ANALYZER
# =======================
def analyze_review(review_text: str):
    sentiment = analyze_sentiment(review_text)
    key_points_list = extract_key_points(review_text)

    # Ubah list → string bullet
    key_points = "\n".join(f"• {p}" for p in key_points_list)

    return sentiment, key_points

