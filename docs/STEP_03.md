# Step 3: Data Pipeline Reliability (S-Class)

**Objective:** "Unbreakable" Data Ingestion with Precision Time-Sync.

## 1. Architectural Standards
*   **Resilience:**
    *   **Exponential Backoff:** If `yfinance` returns 429/500, wait `2^n + jitter` seconds before retry. Max 5 retries.
    *   **Circuit Breaker:** If 50% of requests fail in 1 minute, pause pipeline for 10 minutes.
*   **Data Integrity:**
    *   **Timezone:** ALL schedulers must use `America/New_York` (EST/EDT).
    *   **Validation:** Use `Pydantic` models to validate every row before DB insertion. Drop invalid rows & log warning.

## 2. Task Instructions

### A. Advanced Fetcher Service (`backend/app/services/fetcher.py`)
1.  **Retry Decorator:** Implement `@retry_with_backoff(retries=5, delay=2)` wrapper.
2.  **Batching:**
    *   Split 500+ tickers into chunks of 50.
    *   Parallel execution using `asyncio.gather` with semaphore (max 5 concurrent calls) to respect rate limits.

### B. Multi-Tier Scheduler (`backend/app/scheduler.py`)
*   **Real-time (Market Data):**
    - `CronTrigger(minute='*/1', timezone='America/New_York')` (during market hours).
    - Target: `yfinance` (Price/Volume).
*   **Daily (Macro & Sentiment):**
    - `CronTrigger(hour=18, minute=0)` (Post-market).
    - Target: `FRED` (Treasury Yields, CPI) & `FearGreed`.
*   **Weekly (Fundamentals):**
    - `CronTrigger(day_of_week='sat', hour=10)` (Weekend batch).
    - Target: `FMP` (Balance Sheet, Income Statement) -> Update `Financials` table.

### C. Validation Layer (`backend/app/schemas/market.py`)
*   Define `MarketDataSchema`:
    *   `close`: float (> 0)
    *   `volume`: int (>= 0)
*   Define `FinancialsSchema`:
    *   `revenue`: float (allow negative? No, but `net_income` can be negative).
    *   `period`: date (must be quartely end).

## 3. Verification
1.  **Chaos Engineering:**
    *   Disconnect Internet -> Run Fetcher -> Verify Retry Logs.
    *   Reconnect -> Verify successful recovery.
2.  **Data Quality:**
    *   Query DB: `SELECT * FROM market_data WHERE close <= 0;` (Should be 0 rows).
