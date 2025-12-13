# ✨ Skincare Review Analyzer

**AI-powered sentiment analysis application for skincare product reviews using HuggingFace and Google Gemini API.**

| Backend | Frontend | Database |
| :---: | :---: | :---: |
| Python 3+ | Vite | PostgreSQL 14+ |
| Flask | CSS | SQLAlchemy |

## 🚀 Features

Aplikasi ini menggabungkan kekuatan Model Bahasa Besar (LLM) dengan backend yang stabil untuk memberikan analisis ulasan yang mendalam:

* **AI-Powered Sentiment Analysis:** Menggunakan model DistilBERT dari HuggingFace untuk mengklasifikasikan ulasan sebagai **positive, negative, atau neutral**.
* **Key Insights Extraction:** Memanfaatkan Google Gemini API untuk mengekstrak **poin-poin penting (key points)** secara terperinci dari ulasan panjang.
* **Persistent Storage:** Semua hasil analisis dan ulasan asli disimpan secara permanen di basis data **PostgreSQL**.
* **Modern Interface:** Antarmuka pengguna yang cantik dan responsif (*Responsive Design*) dibangun menggunakan **React** dan **Tailwind CSS**.

## 🖼️ Tampilan Awal Aplikasi

<img src="tampilan_awal.png" alt="Tampilan Aplikasi" width="600"/>

## 🖼️ Tampilan Hasil Analisis 

<img src="hasil_analisis.png" alt="Tampilan hasil_analisis" width="600"/>

## ⚙️ Persyaratan Sistem

Untuk menjalankan proyek ini, Anda memerlukan:

* Python 3.10+
* PostgreSQL Server (Lokal atau Cloud)
* Akses Terminal/Command Line

## 🔑 Konfigurasi API dan Database

1.  **Siapkan API Key:**
    * **Google Gemini API Key:** Dapatkan kunci Anda dari Google AI Studio dan aktifkan untuk model `gemini-1.5-flash`.
    * **HuggingFace Token:** Buat *Access Token* dengan izin *Read* dari situs HuggingFace.

2.  **Buat File `.env`:**
    Di dalam folder `backend`, buat file bernama **`.env`** dan isi variabel lingkungan Anda:
    ```env
    # API Keys
    GEMINI_API_KEY="AIzaSy..."
    HF_TOKEN="hf_..."

    # Database URL
    DATABASE_URL="postgresql+psycopg2://[USER_POSTGRES]:[PASSWORD]@localhost:5432/[DB_NAME]"
    # Contoh: DATABASE_URL="postgresql+psycopg2://atikaadelia@localhost:5432/review_db"
    ```

## 💻 Panduan Instalasi (Backend & Frontend)

### 1. Backend (Python/Flask)

1.  **Buka Terminal** di dalam folder `backend`.
2.  **Buat Virtual Environment:**
    ```bash
    python3 -m venv .venv
    ```
3.  **Aktifkan Environment:**
    ```bash
    source .venv/bin/activate
    ```
4.  **Instal Dependencies:**
    ```bash
    pip install python-dotenv Flask Flask-Cors sqlalchemy psycopg2-binary google-generativeai requests
    ```
5.  **Jalankan Server:**
    ```bash
    python3 app.py
    # Server akan berjalan di [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```

### 2. Frontend (React/Tailwind CSS)

1.  **Buka Terminal** di dalam folder `frontend`.
2.  **Instal Dependencies:**
    ```bash
    npm install
    ```
3.  **Jalankan Aplikasi:**
    ```bash
    npm run dev
    # Aplikasi akan terbuka di browser (biasanya http://localhost:5173)
    ```

## 🤝 Kontributor

* **ATIKA ADELIA (123140172)**
