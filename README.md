# 📧 Smart Email Generator untuk Pelajar
Aplikasi web ini dirancang untuk membantu pelajar menulis email profesional dengan mudah menggunakan teknologi AI dari Google Gemini. Dengan antarmuka yang intuitif, pengguna cukup memasukkan informasi penting, dan aplikasi akan menyusun email yang rapi dan sesuai konteks secara otomatis.

## 🌟 Fitur Aplikasi
- Pilihan jenis email seperti: Permintaan Akademik, Bimbingan Skripsi, Lamaran Magang, dan lainnya

- Gaya bahasa yang dapat disesuaikan: formal, netral, atau santai

- Dukungan multi-bahasa: Bahasa Indonesia dan Bahasa Inggris

- Input poin-poin utama yang ingin disampaikan

- Hasil akhir berupa email profesional yang siap dikirim

## ⚙️ Panduan Instalasi & Menjalankan Proyek
# 1. Kloning Repositori
git clone https://github.com/username/intelligent_email_writer.git
cd UAS_DindaMaharani_2208107010081

# 2. Menjalankan Backend (FastAPI)
- Buat dan aktifkan virtual environment
python -m venv env
env\Scripts\activate         

- Install dependensi backend
pip install -r requirements.txt

- Run Server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 3. Menjalankan Frontend (Streamlit)
Buka terminal baru:

- Aktifkan environment jika belum
env\Scripts\activate         # Windows

- Install dependensi frontend
pip install -r requirements_frontend.txt

- Jalankan Streamlit app
streamlit run app.py

## 🔐 Konfigurasi API Gemini
Buka: Google AI Studio

Buat API key

Simpan key ke dalam file .env seperti berikut:
GEMINI_API_KEY=masukkan_api_key_anda
API_URL=http://localhost:8000 

Salin file template .env.template terlebih dahulu:
cp .env.template .env

## 🧪 Cara Menggunakan
1.Pilih jenis email dan gaya bahasa

2.Masukkan nama penerima, subjek, dan poin-poin penting

3.Klik "Buat Email"

4.Email akan ditampilkan dan bisa langsung disalin untuk digunakan

## 🛠 Teknologi yang Digunakan
- Frontend: Streamlit

- Backend: FastAPI

- AI Model: Google Gemini (Generative AI)

- Bahasa Pemrograman: Python 3.8+

## ❓ Troubleshooting
- Server tidak merespon? Pastikan backend FastAPI sudah dijalankan di port 8000

- Email tidak muncul? Cek kembali format atau isi dari poin yang dimasukkan

- API error? Pastikan API Key sudah benar dan tersimpan di .env
