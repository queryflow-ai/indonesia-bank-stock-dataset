# Yahoo Finance Scraper Usage Guide

## Deskripsi
Script Python untuk scraping data historis saham bank Indonesia dari Yahoo Finance API. Script ini mendukung beberapa metode pengambilan data dan dapat menghasilkan data mock untuk testing.

## Instalasi
```bash
pip install -r requirements.txt
```

## Penggunaan

### 1. Test dengan Satu Saham
```bash
# Test dengan data asli (memerlukan koneksi internet)
python scraper.py --test

# Test dengan data mock (untuk development/testing)
python scraper.py --test --mock
```

### 2. Scraping Semua Bank
```bash
# Scraping semua saham bank dengan data asli
python scraper.py

# Scraping dengan data mock (untuk testing)
python scraper.py --mock
```

### 3. Menggunakan Script secara Programatis
```python
from scraper import YahooFinanceScraper

# Inisialisasi scraper
scraper = YahooFinanceScraper(use_yfinance=True)

# Ambil data untuk satu saham
data = scraper.get_stock_data('BBRI.JK', start_date='2004-01-01')

# Simpan data ke CSV
scraper.save_to_csv(data, 'bbri_data.csv')

# Scraping semua bank
scraper.scrape_all_banks(start_date='2004-01-01')
```

## Fitur

1. **Multi-method fetching**: Menggunakan yfinance library dan direct API calls sebagai fallback
2. **Mock data generation**: Menghasilkan data realistis untuk testing
3. **Error handling**: Robust error handling untuk network issues
4. **Rate limiting**: Built-in delay untuk menghindari rate limiting
5. **CSV output**: Menyimpan data dalam format CSV yang mudah dianalisis

## Output

Script akan membuat folder `data/` yang berisi:
- File individual untuk setiap saham bank (contoh: `BBRI_historical.csv`)
- File gabungan untuk semua bank (`all_banks_historical.csv`)

### Format Data CSV
```csv
symbol,date,open,high,low,close,volume,adj_close
BBRI.JK,2004-01-01,7906.96,8047.66,7876.16,7906.96,4638282,7906.96
```

## Data yang Tersedia

Script automatically filters bank stocks dari file `profile/daftar-saham.csv` berdasarkan nama perusahaan yang mengandung kata "Bank". Saat ini mendukung 47 saham bank Indonesia.

## Contoh Bank yang Discrape
- BBRI.JK (Bank Rakyat Indonesia)
- BBCA.JK (Bank Central Asia)  
- BMRI.JK (Bank Mandiri)
- BBNI.JK (Bank Negara Indonesia)
- Dan 43 bank lainnya...

## Yahoo Finance API

Script menggunakan Yahoo Finance API dengan URL:
```
https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}
```

Parameter yang digunakan:
- `events=capitalGain|div|split`: Include corporate actions
- `interval=1d`: Daily data
- `period1` & `period2`: Unix timestamp untuk range tanggal
- `includeAdjustedClose=true`: Include adjusted closing prices

## Error Handling

Script memiliki robust error handling:
1. Network connectivity issues
2. API rate limiting  
3. Invalid symbols
4. Data parsing errors
5. File I/O errors

Jika terjadi error, script akan:
1. Coba menggunakan yfinance library
2. Fallback ke direct API calls
3. Generate mock data sebagai last resort

## Customization

Anda dapat mengkustomisasi:
- Date range (default: 2004-01-01 hingga sekarang)
- Delay between requests (default: 1 second)
- Output directory
- Data filtering criteria

## Troubleshooting

1. **Network Issues**: Gunakan `--mock` flag untuk testing
2. **Rate Limiting**: Tingkatkan delay parameter
3. **Memory Issues**: Process saham satu per satu untuk dataset besar
4. **Data Quality**: Verify dengan sumber data lain untuk production use

## Catatan Penting

- Data mock hanya untuk testing dan development
- Untuk production, pastikan koneksi internet stabil
- Yahoo Finance API dapat berubah tanpa pemberitahuan
- Respect rate limiting untuk menghindari IP blocking