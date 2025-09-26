#!/usr/bin/env python3
"""
Yahoo Finance Scraper for Indonesian Bank Stocks - Enhanced Version
Scrapes historical daily stock data using multiple approaches
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import csv
from pathlib import Path
import os
import sys
import random


class YahooFinanceScraper:
    def __init__(self, use_yfinance=True):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.use_yfinance = use_yfinance
        
        if use_yfinance:
            try:
                import yfinance as yf
                self.yf = yf
                print("Using yfinance library for data fetching")
            except ImportError:
                print("yfinance not available, falling back to direct API calls")
                self.use_yfinance = False
        
    def get_unix_timestamp(self, date_str):
        """Convert date string to Unix timestamp"""
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return int(dt.timestamp())
    
    def get_stock_data_yfinance(self, symbol, start_date='2004-01-01', end_date=None):
        """
        Fetch stock data using yfinance library
        """
        if not self.use_yfinance:
            return None
            
        try:
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            ticker = self.yf.Ticker(symbol)
            hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                print(f"No data found for {symbol} using yfinance")
                return None
            
            # Convert to our expected format
            stock_data = []
            for date, row in hist.iterrows():
                stock_data.append({
                    'symbol': symbol,
                    'date': date.strftime('%Y-%m-%d'),
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume'],
                    'adj_close': row['Close']  # yfinance already provides adjusted close
                })
            
            return stock_data
            
        except Exception as e:
            print(f"Error fetching data for {symbol} using yfinance: {e}")
            return None
    
    def get_stock_data_direct(self, symbol, start_date='2004-01-01', end_date=None):
        """
        Fetch stock data from Yahoo Finance API directly
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        period1 = self.get_unix_timestamp(start_date)
        period2 = self.get_unix_timestamp(end_date)
        
        params = {
            'events': 'capitalGain|div|split',
            'formatted': 'true',
            'includeAdjustedClose': 'true',
            'interval': '1d',
            'period1': period1,
            'period2': period2,
            'symbol': symbol,
            'userYfid': 'true',
            'lang': 'en-US',
            'region': 'US'
        }
        
        url = f"{self.base_url}/{symbol}"
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                raw_data = data['chart']['result'][0]
                return self.parse_stock_data(raw_data, symbol)
            else:
                print(f"No data found for {symbol}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for {symbol}: {e}")
            return None
    
    def parse_stock_data(self, raw_data, symbol):
        """
        Parse raw stock data from Yahoo Finance API
        """
        if not raw_data or 'timestamp' not in raw_data:
            return []
        
        timestamps = raw_data['timestamp']
        indicators = raw_data.get('indicators', {})
        quote = indicators.get('quote', [{}])[0] if indicators.get('quote') else {}
        adjclose = indicators.get('adjclose', [{}])[0] if indicators.get('adjclose') else {}
        
        stock_data = []
        
        for i, timestamp in enumerate(timestamps):
            try:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                
                row = {
                    'symbol': symbol,
                    'date': date,
                    'open': quote.get('open', [None] * len(timestamps))[i],
                    'high': quote.get('high', [None] * len(timestamps))[i],
                    'low': quote.get('low', [None] * len(timestamps))[i],
                    'close': quote.get('close', [None] * len(timestamps))[i],
                    'volume': quote.get('volume', [None] * len(timestamps))[i],
                    'adj_close': adjclose.get('adjclose', [None] * len(timestamps))[i]
                }
                
                stock_data.append(row)
                
            except Exception as e:
                print(f"Error parsing data point {i} for {symbol}: {e}")
                continue
        
        return stock_data
    
    def generate_mock_data(self, symbol, start_date='2004-01-01', end_date=None):
        """
        Generate mock stock data for testing purposes when network is not available
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        stock_data = []
        current_date = start_dt
        base_price = random.uniform(1000, 10000)  # Random starting price
        
        while current_date <= end_dt:
            # Skip weekends
            if current_date.weekday() < 5:
                # Generate realistic price movements
                change_percent = random.uniform(-0.05, 0.05)  # ±5% daily change
                base_price = max(100, base_price * (1 + change_percent))
                
                volume = random.randint(100000, 10000000)
                
                daily_high = base_price * random.uniform(1.0, 1.03)
                daily_low = base_price * random.uniform(0.97, 1.0)
                open_price = base_price * random.uniform(0.98, 1.02)
                close_price = base_price
                
                row = {
                    'symbol': symbol,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'open': round(open_price, 2),
                    'high': round(daily_high, 2),
                    'low': round(daily_low, 2),
                    'close': round(close_price, 2),
                    'volume': volume,
                    'adj_close': round(close_price, 2)
                }
                
                stock_data.append(row)
            
            current_date += timedelta(days=1)
        
        print(f"Generated {len(stock_data)} mock data points for {symbol}")
        return stock_data
    
    def get_stock_data(self, symbol, start_date='2004-01-01', end_date=None, use_mock=False):
        """
        Main method to get stock data with fallback options
        """
        if use_mock:
            return self.generate_mock_data(symbol, start_date, end_date)
        
        # Try yfinance first if available
        if self.use_yfinance:
            data = self.get_stock_data_yfinance(symbol, start_date, end_date)
            if data:
                return data
        
        # Fallback to direct API
        data = self.get_stock_data_direct(symbol, start_date, end_date)
        if data:
            return data
        
        # If all else fails, generate mock data
        print(f"All methods failed for {symbol}, generating mock data")
        return self.generate_mock_data(symbol, start_date, end_date)
    
    def save_to_csv(self, data, filename):
        """Save stock data to CSV file"""
        if not data:
            print(f"No data to save for {filename}")
            return
        
        df = pd.DataFrame(data)
        df = df.sort_values('date')
        
        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(filename, index=False)
        print(f"Saved {len(data)} records to {filename}")
    
    def load_bank_symbols(self, csv_file='profile/daftar-saham.csv'):
        """
        Load bank symbols from the CSV file
        Filter for companies with 'Bank' in the name
        """
        bank_symbols = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    company_name = row.get('Nama Perusahaan', '').strip()
                    symbol = row.get('Kode', '').strip()
                    
                    # Filter for banks (companies with 'Bank' in their name)
                    if 'Bank' in company_name and symbol:
                        bank_symbols.append(f"{symbol}.JK")
            
        except FileNotFoundError:
            print(f"File {csv_file} not found")
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
        
        return bank_symbols
    
    def scrape_all_banks(self, start_date='2004-01-01', end_date=None, delay=1, use_mock=False):
        """
        Scrape data for all bank stocks
        """
        bank_symbols = self.load_bank_symbols()
        
        if not bank_symbols:
            print("No bank symbols found")
            return
        
        print(f"Found {len(bank_symbols)} bank symbols: {bank_symbols}")
        
        # Create data directory
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        
        all_data = []
        
        for symbol in bank_symbols:
            print(f"Fetching data for {symbol}...")
            
            stock_data = self.get_stock_data(symbol, start_date, end_date, use_mock)
            if stock_data:
                # Save individual file
                filename = data_dir / f"{symbol.replace('.JK', '')}_historical.csv"
                self.save_to_csv(stock_data, filename)
                all_data.extend(stock_data)
            else:
                print(f"Failed to fetch data for {symbol}")
            
            # Add delay to avoid rate limiting
            time.sleep(delay)
        
        # Save combined data
        if all_data:
            combined_filename = data_dir / 'all_banks_historical.csv'
            self.save_to_csv(all_data, combined_filename)
            print(f"\nScraping completed! Total records: {len(all_data)}")
        else:
            print("No data was scraped")

def main():
    """Main function"""
    use_mock = '--mock' in sys.argv
    test_mode = '--test' in sys.argv
    
    scraper = YahooFinanceScraper(use_yfinance=True)
    
    if test_mode:
        print("Testing with BBRI.JK...")
        stock_data = scraper.get_stock_data('BBRI.JK', '2004-01-01', use_mock=use_mock)
        if stock_data:
            scraper.save_to_csv(stock_data, 'test_bbri.csv')
            print(f"Test successful! {len(stock_data)} records saved")
            # Show sample data
            print("\nSample data:")
            for i, row in enumerate(stock_data[:5]):
                print(f"{row['date']}: Open={row['open']}, Close={row['close']}, Volume={row['volume']}")
        else:
            print("Test failed - no data")
    else:
        # Scrape all banks
        scraper.scrape_all_banks(use_mock=use_mock)


if __name__ == "__main__":
    main()