import os
import yfinance as yf
from fredapi import Fred
from google import genai
from dotenv import load_dotenv

# Load Env
load_dotenv()


def log(msg, status="INFO"):
    print(f"[{status}] {msg}")
    with open("backend/tests/validation.log", "a", encoding="utf-8") as f:
        f.write(f"[{status}] {msg}\n")


def test_stocks():
    log("Testing Stock Data (AAPL)...")
    try:
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="5d")
        if not hist.empty:
            log(f"Success. Last Close: {hist['Close'].iloc[-1]:.2f}", "PASS")
        else:
            log("Failed to fetch history.", "FAIL")
    except Exception as e:
        log(f"Error: {e}", "FAIL")


def test_sectors():
    log("Testing Sector Proxies (XLK, XLE)...")
    try:
        tickers = ["XLK", "XLE"]
        for t in tickers:
            ticker = yf.Ticker(t)
            hist = ticker.history(period="2d")
            if not hist.empty:
                change = (
                    (hist["Close"].iloc[-1] - hist["Close"].iloc[0])
                    / hist["Close"].iloc[0]
                ) * 100
                log(f"Success. {t} Change: {change:.2f}%", "PASS")
            else:
                log(f"Failed to fetch {t} data.", "FAIL")
    except Exception as e:
        log(f"Error: {e}", "FAIL")


def test_macro():
    log("Testing FRED API (CPIAUCSL, UNRATE)...")
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        log("FRED_API_KEY not found in .env", "SKIP")
        return

    try:
        fred = Fred(api_key=api_key)
        series_ids = ["CPIAUCSL", "UNRATE"]
        for sid in series_ids:
            data = fred.get_series(sid, limit=1)
            if not data.empty:
                log(f"Success. Latest {sid}: {data.iloc[-1]}", "PASS")
            else:
                log(f"FRED returned empty data for {sid}.", "FAIL")
    except Exception as e:
        log(f"Error: {e}", "FAIL")


def test_calendar():
    log("Testing Earnings Calendar (TSLA)...")
    try:
        tsla = yf.Ticker("TSLA")
        cal = tsla.calendar
        # Handle dict or DataFrame
        if isinstance(cal, dict):
            if cal:
                log(
                    f"Success. Calendar fetched (dict). Keys: {list(cal.keys())[:3]}",
                    "PASS",
                )
            else:
                log("Calendar dict is empty.", "WARN")
        elif hasattr(cal, "empty"):
            if not cal.empty:
                log("Success. Calendar fetched (DataFrame).", "PASS")
            else:
                log("Calendar DataFrame is empty.", "WARN")
        else:
            log(f"Calendar format unknown: {type(cal)}", "WARN")
    except Exception as e:
        log(f"Error: {e}", "FAIL")


def test_smart_money():
    log("Testing Institutional Holders (NVDA)...")
    try:
        nvda = yf.Ticker("NVDA")
        holders = nvda.institutional_holders
        if holders is not None and not holders.empty:
            # Handle potential different column names
            if "Holder" in holders.columns:
                top_holder = holders.iloc[0]["Holder"]
            else:
                top_holder = holders.iloc[0][0]  # Fallback
            log(f"Success. Top Holder: {top_holder}", "PASS")
        else:
            log("Failed to fetch holders.", "FAIL")
    except Exception as e:
        log(f"Error: {e}", "FAIL")


def test_ai():
    log("Testing Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log("GEMINI_API_KEY not found in .env", "SKIP")
        return

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents="Hello"
        )
        text = getattr(response, "text", "")
        if text:
            log(f"Success. Response: {text.strip()[:50]}...", "PASS")
        else:
            log("No response text.", "FAIL")
    except Exception as e:
        log(f"Error: {e}", "FAIL")


def main():
    print("=== MarketFlow Data Source Validation ===")
    test_stocks()
    print("-" * 30)
    test_sectors()
    print("-" * 30)
    test_macro()
    print("-" * 30)
    test_calendar()
    print("-" * 30)
    test_smart_money()
    print("-" * 30)
    test_ai()
    print("=== Validation Complete ===")


if __name__ == "__main__":
    main()
