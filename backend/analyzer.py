import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_TOKEN = os.getenv("HF_TOKEN")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

HF_API_URL = "https://api-inference.huggingface.co/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student"

def analyze_sentiment(review_text):
    if not HF_API_TOKEN:
        return "Error: HF_TOKEN missing"

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": review_text}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"DEBUG SENTIMEN ERROR: {response.text}")
            return "Neutral (API Busy)"

        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            scores = result[0] if isinstance(result[0], list) else result
            top_result = max(scores, key=lambda x: x['score'])
            return top_result['label']
        
        return "Neutral"
    except Exception as e:
        print(f"DEBUG Exception: {str(e)}")
        return "Neutral (Connection Error)"

def extract_key_points(review_text):
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key missing"
        
    prompt = (
        "Dari ulasan produk berikut, identifikasi dan ekstrak 3 poin "
        "kunci terpenting secara singkat dalam bahasa Indonesia. "
        f"Ulasan: \"{review_text}\""
    )
    
    models_to_try = [
        'gemini-1.5-flash',      
        'gemini-1.5-flash-latest',
        'gemini-pro',            
        'gemini-1.0-pro'          
    ]

    last_error = ""

    for model_name in models_to_try:
        try:
            print(f"Mencoba model: {model_name}...") 
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gagal pakai {model_name}, mencoba yang lain...")
            last_error = str(e)
            continue
    
    return f"Gagal semua model. Cek API Key atau koneksi internet."

def analyze_review(review_text):
    sentiment = analyze_sentiment(review_text)
    key_points = extract_key_points(review_text)
    return sentiment, key_points