# Step 6: Backend API Performance (S-Class)

**Objective:** < 50ms Latency for Dashboard Initialization.

## 1. Architectural Standards
*   **Pattern:** **BFF (Backend for Frontend)** Aggregation.
*   **Caching Strategy:** **Stale-While-Revalidate (SWR)** using Redis.
    *   Serve stale data immediately (`HIT`).
    *   Background fetch fresh data (`MISS` logic).
    *   Update cache.

## 2. Task Instructions

### A. Aggregated Endpoint (`GET /api/v1/dashboard/overview`)
*   **Purpose:** Eliminate Network Waterfall. One call for "Above the Fold" content.
*   **Payload:**
    ```json
    {
      "market_status": "Open",
      "indices": { "SPY": {...}, "QQQ": {...} },
      "fear_greed": { "value": 65, "label": "Greed" },
      "top_news": [ {...}, {...} ],
      "sector_performance": { "XLK": 1.2, "XLF": -0.5 }
    }
    ```
*   **Implementation:** Parallelize internal service calls using `asyncio.gather`.

### B. Granular Endpoints (Lazy Load)
*   **`GET /api/v1/market/tickers/{symbol}/analysis`**: Full quant analysis (Heavy compute).
*   **`GET /api/v1/market/screeners/vcp`**: Volatility Contraction candidates.

### C. Advanced Middleware
1.  **Rate Limiter:** Token Bucket algorithm (100 req/min/IP).
2.  **Response Compression:** Gzip/Brotli enabled for payloads > 1KB.

## 3. Verification
1.  **Latency Test:**
    *   `GET /overview` must return within **100ms** (Redis Hit).
2.  **Concurrency:**
    *   Run `locust` with 50 concurrent users. 99th percentile latency < 500ms.
