import asyncio
import sys
import os
import pandas as pd

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.fetcher import fetcher
from backend.app.services.analyzer import quant_analyzer


async def test_quant():
    print("🧪 Testing Quant Engine...")
    ticker = "AAPL"

    # 1. Fetch Data
    print(f"Fetching data for {ticker}...")
    try:
        data = await fetcher.fetch_batch_history([ticker], period="1y")

        if data.empty:
            print("❌ No data fetched.")
            return

        # Handle MultiIndex if present (yfinance group_by='ticker')
        if isinstance(data.columns, pd.MultiIndex):
            df = data[ticker].copy()
        else:
            df = data.copy()

        # 2. Analyze
        print("Running Analysis...")
        result = quant_analyzer.analyze(df)

        # 3. Output
        print("\n=== Analysis Result ===")
        print(f"Symbol: {ticker}")
        print(f"Date: {result['date']}")
        print(f"Price: ${result['price']:.2f}")
        print(f"Score: {result['score']} ({result['label']})")
        print(f"Signals: {result['signals']}")
        print(f"RSI: {result['indicators']['rsi']:.2f}")
        print("=======================\n")

        if result["score"] > 0:
            print("✅ Quant Engine Test PASS")
        else:
            print("⚠️ Quant Engine Test WARN (Score 0?)")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_quant())
