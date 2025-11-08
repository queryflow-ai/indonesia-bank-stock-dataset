# ...existing code...
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_DIR = './datasets'

def process_profile(profile):
    profile_dir = os.path.join(INPUT_DIR, profile)
    json_dir = os.path.join(profile_dir, 'json')
    if not os.path.isdir(json_dir):
        return

    csv_path = os.path.join(profile_dir, f'{profile}.csv')

    rows = []
    for filename in os.listdir(json_dir):
        if not filename.endswith('.json'):
            continue
        filepath = os.path.join(json_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Urutkan kunci agar konsisten; ubah jika urutan lain diinginkan
            row = ','.join([str(data[k]) for k in sorted(data.keys())])
            rows.append(row)
        except Exception:
            # Lewatkan file rusak atau tidak bisa dibaca
            continue

    if rows:
        # Tulis ulang CSV sekali (hapus data lama)
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rows) + '\n')

def main():
    profiles = [p for p in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, p))]
    if not profiles:
        return

    max_workers = min(32, (os.cpu_count() or 1) + 4)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_profile, p) for p in profiles]
        for _ in as_completed(futures):
            pass

if __name__ == "__main__":
    main()
# ...existing code...