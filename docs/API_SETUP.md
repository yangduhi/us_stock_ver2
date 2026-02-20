# API Key Setup Guide

This project relies on a "Hybrid Free Tier" strategy. To enable full functionality (Macro, Fundamentals, AI), you need to obtain the following free API keys and add them to your `.env` file.

## 1. Required Keys

| Service | Variable Name | Purpose | Cost | Limit |
| :--- | :--- | :--- | :--- | :--- |
| **Google Gemini** | `GEMINI_API_KEY` | AI Analysis, News Summaries | Free | 60 req/min |
| **FRED (St. Louis Fed)** | `FRED_API_KEY` | Real-time US Economic Data (CPI, Rates) | Free | High |
| **Financial Modeling Prep** | `FMP_API_KEY` | Company Fundamentals (Balance Sheet, Ratios) | Free | 250 req/day |
| **Finnhub** | `FINNHUB_API_KEY` | Insider Trading, Market News | Free | 60 req/min |

---

## 2. Acquisition Instructions

### 🔑 1. Google Gemini API
*   **Best For:** AI Agent, RAG, News Summarization.
*   **Steps:**
    1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    2.  Click **"Create API key"**.
    3.  Select a project (or create new) and copy the key string.

### 🔑 2. FRED API (Economic Data)
*   **Best For:** Inflation (CPI), Unemployment, Treasury Yields.
*   **Steps:**
    1.  Register at [FRED Account Page](https://fred.stlouisfed.org/user/login).
    2.  After logging in, go to [API Key Request](https://fred.stlouisfed.org/docs/api/api_key.html).
    3.  Accept the terms and copy your alphanumeric key.

### 🔑 3. Financial Modeling Prep (FMP)
*   **Best For:** P/E Ratio, ROE, Debt/Equity, Income Statements.
*   **Steps:**
    1.  Go to [FMP Developer](https://site.financialmodelingprep.com/developer).
    2.  Click **"Sign Up"** (Choose the **Free** plan, usually at the bottom or referenced as "Basic").
    3.  Verify email if required.
    4.  Copy the API Key from your dashboard.

### 🔑 4. Finnhub
*   **Best For:** Insider Trading, Company Profile, Market News.
*   **Steps:**
    1.  Go to [Finnhub Dashboard](https://finnhub.io/register).
    2.  Sign up for a free account.
    3.  Your API key is generated immediately on the dashboard.

---

## 3. Configuration

1.  Open your `.env` file in the project root (`d:/vscode/us_stock_ver2/.env`).
2.  Add or update the following lines:

```ini
# AI
GEMINI_API_KEY=your_gemini_key_here

# Data Providers
FRED_API_KEY=your_fred_key_here
FMP_API_KEY=your_fmp_key_here
FINNHUB_API_KEY=your_finnhub_key_here
```

3.  **Restart** any running scripts or servers to load the new keys.
