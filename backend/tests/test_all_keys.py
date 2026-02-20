import os
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.integration
def test_fred():
    print("\n[INFO] Testing FRED API Key...")
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        pytest.skip("FRED_API_KEY not found.")

    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={api_key}&file_type=json&limit=1"
    response = requests.get(url, timeout=15)
    assert response.status_code == 200, f"FRED Status: {response.status_code}"
    data = response.json()
    assert "observations" in data and len(data["observations"]) > 0, (
        f"FRED Empty Data: {data}"
    )
    print(f"[PASS] FRED Success. Latest CPI Date: {data['observations'][0]['date']}")


@pytest.mark.integration
def test_fmp():
    print("\n[INFO] Testing Financial Modeling Prep (FMP) Key...")
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        pytest.skip("FMP_API_KEY not found.")

    # User provided: https://financialmodelingprep.com/stable/search-symbol?query=AAPL&apikey=...
    url = f"https://financialmodelingprep.com/stable/search-symbol?query=AAPL&apikey={api_key}"

    response = requests.get(url, timeout=15)
    assert response.status_code == 200, (
        f"FMP Status Code: {response.status_code} - {response.text[:100]}"
    )
    data = response.json()
    assert isinstance(data, list) and len(data) > 0, (
        f"FMP Empty/Invalid Data: {str(data)[:100]}"
    )
    print(f"[PASS] FMP Success. Found: {data[0].get('symbol', 'Unknown')}")


@pytest.mark.integration
def test_finnhub():
    print("\n[INFO] Testing Finnhub Key...")
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        pytest.skip("FINNHUB_API_KEY not found.")

    url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={api_key}"
    response = requests.get(url, timeout=15)
    assert response.status_code == 200, f"Finnhub Status: {response.status_code}"
    data = response.json()
    assert "c" in data and data["c"] != 0, f"Finnhub Data Issue: {data}"
    print(f"[PASS] Finnhub Success. Price: {data['c']}")


if __name__ == "__main__":
    test_fred()
    test_fmp()
    test_finnhub()
