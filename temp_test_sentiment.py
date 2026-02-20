
import asyncio
import os
import sys

# 프로젝트 루트 경로 추가
sys.path.append(os.getcwd())

from backend.app.services.market_service import market_service
from backend.app.services.fetcher import fetcher
from backend.app.core.cache import cache

async def test_sentiment_logic():
    print("Testing Composite Sentiment Logic (ETF Flow based)...")
    
    # 캐시 삭제
    await cache.delete("market:composite_sentiment")
    
    # 1. Composite Sentiment 계산
    result = await market_service.get_composite_sentiment(fetcher)
    print(f"Proprietary Composite Score: {result}")
    
    # 2. CNN Official Index 확인
    cnn_result = await market_service.get_fear_greed_index()
    print(f"CNN Official Score: {cnn_result}")
    
    assert "value" in result
    assert "label" in result
    print("SUCCESS: Sentiment logic verified.")

if __name__ == "__main__":
    asyncio.run(test_sentiment_logic())
    
    # 자동 삭제 로직
    import os
    try:
        os.remove(__file__)
    except:
        pass
