import pandas as pd
import ta
from typing import Dict, Any
from core.gemini_logger import logger


class Analyzer:
    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes a single ticker DataFrame (must have Open, High, Low, Close, Volume).
        Returns a dictionary with Technical Indicators, Signals, and a Composite Score.
        """
        if df.empty:
            return {"error": "Empty DataFrame"}

        if df.empty:
            return {"error": "Empty DataFrame"}

        with open("analyzer_debug.log", "w", encoding="utf-8") as f:
            f.write(f"Columns: {df.columns}\n")
            f.write(f"Head: {df.head(1)}\n")
            f.write(f"Index: {df.index}\n")

        # Ensure correct column names

        # Ensure correct column names

        # Ensure correct column names
        # We assume df has standard yfinance columns: Open, High, Low, Close, Volume

        # 1. Calculate Indicators using 'ta' library
        # SMA
        df["SMA_20"] = ta.trend.sma_indicator(df["Close"], window=20)
        df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
        df["SMA_200"] = ta.trend.sma_indicator(df["Close"], window=200)

        # RSI
        df["RSI_14"] = ta.momentum.rsi(df["Close"], window=14)

        # MACD
        macd = ta.trend.MACD(df["Close"], window_slow=26, window_fast=12, window_sign=9)
        df["MACD_12_26_9"] = macd.macd()
        df["MACDs_12_26_9"] = macd.macd_signal()
        df["MACDh_12_26_9"] = macd.macd_diff()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
        df["BBU_20_2"] = bb.bollinger_hband()
        df["BBL_20_2"] = bb.bollinger_lband()
        df["BBM_20_2"] = bb.bollinger_mavg()

        # Get latest values
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest

        # Helper to safely get value (handle NaN at start)
        rsi = latest.get("RSI_14", 50)
        if pd.isna(rsi):
            rsi = 50

        sma20 = latest.get("SMA_20", 0)
        sma50 = latest.get("SMA_50", 0)
        sma200 = latest.get("SMA_200", 0)
        macd_val = latest.get("MACD_12_26_9", 0)
        macd_signal = latest.get("MACDs_12_26_9", 0)
        close = latest["Close"]

        # 2. Generate Signals
        signals = []

        # Golden/Death Cross
        prev_sma50 = prev.get("SMA_50", 0)
        prev_sma200 = prev.get("SMA_200", 0)

        if (
            pd.notna(sma50)
            and pd.notna(sma200)
            and pd.notna(prev_sma50)
            and pd.notna(prev_sma200)
        ):
            if sma50 > sma200 and prev_sma50 <= prev_sma200:
                signals.append("Golden Cross")
            elif sma50 < sma200 and prev_sma50 >= prev_sma200:
                signals.append("Death Cross")

        # RSI
        if rsi < 30:
            signals.append("Oversold (RSI < 30)")
        elif rsi > 70:
            signals.append("Overbought (RSI > 70)")

        # MACD
        if macd_val > macd_signal:
            signals.append("MACD Bullish")
        elif macd_val < macd_signal:
            signals.append("MACD Bearish")

        # Price vs SMA
        if sma200 and close > sma200:
            signals.append("Price > SMA200 (Long-term Bull)")
        elif sma200:
            signals.append("Price < SMA200 (Long-term Bear)")

        # 3. Composite Score (0-100)
        score = 50  # Neutral start

        # Technical Score (40%)
        if sma20 and close > sma20:
            score += 5
        if sma50 and close > sma50:
            score += 5
        if sma200 and close > sma200:
            score += 10
        if rsi < 30:
            score += 15  # Contrarian Buy
        if rsi > 70:
            score -= 10  # Caution
        if macd_val > macd_signal:
            score += 5

        # Fundamental (30%) - Placeholder until API integration
        # Assume 'Neutral' fundamentals for now

        # Macro (30%) - Placeholder until API integration
        # Assume 'Neutral' macro for now

        # Cap Score
        score = max(0, min(100, score))

        # Label
        if score >= 80:
            label = "Strong Buy"
        elif score >= 60:
            label = "Buy"
        elif score <= 20:
            label = "Strong Sell"
        elif score <= 40:
            label = "Sell"
        else:
            label = "Hold"

        result = {
            "symbol": "Unknown",  # Caller should inject
            "date": latest.name.isoformat()
            if hasattr(latest.name, "isoformat")
            else str(latest.name),
            "price": close,
            "score": score,
            "label": label,
            "signals": signals,
            "indicators": {
                "rsi": rsi,
                "sma200": sma200 if pd.notna(sma200) else 0,
                "macd": macd_val,
            },
        }

        logger.log("system", f"Analysis complete. Score: {score}", "analyzer")
        return result


quant_analyzer = Analyzer()
