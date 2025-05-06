
# fetch_hkex.py
# --------------
# Download HKEX official CSV (anonymous) and save as latest_price.json
#
# Usage:
#   pip install requests
#   python fetch_hkex.py --code 02618             # default: today HK date
#   python fetch_hkex.py --code 02618 --date 2025-05-06
import argparse, datetime, json, pathlib, requests, sys

API = "https://dce1hkexted.blob.core.windows.net/hquotes/CSV/{date}/{code}.csv"

def fetch(code, date_str):
    url = API.format(code=code, date=date_str)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse(csv_text):
    # Date,Open,High,Low,Close,Volume
    line = csv_text.strip().splitlines()[-1]
    _, o, h, l, c, _ = line.split(",")
    return dict(open=float(o), high=float(h), low=float(l), close=float(c))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--code", required=True)
    p.add_argument("--date")
    args = p.parse_args()

    if args.date:
        date_str = args.date
    else:
        tz = datetime.timezone(datetime.timedelta(hours=8))
        date_str = datetime.datetime.now(tz).strftime("%Y-%m-%d")

    try:
        csv_text = fetch(args.code, date_str)
        ohlc = parse(csv_text)
    except Exception as e:
        print("Fetch error:", e, file=sys.stderr)
        sys.exit(1)

    data = {"code": args.code, "date": date_str, "ohlc": ohlc}
    pathlib.Path("latest_price.json").write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print("Saved latest_price.json")

if __name__ == "__main__":
    main()
