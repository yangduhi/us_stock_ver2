# Step 9: Caching (Mandatory)

**Objective:** Mask yfinance latency.

## 1. Task Instructions
1.  **Redis Setup:** Add `redis` to `docker-compose.yml`.
2.  **Middleware:**
    - **Long Cache (10m):** Sectors, Calendar, Smart Money, Earnings.
    - **Short Cache (1m):** Stock History, Crypto, Overview.
3.  **Logic:** Check Redis -> DB -> Redis.

## 2. Verification
**Performance Test:**
- First load: ~2.0s (Fetching data).
- Refresh: < 0.05s (Redis Hit).
> **Failure Condition:** If refresh takes > 1s, Step 9 is failed.
