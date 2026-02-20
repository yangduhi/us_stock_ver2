# Step 10: Docker Deployment

**Objective:** Run 24/7.

## 1. Task Instructions
1.  **Docker Compose (Prod):**
    - Services: `backend`, `frontend`, `db`, `redis`, `scheduler`.
    - Restart: `always`.
2.  **Env Variables:**
    - Inject `FRED_API_KEY`, `GEMINI_API_KEY`.

## 2. Verification
```bash
docker-compose up --build
```
Success Criteria: Dashboard accessible via localhost. Data updates automatically via Scheduler.
