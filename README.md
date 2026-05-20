# 🌸 Anime AI Recommendation API 🤖

[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-blue?style=for-the-badge&logo=kaggle)](https://[www.kaggle.com/datasets/nathanfam/anime-datasets-updated-apr-**2026**](https://www.kaggle.com/datasets/nathanfam/anime-datasets-updated-apr-**2026**)) [![FastAPI](https://img.shields.io/badge/FastAPI-**005571**?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

🌍 **Choose Language:** [English](#english-version) | [Bahasa Indonesia](#versi-indonesia)

---

## <a id=*english-version*></a> 🇬🇧 English Version

### 📖 Overview

This repository contains the backend code for an **AI-powered Anime Recommendation **API****. Built with **FastAPI**, it uses **Sentence-Transformers** (Semantic Search) and **FAISS** (Facebook AI Similarity Search) to instantly find anime that share similar storylines, genres, and themes based on vector similarity.

### 🗄️ Where is the Dataset?

Due to GitHub's file size limits, the large data files (**CSV** and **FAISS** vectors) are **not included** in this repository. You must download them from Kaggle to run this **API**: 👉 **[Download Anime Dataset on Kaggle](https://[www.kaggle.com/datasets/nathanfam/anime-datasets-updated-apr-**2026**](https://www.kaggle.com/datasets/nathanfam/anime-datasets-updated-apr-**2026**))**

### 🚀 How to Run Locally

**Clone this repository** 
git clone [https://github.com/nathAlv08/anime_recommendation_model.git](https://github.com/nathAlv08/anime_recommendation_model.git) 
cd anime_recommendation_model 

## Download the Dataset Download the files from the Kaggle link above and place them in the root directory of this project. Ensure you have these file:

anime_ultimate_cross_validated.csv

## Generate FAISS Vector File (Important!)
Because the FAISS file is too large to host, you need to build it locally. Run the following script (this may take 10-15 minutes depending on your CPU):
python generate_vector.py

## Install Dependencies

Make sure you have Python 3.10+ installed.

pip install -r requirements.txt ## Start the Server
uvicorn app:app --host 0.0.0.0 --port **7860** The **API** will be running at [http://localhost:**7860**](http://localhost:**7860**)

📡 Main Endpoints **GET** / : Health check to see if the server is running.

**POST** /recommend : The main endpoint to get anime recommendations.

Payload Example (**JSON**):

**JSON**
{
    *title*: *Naruto*,
    *synopsis*: *Ninja boy wants to become Hokage...*,
    *top_k*: 10
}
**POST** /update-database : Triggers a background task to fetch the latest airing anime from Jikan **API**, converts them into vectors, and updates the **FAISS** index automatically.

## <a id=*versi-indonesia*></a> 🇮🇩 Versi Indonesia 

### 📖 Deskripsi Singkat 

Repositori ini berisi kode backend untuk **API** Rekomendasi Anime berbasis AI. Dibangun menggunakan FastAPI, sistem ini menggunakan Sentence-Transformers (Pencarian Semantik) dan **FAISS** untuk menemukan anime dengan alur cerita, genre, dan tema yang mirip secara instan melalui perbandingan jarak vektor.

### 🗄️ Di Mana Dataset-nya? 

Karena adanya batasan ukuran file di GitHub, file data berukuran besar (**CSV** dan Vektor **FAISS**) tidak disertakan di dalam repositori ini. Kamu wajib mengunduhnya dari Kaggle untuk bisa menjalankan **API** ini: 👉 Download Dataset Anime di Kaggle

### 🚀 Cara Menjalankan di Komputer Lokal 

**Clone Repositori Ini**

git clone [https://github.com/nathAlv08/anime_recommendation_model.git](https://github.com/nathAlv08/anime_recommendation_model.git) 
cd anime_recommendation_model 

**Unduh Dataset Unduh file dari tautan Kaggle di atas, lalu letakkan di dalam folder utama project ini. Pastikan ada file ini**

anime_ultimate_cross_validated.csv

**Buat File Vektor FAISS (Wajib!)**
Karena file FAISS tidak disediakan, kamu harus membangunnya sendiri. Jalankan perintah ini (prosesnya butuh sekitar 10-15 menit tergantung kecepatan CPU):

python generate_vector.py

**Install Library yang Dibutuhkan**

Pastikan Python 3.10+ sudah terinstal di komputermu.

pip install -r requirements.txt ## Nyalakan Server

uvicorn app:app --host 0.0.0.0 --port **7860** **API** akan berjalan di [http://localhost:**7860**](http://localhost:**7860**)

📡 Endpoints Utama **GET** / : Pengecekan status untuk memastikan server menyala.

**POST** /recommend : Jalur utama untuk meminta rekomendasi anime.

Contoh Payload (**JSON**):

**JSON**
{
    *title*: *Naruto*,
    *synopsis*: *Seorang anak ninja yang ingin menjadi Hokage...*,
    *top_k*: 10
}
**POST** /update-database : Menjalankan tugas di latar belakang (background task) untuk mengambil data anime terbaru dari Jikan **API**, mengubahnya menjadi vektor, dan memperbarui memori **FAISS** secara otomatis.

Built with 🔥 by Nathan  `
