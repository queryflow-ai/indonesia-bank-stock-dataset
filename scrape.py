import os
import csv
import json
import time
import requests
import argparse
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# === CONFIG ===
CSV_FILE = "./profile/daftar_saham.csv"
OUTPUT_DIR = "./datasets"
MAX_WORKERS = 8
ERROR_LOG = "errors.log"
START_DATE = datetime(2004, 1, 1, tzinfo=timezone.utc)

# === HELPER ===
def unix_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())

def download_yahoo_chart(symbol: str, start: datetime, end: datetime):
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

def save_daily_json(data, kode, nama):
    """Simpan data ke file per tanggal (JSON harian)"""
    result = data.get("chart", {}).get("result", [])
    if not result:
        raise Exception("No result in JSON")

    res = result[0]
    timestamps = res.get("timestamp", [])
    quotes = res.get("indicators", {}).get("quote", [{}])[0]

    outdir_json = os.path.join(OUTPUT_DIR, kode, "json")
    os.makedirs(outdir_json, exist_ok=True)

    records = []
    saved = 0
    for i, ts in enumerate(timestamps):
        dt_obj = datetime.fromtimestamp(ts, tz=timezone.utc)
        if dt_obj.weekday() >= 5:  # skip weekend
            continue

        date_str = dt_obj.strftime("%Y-%m-%d")
        json_file = os.path.join(outdir_json, f"{date_str}.json")

        record = {
            "kode": kode,
            "nama": nama,
            "date": date_str,
            "open": quotes.get("open", [None])[i],
            "high": quotes.get("high", [None])[i],
            "low": quotes.get("low", [None])[i],
            "close": quotes.get("close", [None])[i],
            "volume": quotes.get("volume", [None])[i],
        }

        # Save JSON harian (skip kalau sudah ada)
        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as fjson:
                json.dump(record, fjson, ensure_ascii=False, indent=2)
            saved += 1

        records.append(record)

    return records, saved

def process_symbol(row, fetch_all: bool):
    kode = row["Kode"].strip()
    nama = row["Nama Perusahaan"].strip()
    symbol = f"{kode}.JK"

    print(f"Fetching {symbol} ({nama})...")

    try:
        end = datetime.now(timezone.utc)
        if fetch_all:
            start = START_DATE
        else:
            start = end - timedelta(days=5)  # default hanya beberapa hari terakhir

        raw = download_yahoo_chart(symbol, start, end)
        records, saved = save_daily_json(raw, kode, nama)
        print(f"  -> {symbol} saved {saved} new JSON files")
        return kode, records
    except Exception as e:
        err_msg = f"Error {symbol}: {e}"
        print(f"  !! {err_msg}")
        with open(ERROR_LOG, "a", encoding="utf-8") as ferr:
            ferr.write(f"{datetime.now()} - {err_msg}\n")
        return kode, []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Scrape full data from 2004 until now")
    args = parser.parse_args()

    all_data = {}

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_symbol, row, args.all): row["Kode"].strip() for row in reader}
        for future in as_completed(futures):
            try:
                kode, records = future.result()
                all_data.setdefault(kode, []).extend(records)
            except Exception as e:
                with open(ERROR_LOG, "a", encoding="utf-8") as ferr:
                    ferr.write(f"{datetime.now()} - Future error: {e}\n")

if __name__ == "__main__":
    main()
