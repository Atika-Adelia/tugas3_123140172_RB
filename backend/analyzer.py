import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- PERBAIKAN 1: URL ROUTER BARU (WAJIB GANTI INI) ---
HF_API_URL = "https://router.huggingface.co/hf-inference/models/mdhugol/indonesia-bert-sentiment-classification"
HF_API_TOKEN = os.getenv("HF_TOKEN") 

def analyze_sentiment(review_text):
    if not HF_API_TOKEN:
        return "Error: HF_TOKEN missing"

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": review_text}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        
        # Jika masih error, kita kembalikan pesan netral agar aplikasi tidak crash
        if response.status_code != 200:
            print(f"DEBUG HF Error: {response.text}") # Cek terminal untuk detail
            return "Neutral (API Error)"

        result = response.json()
        
        # Kadang API mengembalikan list, kadang dict
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                top_result = max(result[0], key=lambda x: x['score'])
            else:
                top_result = max(result, key=lambda x: x['score'])
            return top_result['label']
        
        return "Neutral"
    except Exception as e:
        print(f"DEBUG Exception: {str(e)}")
        return "Neutral (Conn Error)"

def extract_key_points(review_text):
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key missing"
        
    prompt = (
        "Dari ulasan produk berikut, identifikasi dan ekstrak 3 poin "
        "kunci terpenting secara singkat. "
        f"Ulasan: \"{review_text}\""
    )
    
    try:
        # --- PERBAIKAN 2: KEMBALI KE GEMINI-PRO (LEBIH STABIL) ---
        model = genai.GenerativeModel('gemini-pro') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Poin kunci tidak tersedia (Gemini Error: {str(e)[:50]}...)"

def analyze_review(review_text):
    sentiment = analyze_sentiment(review_text)
    key_