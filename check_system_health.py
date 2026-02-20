import asyncio
import httpx
import sys


async def check_health():
    print("Starting System Health Check...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Backend API
        try:
            resp = await client.get("http://localhost:8000/docs")
            if resp.status_code == 200:
                print("✅ Backend API: ONLINE (Docs Accessible)")
            else:
                print(f"❌ Backend API: FAILED ({resp.status_code})")
        except Exception as e:
            print(f"❌ Backend API: UNREACHABLE ({e})")

        # 2. Frontend UI
        try:
            resp = await client.get("http://localhost:3000")
            if resp.status_code == 200:
                print("✅ Frontend UI: ONLINE (Dashboard Accessible)")
            else:
                print(f"❌ Frontend UI: FAILED ({resp.status_code})")
        except Exception as e:
            print(f"❌ Frontend UI: UNREACHABLE ({e})")

        # 3. Data Flow (BFF Endpoint)
        try:
            resp = await client.get("http://localhost:8000/api/v1/dashboard/overview")
            if resp.status_code == 200:
                data = resp.json()
                if "indices" in data and "sectors" in data:
                    print(
                        f"✅ Data Flow: ONLINE (Indices: {len(data['indices'])}, Sectors: {len(data['sectors'])})"
                    )
                else:
                    print("⚠️ Data Flow: PARTIAL (Missing Keys)")
            else:
                print(f"❌ Data Flow: FAILED ({resp.status_code})")
        except Exception as e:
            print(f"❌ Data Flow: UNREACHABLE ({e})")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_health())
