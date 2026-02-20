# Step 1: Zero-Cost Data Source Strategy

**Objective:** Validate fetching data using `yfinance` and `fredapi` proxies, and understand the free API landscape.

## 1. Zero-Cost API Landscape & Strategy

To build an enterprise-grade dashboard without cost, we must hybridize data sources to overcome rate limits and data delays.

> [!NOTE]
> Most free APIs have **Rate Limits** or **15-min Delays**. We use a **Hybrid Strategy** to mitigate this.

### A. Price & Chart Data (The Core)
| Service | Best For | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Yahoo Finance** (`yfinance`) | **Main Feed** | Unlimited calls, 1-min intervals, extensive history. | Scraper-based (watch for library updates). |
| **Alpha Vantage** | Backup | Server-side technical indicators. | Strict limit (25 req/day). |
| **Polygon.io** | Reference | High quality documentation. | Free tier is EOD (End-of-Day) only. |

### B. Fundamentals (The Analysis)
| Service | Best For | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Financial Modeling Prep** | **Valuation** | Clean PER, ROE, DCF data. | 250 req/day limit. **Batch this.** |
| **Finnhub.io** | Profiling | Insider trading, company profiles. | 60 req/min. |

### C. Macro & News (The Context)
| Service | Best For | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **FRED (St. Louis Fed)** | **Macro** | Official US economic data (Interest rates, CPI). | Completely Free & Reliable. |
| **NewsAPI / Finnhub** | Sentiment | Market news & headlines. | No full articles, just summaries. |

---

### 💡 Recommended Architecture
1.  **Price:** Use `yfinance` for all charting and live prices (1-min delay acceptable for analytics).
2.  **Fundamentals:** Use **FMP** (Financial Modeling Prep) for deep dives. Cache results for 24h to save API calls.
3.  **Macro:** Sync **FRED** data once daily (e.g., Treasury Yields, Inflation).
4.  **Technicals:** Calculate RSI/MACD locally using `pandas-ta` instead of wasting API calls.

---

## 2. Task Instructions (Prompt for AI)
"Write a Python script `backend/tests/test_data_source.py` to fetch:"

1.  **Stocks:** Daily OHLCV for `AAPL` (last 5 days) using `yfinance`.
2.  **Sectors (Proxy):** Fetch % Change for ETF `XLK` (Technology) and `XLE` (Energy).
3.  **Macro:** Fetch `CPIAUCSL` (CPI) and `UNRATE` (Unemployment) via `fredapi`.
4.  **Calendar:** Fetch Earnings Date for `TSLA` via `yf.Ticker('TSLA').calendar`.
5.  **Smart Money:** Fetch `yf.Ticker('NVDA').institutional_holders`.
6.  **AI:** Send a test prompt "Hello" to Gemini API.

## 3. Verification
```bash
python backend/tests/test_data_source.py
```
Success Criteria: Console must print valid data for ALL 6 categories. No errors.
