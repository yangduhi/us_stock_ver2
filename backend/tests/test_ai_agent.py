import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.ai_service import ai_service


def test_ai_agent():
    print("🤖 Testing AI Agent (News Analysis)...")
    ticker = "TSLA"
    # Simulated daily change
    change = -2.5

    print(f"Target: {ticker}, Change: {change}%")

    result = ai_service.analyze_news(ticker, change)

    print("\n=== AI Analysis Result ===")
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"Headlines: {len(result['headlines'])} found.")
        print("-" * 20)
        print(result["summary"])
        print("-" * 20)
        print("✅ AI Agent Test PASS")


if __name__ == "__main__":
    test_ai_agent()
