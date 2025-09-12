# Prospect AI – Technical Design

## 1. Overview
A B2B sales prospecting system with:
- Frontend: React + Vite + Tailwind (prospect-ai-dashboard).
- Backend: FastAPI (prospect_ai_backend), modularized like Flask Blueprints via APIRouter.
- LLM: Wrapped via llm_manager.
- MCP: Model Context Protocol client to tool servers (enrichment/search/CRM).
- Automation: Contact form orchestration with CAPTCHA handling.

## 2. Goals and Non‑Goals
Goals
- Modular API with APIRouter per domain.
- Reuse existing automation code (contact_form_manager, captcha_handler, llm_manager).
- MCP-enabled enrichment and tool use.
- TDD-first with pytest and FastAPI TestClient.
- Easy local dev via Vite proxy to FastAPI.

Non‑Goals
- Full persistence or complex workflows at MVP (mock/BackgroundTasks first).
- Production auth/ACL (add later).

## 3. High-Level Architecture
- React App → HTTP → FastAPI (/api)
- FastAPI Routers (prospects | campaigns | automation | llm | health)
- Services
  - ProspectService, CampaignService (mock → DB later)
  - AutomationService (wraps contact_form_manager, captcha_handler)
  - LLMService (wraps llm/llm_manager)
  - MCPClient (talks to MCP tool servers)
- Workers: FastAPI BackgroundTasks (MVP), Celery/RQ + Redis (next)
- Data: mock/in-memory (MVP), Postgres + SQLAlchemy (next)
- Observability: structured logs, request IDs, health

ASCII diagram
- prospect-ai-dashboard (React)
  -> /api (Vite proxy or direct) -> FastAPI
     -> Routers
        -> Services
           -> Existing modules (contact_form_*, captcha_handler, llm_manager)
           -> MCP Client -> MCP Servers (enrichment/search/CRM)
        -> Background jobs -> External sites/APIs
     -> DB (future)

