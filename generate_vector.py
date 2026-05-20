# generate_vector.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

print("1. Membaca dataset CSV...")
df = pd.read_csv('anime_ultimate_cross_validated.csv').fillna('')

print("2. Menggabungkan teks...")
texts = (df['title'] + " " + df['tags'] + " " + df['description']).tolist()

print("3. Memuat AI Model (all-MiniLM-L6-v2)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("4. Sedang membuat Vektor (Bisa memakan waktu 10-15 menit tergantung CPU)...")
embeddings = model.encode(texts, show_progress_bar=True)

print("5. Menyimpan ke anime_vector.faiss...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))
faiss.write_index(index, 'anime_vector.faiss')

print("✅ SELESAI! File anime_vector.faiss berhasil dibuat. Silakan nyalakan server FastAPI.")
