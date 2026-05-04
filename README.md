# 📊 Business Dashboard - Analisis Penjualan

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Sebuah aplikasi web interaktif berbasis **Streamlit** untuk memantau, menganalisis, dan memvisualisasikan data penjualan secara *real-time*. Dashboard ini dirancang agar pengguna dapat dengan mudah mengunggah data mentah (CSV) dan langsung mendapatkan *insight* bisnis melalui grafik interaktif dan tabel informatif.

---

## 🔗 Live Demo

- 🚀 **Akses Dashboard:**  
  https://fxghkrpx8trremxkmbeuau.streamlit.app/

- 🧪 **Generate Data Dummy (CSV):**  
  https://generate-data-belajar-da-9ybp4njxabdmqtra27bkks.streamlit.app/

💡 Gunakan data dummy jika belum memiliki dataset sendiri, lalu upload ke dashboard untuk mencoba semua fitur.

---

---

## ✨ Fitur Utama

- 📁 **Unggah Data Otomatis**  
  Upload file CSV langsung dari antarmuka. Tersedia juga tombol unduh *Template CSV* di sidebar agar format tetap sesuai.

- 🕹️ **Filter Dinamis (Cascading)**  
  Filter berdasarkan Tahun, Bulan (Jan–Des), Kategori, dan Produk secara fleksibel.

- 📈 **Tren Omzet Real-Time**  
  Visualisasi *Area Chart* interaktif untuk melihat pergerakan omzet dari waktu ke waktu.

- 🏆 **Performa Komoditas & Kategori**  
  Analisis kontribusi produk dan kategori menggunakan *Bar Chart* dan *Donut Chart*.

- 📊 **Komparasi Bulanan**  
  Perbandingan omzet dan volume penjualan antar bulan dengan tabel rekap yang rapi.

---

## 📂 Struktur Direktori

    📁 belajar-da/
    │
    ├── app.py           # Entry point aplikasi Streamlit
    ├── data_cleaning.py # Data preprocessing & cleaning
    ├── eda_analysis.py  # Logika EDA & agregasi data
    ├── data_viz.py      # Visualisasi dengan Plotly
    └── README.md        # Dokumentasi proyek

---

## 🚀 Cara Menjalankan Proyek

### 1. Persiapan Lingkungan
Pastikan sudah menginstal Python versi **3.8+**. Disarankan menggunakan virtual environment.

### 2. Clone Repository

    git clone https://github.com/faizalrizqikholily/belajar-da.git
    cd belajar-da

### 3. Install Dependencies

    pip install streamlit pandas plotly

### 4. Jalankan Aplikasi

    streamlit run app.py

### 5. Akses di Browser

    http://localhost:8501

---

## 📝 Format Data (Penting!)

Pastikan file CSV memiliki struktur kolom berikut:

| Kolom               | Deskripsi |
|---------------------|----------|
| `tanggal`           | Format: YYYY-MM-DD (contoh: 2024-01-25) |
| `produk`            | Nama produk |
| `kategori`          | Kategori produk |
| `harga`             | Harga Produk |
| `jumlah`            | Kuantitas terjual |

💡 **Tips:**  
Gunakan fitur *Download Template CSV* di aplikasi agar format pasti sesuai.

---

## 🎯 Tujuan Proyek

Dashboard ini dibuat untuk:
- Mempermudah analisis penjualan tanpa tools kompleks
- Memberikan insight cepat berbasis data
- Mendukung pengambilan keputusan bisnis

---

## 📌 Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---

## 🙌 Kontribusi

Feel free untuk fork, improve, atau kasih feedback untuk pengembangan lebih lanjut 🚀


## 📬 Contact

Jika ingin berdiskusi, kolaborasi, atau memberikan feedback:

- 👤 **Faizal Rizqi Kholily**
- 💼 LinkedIn: https://www.linkedin.com/in/faizalrizqikholily/
- 📧 Email: faizalrzqkh@gmail.com

Terbuka untuk peluang kerja, freelance, maupun project kolaborasi 🚀
