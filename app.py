from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import datetime
import os

# ==========================================
# 1. PERSIAPAN SERVER API
# ==========================================
app = FastAPI(title="Anime AI Recommender API", version="2.0")

# Mengizinkan akses dari aplikasi Flutter (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nama file database kita
CSV_FILE = "anime_ultimate_cross_validated.csv"
FAISS_FILE = "anime_vector.faiss"

# Variabel global untuk menyimpan data di memori server
df = None
model = None
faiss_index = None

# ==========================================
# 2. PROSES STARTUP (HANYA BERJALAN 1 KALI)
# ==========================================
@app.on_event("startup")
def load_resources():
    global df, model, faiss_index
    
    print("🚀 [1/3] Memuat AI Model (Sentence-Transformers)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("🧠 [2/3] Memuat FAISS Vector Memory Anime...")
    faiss_index = faiss.read_index(FAISS_FILE)
    
    print("📚 [3/3] Memuat Database Anime CSV...")
    df = pd.read_csv(CSV_FILE)
    df = df.fillna("") # Membersihkan data kosong
    
    print("✅ Server Anime Recommender Siap Digunakan!")

# ==========================================
# 3. FORMAT PERMINTAAN DARI FLUTTER
# ==========================================
class RecommendRequest(BaseModel):
    title: str
    synopsis: str
    top_k: int = 15

# ==========================================
# 4. ENDPOINT CEK STATUS
# ==========================================
@app.get("/")
def read_root():
    return {
        "status": "Active", 
        "total_anime": len(df) if df is not None else 0,
        "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Backend Anime AI Berjalan Lancar!"
    }

# ==========================================
# 5. ENDPOINT UTAMA UNTUK MENCARI REKOMENDASI
# ==========================================
@app.post("/recommend")
def get_recommendations(req: RecommendRequest):
    try:
        query_text = f"{req.title} {req.synopsis}"
        query_vector = model.encode([query_text]).astype('float32')
        
        distances, indices = faiss_index.search(query_vector, req.top_k)
        
        results = []
        for i in range(req.top_k):
            idx = int(indices[0][i])
            if idx < len(df):
                row = df.iloc[idx]
                results.append({
                    "title": str(row.get("title", "Unknown")),
                    "description": str(row.get("description", "")),
                    "year": str(row.get("year", "")),
                    "tags": str(row.get("tags", "")),
                    "cover": str(row.get("cover", "")),
                    "similarity_score": float(distances[0][i])
                })
                
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 6. LOGIKA AUTO-UPDATE (BERJALAN DI LATAR BELAKANG)
# ==========================================
def fetch_and_update_database():
    global df, faiss_index
    print(f"🔄 Memulai proses update harian pada: {datetime.datetime.now()}")
    
    try:
        # Mengambil data anime yang sedang tayang musim ini dari Jikan API
        url = "https://api.jikan.moe/v4/seasons/now?limit=25"
        res = requests.get(url, timeout=10)
        
        if res.status_code == 200:
            data = res.json().get('data', [])
            new_anime_added = 0
            
            # Buat daftar judul yang sudah ada menjadi huruf kecil semua untuk pencocokan
            existing_titles = set(df['title'].str.lower().str.strip().tolist())
            
            new_rows = []
            new_texts = []
            
            for item in data:
                title = item.get('title_english') or item.get('title') or ""
                if not title: continue
                
                cleaned_title = title.lower().strip()
                
                # Jika anime ini benar-benar baru dan belum ada di database kita
                if cleaned_title not in existing_titles:
                    genres = [g['name'] for g in item.get('genres', [])]
                    description = item.get('synopsis') or "Tidak ada sinopsis."
                    
                    # Siapkan baris data baru
                    new_row = {
                        "title": title.strip(),
                        "description": description,
                        "rating": item.get('score') or 0.0,
                        "year": str(item.get('year') or ""),
                        "tags": str(genres),
                        "cover": item.get('images', {}).get('jpg', {}).get('large_image_url') or ""
                    }
                    new_rows.append(new_row)
                    
                    # Siapkan teks gabungan untuk dipelajari oleh AI
                    combined_text = f"{title} {str(genres)} {description}"
                    new_texts.append(combined_text)
                    new_anime_added += 1
            
            if new_anime_added > 0:
                print(f"✨ Menemukan {new_anime_added} anime baru! Sedang memproses AI Vektor...")
                
                # 1. Ubah teks baru menjadi vektor
                new_embeddings = model.encode(new_texts).astype('float32')
                
                # 2. Tambahkan ke memori FAISS
                faiss_index.add(new_embeddings)
                
                # 3. Tambahkan ke DataFrame Pandas (CSV)
                new_df = pd.DataFrame(new_rows)
                df = pd.concat([df, new_df], ignore_index=True)
                df = df.fillna("")
                
                # 4. Simpan pembaruan ke dalam file fisik
                faiss.write_index(faiss_index, FAISS_FILE)
                df.to_csv(CSV_FILE, index=False)
                
                print("✅ Database berhasil diperbarui dan disimpan!")
            else:
                print("💤 Tidak ada anime baru yang perlu ditambahkan hari ini.")
                
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat auto-update: {e}")

# ==========================================
# 7. ENDPOINT PINTU RAHASIA UNTUK AUTO-UPDATE
# ==========================================
@app.post("/update-database")
def trigger_update(background_tasks: BackgroundTasks):
    # BackgroundTasks memastikan server langsung menjawab "OK" ke cron-job
    # tanpa harus menunggu proses download dan AI selesai.
    background_tasks.add_task(fetch_and_update_database)
    return {"message": "Proses update latar belakang telah dimulai!"}