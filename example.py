#!/usr/bin/env python3
"""
Contoh penggunaan Yahoo Finance Scraper untuk saham bank Indonesia
Example usage of Yahoo Finance Scraper for Indonesian bank stocks
"""

from scraper import YahooFinanceScraper
import pandas as pd
from pathlib import Path

def main():
    # Initialize scraper
    scraper = YahooFinanceScraper(use_yfinance=True)
    
    print("=== Yahoo Finance Scraper Example ===")
    print()
    
    # Example 1: Get data for a single stock
    print("1. Mengambil data untuk BBRI.JK...")
    bbri_data = scraper.get_stock_data('BBRI.JK', start_date='2020-01-01', use_mock=True)
    
    if bbri_data:
        print(f"   Berhasil mendapatkan {len(bbri_data)} records untuk BBRI.JK")
        print(f"   Data dari {bbri_data[0]['date']} sampai {bbri_data[-1]['date']}")
        
        # Save individual stock data
        scraper.save_to_csv(bbri_data, 'example_bbri.csv')
        
        # Show sample data
        print("\n   Sample data:")
        for i, row in enumerate(bbri_data[:3]):
            print(f"   {row['date']}: Open={row['open']}, Close={row['close']}, Volume={row['volume']}")
    else:
        print("   Gagal mendapatkan data untuk BBRI.JK")
    
    print()
    
    # Example 2: Get list of bank symbols
    print("2. Mendapatkan daftar simbol bank...")
    bank_symbols = scraper.load_bank_symbols()
    print(f"   Ditemukan {len(bank_symbols)} simbol bank:")
    print(f"   {', '.join(bank_symbols[:10])}...")  # Show first 10
    
    print()
    
    # Example 3: Process a few banks with mock data
    print("3. Memproses beberapa saham bank (dengan data mock)...")
    sample_banks = bank_symbols[:5]  # Process first 5 banks
    all_data = []
    
    for symbol in sample_banks:
        print(f"   Memproses {symbol}...")
        stock_data = scraper.get_stock_data(symbol, start_date='2023-01-01', use_mock=True)
        
        if stock_data:
            all_data.extend(stock_data)
            print(f"     ✓ {len(stock_data)} records")
        else:
            print(f"     ✗ Gagal")
    
    if all_data:
        # Save combined data
        scraper.save_to_csv(all_data, 'example_combined.csv')
        print(f"   Total records: {len(all_data)}")
        
        # Create a simple analysis
        df = pd.DataFrame(all_data)
        print("\n   Analisis sederhana:")
        print(f"   - Jumlah saham: {df['symbol'].nunique()}")
        print(f"   - Periode data: {df['date'].min()} s/d {df['date'].max()}")
        print(f"   - Rata-rata volume: {df['volume'].mean():,.0f}")
        
        # Show price ranges by symbol
        price_stats = df.groupby('symbol')['close'].agg(['min', 'max', 'mean']).round(2)
        print("\n   Statistik harga (min/max/rata-rata):")
        for symbol, stats in price_stats.iterrows():
            print(f"   {symbol}: {stats['min']} / {stats['max']} / {stats['mean']}")
    
    print()
    print("=== Selesai ===")
    print()
    print("File yang dibuat:")
    files = ['example_bbri.csv', 'example_combined.csv']
    for file in files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"  - {file} ({size:,} bytes)")

if __name__ == "__main__":
    main()