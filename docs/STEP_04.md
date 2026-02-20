# Step 4: Quant & Prediction Engine

**Objective:** Generate "Insights" from raw data locally.

## 1. Task Instructions
Create `backend/app/services/analyzer.py`:

1.  **Signals (Technical Indicators):**
    - Calculate RSI(14), MACD, SMA(20/50/200) using `pandas-ta`.
    - **Golden Cross:** SMA50 crosses above SMA200.
    - **Oversold:** RSI < 30.

2.  **Prediction Model (Composite Score):**
    - *Logic (0-100 Score):*
        - **Technical (40%):**
            - Price > SMA20: +10.
            - RSI < 30 (Oversold): +15.
            - MACD > Signal: +10.
            - Volatility Squeeze: +5.
        - **Fundamental (30%):**
            - ROE (Return on Equity) > 15%: +15.
            - Net Profit Margin > 20%: +15.
        - **Macro (30%):**
            - Yield Curve (10Y-2Y) > 0: +15 (No Recession).
            - Fear & Greed Index < 20 (Extreme Fear): +15 (Contrarian Buy).
    - *Output:* Score (0-100) & Label ("Strong Buy"/"Hold"/"Sell").

3.  **Smart Money Logic:**
    - Query `Holdings` table. Sort by largest % held.

4.  **Market Regime:**
    - If `SPY` Price > SMA200 -> "Risk-On". Else "Risk-Off".

## 2. Verification
Test script printing analysis for 'AAPL'.
> **Success Criteria:** Prints "Prediction: Bullish (75)", "Signal: Golden Cross".
