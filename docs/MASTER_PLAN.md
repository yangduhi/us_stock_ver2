# 🚀 MarketFlow: Zero-Cost Final Master Plan (S-Class Edition)

## 1. Project Vision
- **Goal:** Build an **Enterprise-Grade** Investment Dashboard using **100% Free Data Sources**.
- **Philosophy:** "Zero Cost, Zero Compromise".
    - **Reliability:** 99.9% Uptime via Self-Healing Pipelines.
    - **Performance:** Instant Logic (RSC + Redis).
    - **UX:** Professional, bespoke aesthetics (No "Bootstrap" feel).

## 2. Tech Stack (The "S-Class" Suite)
- **Frontend:** Next.js 14 (App Router, RSC), Tailwind CSS, Shadcn UI, Zustand + Nuqs (URL State).
- **Backend:** Python FastAPI (Async), Pydantic V2, SQLAlchemy 2.0.
- **Data:** PostgreSQL (TimescaleDB), Redis (Cache + Pub/Sub).
- **AI:** Google Gemini Pro (Free Tier) with Persona Engineering.
- **DevOps:** Docker Compose, GitHub Actions (CI/CD).

## 3. Directory Structure (Strict Domain-Driven)
```text
MarketFlow/
├── backend/
│   ├── app/
│   │   ├── api/            # v1 Endpoints (BFF Pattern)
│   │   ├── core/           # Config, Security, Logging
│   │   ├── services/       # Domain Logic (Fetcher, Analyzer)
│   │   ├── models/         # DB Models (SQLAlchemy)
│   │   ├── schemas/        # Pydantic DTOs
│   │   └── main.py
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── app/                # Route Groups & Pages
│   ├── components/         # UI Primitives & Widgets
│   ├── lib/                # Utils, Hooks
│   ├── config/             # Navigation & Constants
│   └── public/
├── docs/                   # S-Class Documentation
└── docker-compose.yml
```

## 4. The 10-Step Roadmap (Enhanced)
Do not proceed until the verification command passes.

### Phase 1: Unbreakable Foundation
[ ] STEP_01.md: Data Source Validation (Proxy Strategy Check)
[ ] STEP_02.md: DB Schema Setup (TimescaleDB + Hypertables)
[ ] STEP_03.md: **Reliable** ETL Pipeline (Backoff & Timezone Precision)

### Phase 2: Intelligence & Logic
[ ] STEP_04.md: Quant Engine (Scoring & Indicators)
[ ] STEP_05.md: AI Agent (Gemini Persona Integration)

### Phase 3: High-Performance Services
[ ] STEP_06.md: **BFF** API Implementation (Aggregation & Caching)
[ ] STEP_07.md: **RSC** Frontend Architecture (Streaming & Config-UI)
[ ] STEP_08.md: Visualization (Charts, Heatmaps, Gauge Widgets)

### Phase 4: Production Readiness
[ ] STEP_09.md: Advanced Caching (Stale-While-Revalidate)
[ ] STEP_10.md: Secure Docker Deployment (Secrets Management)

## 5. Security Protocols (Mandatory)
- **Secrets:** NEVER commit `.env`. Use Docker Secrets in prod.
- **Input Sanitization:** All API inputs validated via Pydantic.
- **Rate Limiting:** 100 req/min per IP on API Gateway.
- **Error Handling:** Centralized Exception Handler (Mask internal 500 errors).

## 6. Key Commands
Run All: `docker-compose up -d --build`
Seed Data: `docker-compose exec backend python app/seed.py --mode=full`
