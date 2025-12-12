# backend/analyzer.py
import os
from transformers import pipeline
from google import genai
from dotenv import load_dotenv # type: ignore

load_dotenv()

sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model=os.getenv("HF_SENTIMENT_MODEL", "w11wo/indonesian-roberta-sentiment-classifier")
) 

# Inisialisasi Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = "gemini-2.5-flash"

def analyze_sentiment(review_text):
    # analisis sentimen
    result = sentiment_pipeline(review_text)[0]
    return result['label'] 

def extract_key_points(review_text):
    prompt = (
        "Dari ulasan produk berikut, identifikasi dan ekstrak 3 poin "
        "kunci terpenting dari ulasan tersebut. Format jawabannya sebagai "
        "daftar poin yang dipisahkan koma atau sebagai satu paragraf terstruktur."
        f"Ulasan: \"{review_text}\""
    )

    try:
        response = client.models.generate_content(
            model=gemini_model,
            contents=[prompt]
        )
        return response.text
    except Exception as e:
        return f"Error ekstrasi: {str(e)}"

def analyze_review(review_text):
    sentiment = analyze_sentiment(review_text)
    key_points = extract_key_points(review_text)
    return sentiment, key_points