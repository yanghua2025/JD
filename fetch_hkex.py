
"""
fetch_hkex.py
--------------
Fetch official HKEX daily OHLC for a given stock code and write to 'latest_price.json'.
Requires 'requests' library.

Usage:
    python fetch_hkex.py --code 02618 --date 2025-05-06
"""
import argparse, datetime, json, requests, sys, pathlib

API_TEMPLATE = (
    "https://dce1hkexted.blob.core.windows.net/hquotes/CSV/{date}/{code}.csv"
    # Example: https://dce1hkexted.blob.core.windows.net/hquotes/CSV/2025-05-06/02618.csv
)

def fetch_csv(code: str, date: str):
    url = API_TEMPLATE.format(code=code, date=date)
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code} for {url}")
    return resp.text

def parse_ohlc(csv_text: str):
    # HKEX simple CSV: Date,Open,High,Low,Close,Volume
    line = csv_text.strip().splitlines()[-1]
    _, open_, high_, low_, close_, _ = line.split(",")
    return dict(open=float(open_), high=float(high_), low=float(low_), close=float(close_))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", required=True, help="Stock code, e.g., 02618")
    parser.add_argument("--date", help="YYYY-MM-DD, default=today HK")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d")

    try:
        csv_text = fetch_csv(args.code, date_str)
        ohlc = parse_ohlc(csv_text)
    except Exception as e:
        print("Fetch error:", e, file=sys.stderr)
        sys.exit(1)

    data = {
        "code": args.code,
        "date": date_str,
        "ohlc": ohlc
    }
    outfile = pathlib.Path(__file__).with_name("latest_price.json")
    outfile.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print("Saved", outfile)

if __name__ == "__main__":
    main()
