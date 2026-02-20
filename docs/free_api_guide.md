# Zero-Cost Data Strategy Guide (S-Class)

**Version:** 1.0.0
**Status:** Active Strategy
**Objective:** Build an institutional-grade investment dashboard using only free data tiers.

---

## 1. Core Architecture: The "Hybrid Proxy" Model

To overcome rate limits and data delays inherent in free APIs, we use a hybrid approach:
*   **Live/Intraday:** `yfinance` (Scraper-based, 1-min delay)
*   **Fundamentals:** `Financial Modeling Prep` (Limit 250/day) + `Finnhub` (Limit 60/min)
*   **Macro:** `FRED` (Official US Gov, Limitless)
*   **Sentiment:** `Fear & Greed` (CNN Proxy)

## 2. Data Source Breakdown

### A. Market Data (Price & Volume)
*   **Primary:** `yfinance` (Yahoo Finance API Proxy)
    *   **Limits:** None (Technical). Avoid IP bans only.
    *   **Data:** OHLCV (1m, 5m, 1h, 1d), Splits, Dividends.
    *   **Strategy:** Fetch batch history overnight. Stream 1m interval only for active dashboard view.

### B. Fundamental Data (Valuation & Health)
*   **Primary:** `Financial Modeling Prep (FMP)` (Free Tier)
    *   **Key:** Required (Get from [site](https://site.financialmodelingprep.com/developer)).
    *   **Limits:** 250 requests/day.
    *   **Strategy:** **Do not fetch on load.** Fetch once per week per ticker and cache in TimescaleDB.
    *   **EndPoints:** `/ratios`, `/income-statement`, `/balance-sheet-statement`.

### C. Macroeconomic Indicators
*   **Primary:** `FRED API` (St. Louis Fed)
    *   **Key:** Required (Get from [site](https://fred.stlouisfed.org/docs/api/api_key.html)).
    *   **Limits:** High (effectively unlimited for this use).
    *   **Strategy:** Fetch daily via Scheduler (See `backend/app/scheduler.py`).
    *   **Series IDs:**
        *   `CPIAUCSL`: CPI (Inflation)
        *   `UNRATE`: Unemployment Rate
        *   `DGS10`: 10-Year Treasury Yield
        *   `FEDFUNDS`: Federal Funds Rate

### D. Corporate Actions & News
*   **Primary:** `Finnhub` (Free Tier)
    *   **Key:** Required.
    *   **Limits:** 60 calls/minute.
    *   **Data:** Insider Trading, Company Profile.
*   **Secondary:** `yfinance` Calendar
    *   **Data:** Earnings Dates.

## 3. Implementation Status (Phase 1)

| Category | Source | Implemented? | Notes |
| :--- | :--- | :--- | :--- |
| **Stocks** | yfinance | ✅ Yes | `fetcher.py` handles batching. |
| **Sectors** | yfinance | ✅ Yes | Proxies (XLK, XLE, etc.) used. |
| **Macro** | FRED | ⚠️ Partial | `test_data_source.py` added, but **API Key missing**. |
| **Fundamentals**| FMP | ⏳ Pending | DB Schema (`Financials`) ready. Fetcher pending. |
| **Sentiment** | AI/Crawl | ⏳ Pending | DB Schema (`MarketSentiment`) ready. |

## 4. Action Items
1.  **Add Keys:** Add `FRED_API_KEY` and `FMP_API_KEY` to `.env`.
2.  **Verify FRED:** Run `backend/tests/test_data_source.py`.
3.  **Implement FMP Fetcher:** Add to `backend/app/services/fetcher.py`.