## 4. Repository Structure
Frontend (already in repo)
- index.html, vite.config.ts, tailwind.config.js
- src/
  - main.tsx, App.tsx, styles/index.css
  - contexts/ThemeContext.tsx
  - components/Dashboard/*, components/UI/*
  - hooks/*, services/ProspectService.tsx
  - types/index.ts, constants/dashboard.ts, utils/utils.ts

Backend (target)
- src/
  - captcha_handler.py
  - contact_form_automator.py
  - contact_form_bot_facade.py
  - contact_form_manager.py
  - strings.py, utils.py
  - llm/llm_manager.py
  - api/
    - main.py (create_app, include_router, CORS)
    - routers/ (Flask Blueprint equivalent)
      - health.py, prospects.py, campaigns.py, automation.py, llm.py
    - schemas/ (Pydantic models)
      - prospect.py, campaign.py, automation.py, llm.py
    - services/
      - prospect_service.py, campaign_service.py
      - automation_service.py, llm_service.py, mcp_client.py

## 5. API Design (MVP)
Base: /api

- GET /health
  - 200 { status: "ok" }

- GET /prospects
  - Query: search?, industry? (CSV), status? (CSV)
  - 200 [ProspectOut]

- GET /campaigns
  - 200 [CampaignOut]

- POST /llm/generate
  - Body: { prompt: string, params?: object }
  - 200 { output: string }

- POST /automation/contact-forms/run
  - Body: RunCampaignIn { campaign_id?, message_template, targets[] }
  - 200 RunResultOut { job_id, status: "queued" }
  - Notes: enqueue via BackgroundTasks; future: job status endpoints.

## 6. Services and Integrations
- ProspectService
  - list(search, industries[], statuses[]) → [Prospect]
  - MVP: in-memory mocks; later: DB query.

- CampaignService
  - list() → [Campaign]
  - MVP: mocks.

- LLMService
  - generate(prompt, **params) → string
  - Wraps llm_manager; single responsibility boundary.

- MCPClient
  - enrich_company(domain) → dict
  - search_contacts(query) → [{ name, email }]
  - Implementation via MCP Python SDK (stub until tools available).

- AutomationService
  - enqueue_campaign(payload, background) → job_id
  - _run_sync(job_id, data): orchestrate contact_form_manager +
    captcha_handler; optional pre-enrichment via MCP; prompt crafting via LLMService.

## 7. LLM Integration
- Centralized via LLMService to isolate provider logic.
- llm_manager invoked for:
  - Message generation/personalization from templates and prospect context.
  - Classification/scoring of responses (future).
- Guardrails:
  - Deterministic params in tests (temperature=0).
  - Token/latency budgets; retries with backoff.

## 8. MCP Integration
- MCPClient abstracts tool servers; configurable via env MCP_SERVER_URL.
- Use cases:
  - Company enrichment (employees, industry, tech).
  - Contact discovery (search, SERP).
  - CRM sync (future).
- Non-blocking pattern:
  - Enrichment pre-step best-effort; cache results when DB is added.

## 9. Data Model (Schemas)
- ProspectOut: id, name, company, status, industry?, lastContactDate?
- CampaignOut: id, name, channel, sent, opens, clicks, responses
- RunCampaignIn: campaign_id?, message_template, targets[]
- RunResultOut: job_id, status

Future:
- Persist Prospects, Campaigns, CampaignRun, ResultLog in Postgres.
- SQLAlchemy models; Alembic migrations.

## 10. Security
- CORS allow http://localhost:5173 in dev.
- Secrets via env vars; do not commit keys.
- Auth: API key/Bearer token (future).
- Rate limiting for automation endpoints (future).

## 11. Configuration
Backend (env)
- PORT=8000
- MCP_SERVER_URL=http://localhost:8765
- LOG_LEVEL=INFO

Frontend (env)
- VITE_API_URL=/api (with Vite proxy) or http://localhost:8000/api

Vite proxy (dev)
- Proxy /api → http://localhost:8000

## 12. Error Handling
- FastAPI exception handlers → JSON problem responses.
- Service-level try/except with contextual logs.
- Clear client errors for unreachable API; retries for transient errors.

## 13. Observability
- Structured JSON logs with request_id and job_id.
- /api/health endpoint.
- Metrics (future): Prometheus exporter; request latency; queue depth.

## 14. Performance and Reliability
- Use httpx async clients for external calls.
- Timeouts and retries with jittered backoff.
- BackgroundTasks for MVP; switch to Celery/RQ with Redis for scale.
- Idempotent job handling keyed by campaign_id + target hash (future).

## 15. Testing Strategy (TDD)
- pytest + FastAPI TestClient.
- Dependency overrides for services in tests.
- Unit tests for services; API tests for routers; contract tests for schemas.
- LLM tests via monkeypatch on llm_manager.
- MCP client tests stubbed with deterministic responses.

Directory
- prospect_ai_backend/tests/
  - conftest.py (app + overrides)
  - test_health.py, test_prospects_api.py, test_campaigns_api.py
  - test_llm_api.py, test_automation_api.py
  - services/: test_*_service.py, test_mcp_client.py

## 16. Local Development
Backend
- uvicorn src.api.main:app --reload --port 8000

Frontend
- Vite proxy configured; set VITE_API_URL=/api
- npm run dev

End-to-end
- Open http://localhost:5173
- Calls proxy to FastAPI at http://localhost:8000/api

## 17. Milestones
M1: Scaffold FastAPI (routers, schemas, services), health/prospects/campaigns/llm endpoints, tests green.
M2: Automation endpoint enqueues BackgroundTasks; basic orchestration with existing modules.
M3: MCP enrichment hooks; feature flags; improved logging.
M4: Job status API; move to Celery/RQ; Redis.
M5: Postgres persistence; SQLAlchemy; migrations; e2e tests.

## 18. Risks and Mitigations
- Long-running automation blocking: use background jobs and queues.
- LLM cost/latency: cache prompts, batch, tune params.
- Tool reliability via MCP: degrade gracefully; circuit breakers.
- Website anti-bot/CAPTCHA: rotate strategies; respect robots and legal