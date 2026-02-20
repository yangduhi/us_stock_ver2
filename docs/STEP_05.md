# Step 5: AI Agent Integration (Gemini)

**Objective:** Free News Analysis.

## 1. Task Instructions
1.  **News Source:**
    - Use `yf.Ticker('SYMBOL').news` (Returns JSON).
2.  **Prompt Engineering:**
    - **Input:** JSON News titles + Today's % Change.
    - **Prompt:** "You are a financial analyst. Based on these news headlines for {symbol} which moved {change}%, summarize the key driver in 3 bullet points."
3.  **Service:** `backend/app/services/ai.py`.

## 2. Verification
Run script.
> **Success Criteria:** Gemini returns a coherent markdown summary.
