import argparse, json, pathlib, datetime, requests, sys

def fetch_yahoo(code):
    # Yahoo 需要加 .HK
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{code}.HK?range=1d&interval=1d"
    data = requests.get(url, timeout=10).json()
    quote = data["chart"]["result"][0]
    ohlc = quote["indicators"]["quote"][0]
    open_, high_, low_, close_ = (
        ohlc["open"][0],
        ohlc["high"][0],
        ohlc["low"][0],
        ohlc["close"][0],
    )
    return dict(open=open_, high=high_, low=low_, close=close_)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--code", required=True)         # 5-digit, e.g. 02618
    args = p.parse_args()

    try:
        ohlc = fetch_yahoo(args.code.lstrip("0"))
    except Exception as e:
        print("Fetch error:", e, file=sys.stderr)
        sys.exit(1)

    date_str = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d")
    pathlib.Path("latest_price.json").write_text(
        json.dumps({"code": args.code, "date": date_str, "source": "Yahoo", "ohlc": ohlc}, indent=2)
    )
    print("Saved latest_price.json")

if __name__ == "__main__":
    main()
