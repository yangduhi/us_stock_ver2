import json
import yfinance as yf
from typing import Dict, Any
from app.core.llm_setup import get_gemini_client, get_model_name, get_generation_config
from core.gemini_logger import logger


class AIService:
    def __init__(self):
        try:
            self.client = get_gemini_client()
            self.model_name = get_model_name()
            self.gen_config = get_generation_config()
            logger.log(
                "system",
                "AIService initialized with Google GenAI Client.",
                "ai_service",
            )
        except Exception as e:
            logger.log("error", f"Failed to init Gemini Client: {e}", "ai_service")
            self.client = None

    def analyze_news(self, ticker: str, change_percent: float) -> Dict[str, Any]:
        """
        Fetches news for a ticker and generates a summary explaining the price movement.
        """
        logger.log(
            "user", f"Analyzing news for {ticker} ({change_percent}%)", "ai_service"
        )

        # 1. Fetch News
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            if not news:
                return {"error": "No news found"}

            # Extract headlines
            headlines = []
            for n in news[:5]:
                title = n.get("title")
                if not title and "content" in n:
                    title = n["content"].get("title")
                if title:
                    headlines.append(title)

            if not headlines:
                news_text = "No recent specific news found for this ticker."
            else:
                news_text = "\n".join([f"- {h}" for h in headlines])

        except Exception as e:
            logger.log("error", f"News fetch failed: {e}", "ai_service")
            return {"error": str(e)}

        if not self.client:
            return {"error": "Gemini client not initialized"}

        # 2. Prompt Engineering
        prompt = f"""
        You are a financial analyst. 
        Target: {ticker}
        Price Change: {change_percent:.2f}%
        
        Recent News Headlines:
        {news_text}
        
        Task: Based on these headlines, explain the likely driver for today's price movement in 3 concise bullet points.
        If the news seems unrelated to the price move, state that clearly.
        Output MUST be a JSON object with a key 'summary' containing the markdown text.
        """

        # 3. Generate
        try:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.gen_config
            )

            text = response.text.strip()
            # Simple cleanup for JSON parsing if model outputs json blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            # Try parse, else return raw
            try:
                res_json = json.loads(text)
                summary = res_json.get("summary", text)
            except:
                summary = text

            return {
                "ticker": ticker,
                "change": change_percent,
                "headlines": headlines,
                "summary": summary,
            }

        except Exception as e:
            logger.log("error", f"Gemini generation failed: {e}", "ai_service")
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                return {
                    "ticker": ticker,
                    "change": change_percent,
                    "headlines": headlines,
                    "summary": "⚠️ AI 쿼터 제한으로 인해 분석이 일시 중단되었습니다. 잠시 후 상단 새로고침을 통해 재시도해 주세요.",
                    "status": "429",
                }
            return {"error": msg}


ai_service = AIService()
