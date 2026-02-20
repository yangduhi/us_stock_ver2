# Step 2: Database Infrastructure

**Objective:** Set up TimescaleDB to store time-series data efficiently.

## 1. Task Instructions
1.  **Docker Setup:**
    - `docker-compose.yml`: Service `db` using `timescale/timescaledb:latest-pg14`.
    - Ports: `5432:5432`.

2.  **Schema Design (`backend/app/models`):**
    - **`Ticker`**: `symbol` (PK), `name`, `sector`, `industry`, `is_etf` (bool).
    - **`MarketData`**: `symbol` (FK), `date` (PK), `open`, `high`, `low`, `close`, `volume`.
        - *Action:* Convert to Hypertable.
    - **`Financials`** (New): `symbol` (FK), `period` (date), `revenue`, `net_income`, `eps`, `total_debt`, `equity`, `roe`.
    - **`MacroData`**: `series_id` (e.g., 'CPI', 'TREASURY_10Y'), `date`, `value`.
    - **`MarketSentiment`** (New): `date`, `score` (0-100), `source` (e.g., 'FearGreed').
    - **`Holdings`**: `symbol`, `holder`, `shares`, `date_reported`.

3.  **Init Script:**
    - Create `backend/init_db.py` to apply schemas.

## 2. Verification
```bash
docker-compose up -d db
python backend/init_db.py
```
Success Criteria: Tables created. MarketData is a hypertable.
