import os
import csv
import json
import time
import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# === CONFIG ===
CSV_FILE = "./profile/daftar_saham.csv"   # file CSV dengan formatmu
OUTPUT_DIR = "./datasets"                 # folder output utama
START_DATE = datetime(2004, 1, 1, tzinfo=timezone.utc)
MAX_WORKERS = 8                           # jumlah thread paralel
ERROR_LOG = "errors.log"                  # file log error

# === HELPER ===
def unix_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())

def download_yahoo_chart(symbol: str, start: datetime, end: datetime):
    """Ambil data chart Yahoo Finance untuk 1 emiten"""
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        "?interval=1d&events=capitalGain|div|split"
        "&formatted=true&includeAdjustedClose=true"
        "&period1={p1}&period2={p2}&lang=en-US&region=US"
    ).format(
        symbol=symbol,
        p1=unix_timestamp(start),
        p2=unix_timestamp(end),
    )

    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"Failed {symbol}: {resp.status_code}")
    return resp.json()

def process_symbol(row, today: str):
    """Worker function untuk 1 ticker"""
    kode = row["Kode"].strip()
    nama = row["Nama Perusahaan"].strip()
    symbol = f"{kode}.JK"

    outdir = os.path.join(OUTPUT_DIR, kode)
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, f"{today}.json")

    # Resume check
    if os.path.exists(outfile):
        print(f"Skipping {symbol} ({nama}) — already exists.")
        return

    print(f"Fetching {symbol} ({nama})...")

    try:
        data = download_yahoo_chart(symbol, START_DATE, datetime.now(timezone.utc))

        with open(outfile, "w", encoding="utf-8") as fjson:
            json.dump(data, fjson, ensure_ascii=False, indent=2)

        print(f"  -> Saved {outfile}")
    except Exception as e:
        err_msg = f"Error {symbol}: {e}"
        print(f"  !! {err_msg}")
        # simpan ke log error
        with open(ERROR_LOG, "a", encoding="utf-8") as ferr:
            ferr.write(f"{datetime.now()} - {err_msg}\n")

    # Rate limiting kecil
    time.sleep(0.5)

def main():
    today = datetime.now().strftime("%d-%m-%Y")

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_symbol, row, today) for row in reader]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                # catch error yang lepas dari worker
                with open(ERROR_LOG, "a", encoding="utf-8") as ferr:
                    ferr.write(f"{datetime.now()} - Future error: {e}\n")

if __name__ == "__main__":
    main()
