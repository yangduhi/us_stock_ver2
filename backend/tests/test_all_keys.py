import os
import requests
from dotenv import load_dotenv

load_dotenv()


def test_fred():
    print("\n[INFO] Testing FRED API Key...")
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("[SKIP] FRED_API_KEY not found.")
        return

    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={api_key}&file_type=json&limit=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "observations" in data and len(data["observations"]) > 0:
                print(
                    f"[PASS] FRED Success. Latest CPI Date: {data['observations'][0]['date']}"
                )
            else:
                print(f"[FAIL] FRED Empty Data: {data}")
        else:
            print(f"[FAIL] FRED Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] FRED Exception: {e}")


def test_fmp():
    print("\n[INFO] Testing Financial Modeling Prep (FMP) Key...")
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("[SKIP] FMP_API_KEY not found.")
        return

    # User provided: https://financialmodelingprep.com/stable/search-symbol?query=AAPL&apikey=...
    url = f"https://financialmodelingprep.com/stable/search-symbol?query=AAPL&apikey={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"[PASS] FMP Success. Found: {data[0].get('symbol', 'Unknown')}")
            else:
                print(f"[FAIL] FMP Empty/Invalid Data: {str(data)[:100]}")
        else:
            print(
                f"[FAIL] FMP Status Code: {response.status_code} - {response.text[:100]}"
            )
    except Exception as e:
        print(f"[FAIL] FMP Exception: {e}")


def test_finnhub():
    print("\n[INFO] Testing Finnhub Key...")
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        print("[SKIP] FINNHUB_API_KEY not found.")
        return

    url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "c" in data and data["c"] != 0:
                print(f"[PASS] Finnhub Success. Price: {data['c']}")
            else:
                print(f"[FAIL] Finnhub Data Issue: {data}")
        elif response.status_code == 403:
            print("[FAIL] Finnhub Forbidden (Check Key)")
        else:
            print(f"[FAIL] Finnhub Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Finnhub Exception: {e}")


if __name__ == "__main__":
    test_fred()
    test_fmp()
    test_finnhub()
