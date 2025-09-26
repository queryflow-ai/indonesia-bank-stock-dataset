# indonesia-bank-stock-dataset
Dataset historis harga saham bank di Indonesia yang dikumpulkan dari berbagai sumber publik seperti Bursa Efek Indonesia (IDX), Yahoo Finance, dan sumber data keuangan lainnya.

## Maintainer 
[@robbypambudi](https://github.com/robbypambudi)

## Yahoo Finance Scraper

Repository ini sekarang dilengkapi dengan scraper otomatis untuk mengambil data historis saham bank dari Yahoo Finance API.

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test scraper dengan satu saham
python scraper.py --test --mock

# Scrape semua saham bank (dengan data mock untuk testing)
python scraper.py --mock

# Jalankan example script
python example.py
```

### Fitur Scraper

- **Automatic bank filtering**: Otomatis memfilter saham bank dari daftar perusahaan
- **Multi-method fetching**: Menggunakan yfinance dan direct API calls
- **Mock data generation**: Untuk testing dan development
- **CSV export**: Output dalam format CSV yang mudah dianalisis
- **Error handling**: Robust handling untuk network dan API issues
- **Rate limiting**: Built-in delay untuk menghindari blocking

### Data Coverage

- **47 saham bank Indonesia** (dari AGRO.JK sampai MASB.JK)
- **Periode**: Januari 2004 - sekarang
- **Frequency**: Daily (hari kerja)
- **Data points**: Open, High, Low, Close, Volume, Adjusted Close

### Files

- `scraper.py` - Main scraper script
- `example.py` - Example usage
- `SCRAPER_README.md` - Detailed documentation
- `requirements.txt` - Python dependencies
- `profile/daftar-saham.csv` - List of Indonesian financial companies

### Usage Examples

```python
from scraper import YahooFinanceScraper

scraper = YahooFinanceScraper()

# Get data for BBRI
data = scraper.get_stock_data('BBRI.JK', start_date='2004-01-01')

# Scrape all banks
scraper.scrape_all_banks()
```

Lihat `SCRAPER_README.md` untuk dokumentasi lengkap.
