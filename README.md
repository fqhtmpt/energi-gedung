# 🔌 Analisis Konsumsi Energi Gedung

Aplikasi berbasis **Streamlit** buat analisis konsumsi energi dari data Excel. Cocok dipakai buat teknisi atau tim operasional gedung yang pengen tahu pemakaian listrik harian, mingguan, atau bulanan dengan lebih mudah dan visual.

---

## ⚙️ Fitur Utama

✅ Upload file Excel berisi data energi  
✅ Tampilkan data mentah dalam bentuk tabel  
✅ Hitung statistik deskriptif otomatis  
✅ Visualisasi grafik tren konsumsi energi  
✅ Download hasil analisis ke file Excel

---

## 🚀 Cara Pakai Aplikasi

1. **Clone repo ini** ke komputer kamu:
   ```bash
   git clone https://github.com/fqhtmpt/energi-gedung.git
   cd energi-gedung
   ```

2. **Aktifin virtual environment (opsional tapi direkomendasiin)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install library yang dibutuhin**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasinya pake Streamlit**:
   ```bash
   streamlit run app.py
   ```

---

## 📂 Struktur Folder

| File/Folder         | Penjelasan                                  |
|---------------------|----------------------------------------------|
| `app.py`            | Script utama Streamlit                       |
| `style.css`         | Custom styling buat tampilan (opsional)      |
| `requirements.txt`  | Daftar pustaka Python yang dipakai           |
| `hasil_analisis.xlsx` | Contoh hasil analisis (Excel)             |
| `.devcontainer/`    | Setting Dev Container (jika dipakai)         |

---

## 📊 Format Data yang Diterima

File Excel (.xlsx) minimal punya dua kolom:
- `Tanggal` → berisi tanggal pemakaian
- `Konsumsi Energi` → nilai kWh/hari

Contoh:

| Tanggal    | Konsumsi Energi |
|------------|------------------|
| 2024-01-01 | 125              |
| 2024-01-02 | 132              |

---

## 👨‍💻 Dibuat Oleh

**Muhammad Fiqih Tampati**  
🧠 Magang Teknik Gedung • Mainan Data & Streamlit

GitHub: [https://github.com/fqhtmpt](https://github.com/fqhtmpt)

---

## 📄 Lisensi

Proyek ini dilisensikan dengan [MIT License](LICENSE) – bebas dipake, dimodif, atau dikembangin.

---
