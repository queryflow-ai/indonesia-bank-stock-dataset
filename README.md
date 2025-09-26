# 🇮🇩 Indonesia Bank Stock Dataset

Dataset harian saham perbankan Indonesia yang dikumpulkan secara otomatis dari [Yahoo Finance](https://finance.yahoo.com/) dan daftar emiten resmi [IDX](https://www.idx.co.id/).

> Repo ini dibuat untuk kebutuhan riset, analisis pasar modal, machine learning, dan pembelajaran.  
> Data diperbarui **setiap hari pukul 20:00 WIB** melalui [GitHub Actions](.github/workflows/update.yml).

## 📂 Struktur Folder


```bash
├── .github/
│ └── workflows/
│ └── update.yml # workflow GitHub Actions
│
├── profile/
│ └── daftar_saham.csv # daftar kode emiten (input utama)
│
├── datasets/ # hasil scraping (otomatis update harian)
│ ├── BBRI/
│ │ ├── 02-01-2004.json
│ │ ├── 03-01-2004.json
│ │ └── ...
│ ├── BBCA/
│ │ ├── 02-01-2004.json
│ │ └── ...
│ └── ...
│
├── scrape.py # script scraping Yahoo Finance
├── requirements.txt # dependency Python
├── errors.log # log error scraping (opsional)
└── README.md # dokumentasi proyek
```

## ⚙️ Cara Menjalankan Scraper

1. **Clone repo**
```bash
git clone https://github.com/queryflow-ai/indonesia-bank-stock-dataset.git
cd indonesia-bank-stock-dataset
```

2. **Install dependencies**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

3. **Jalankan scraper**
```bash
python scrape.py
```



## 🤖Otomatisasi via GitHub Actions

- Repo ini memiliki workflow otomatis:
    - 📅 Jadwal: setiap hari pukul 20:00 WIB (13:00 UTC)
    - ⚡ Scraper dijalankan di server GitHub
    - 💾 Dataset terbaru di-commit ke branch utama jika ada perubahan

Lihat file [update.yml](https://github.com/queryflow-ai/indonesia-bank-stock-dataset/blob/main/.github/workflows/update.yml) untuk detail konfigurasi.

## 📝 Daftar Saham Bank

Daftar emiten diambil dari file profile/daftar_saham.csv
.
Contoh format:
```csv
No,Kode,Nama Perusahaan,Tanggal Pencatatan,Saham,Papan Pencatatan
1,BBRI,Bank Rakyat Indonesia Tbk.,10 Nov 2003,12345678900,Utama
2,BBCA,Bank Central Asia Tbk.,31 Mei 2000,25000000000,Utama
3,BNI,Bank Negara Indonesia Tbk.,25 Nov 1996,18700000000,Utama
```

### 📌 Roadmap

- Scraping Yahoo Finance per hari sejak 2004
- Otomatis update via GitHub Actions
- Konversi dataset ke format CSV / Parquet
- Tambah analisis sederhana (moving average, return harian)
- Dokumentasi API sederhana untuk konsumsi dataset

## Maintainer 
[@robbypambudi](https://github.com/robbypambudi)
