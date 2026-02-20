import pytest
from httpx import AsyncClient, ASGITransport
import asyncio
from backend.app.main import app

# This test requires the server to be running or using TestClient/AsyncClient
# We will use AsyncClient with the app directly


@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_dashboard_overview():
    print("\n🧪 Testing Dashboard Overview BFF...")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/dashboard/overview")

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Keys: {list(data.keys())}")
        assert "indices" in data
        assert "sectors" in data
        print("✅ Dashboard Overview PASS")
    else:
        print(f"❌ Dashboard Failed: {response.text}")
        assert False


@pytest.mark.asyncio
async def test_ticker_analysis():
    print("\n🧪 Testing Ticker Analysis (AAPL)...")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/market/tickers/AAPL/analysis")

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Score: {data.get('score')}")
        assert "score" in data
        assert "signals" in data
        print("✅ Ticker Analysis PASS")
    else:
        print(f"❌ Analysis Failed: {response.text}")
        with open("api_test_debug.log", "w", encoding="utf-8") as f:
            f.write(f"Status: {response.status_code}\n")
            f.write(f"Response: {response.text}\n")
        assert False


if __name__ == "__main__":
    # Manually run async tests if called as script
    async def run_tests():
        await test_root()
        await test_dashboard_overview()
        await test_ticker_analysis()

    asyncio.run(run_tests())
