# Nirikshak.AI — Project Context

> **Living document** — Updated as the project is built. Use this to track what exists, what's pending, and how everything connects.

---

## Project Identity

| Field | Value |
|---|---|
| **Name** | Nirikshak.AI |
| **Tagline** | Proactive Intelligence for Life-Stage Banking |
| **Hackathon** | SBI Hackathon — PS-3 |
| **Author** | Rahul Singh Rajpurohit |
| **Status** | 🟡 Planning Phase |

---

## Current State

- [x] PPT and PDF analyzed
- [x] Implementation plan created and approved
- [x] Folder structure scaffolded
- [x] Backend (FastAPI) stubs created
- [x] Frontend (React + Vite) shell created
- [x] Synthetic data generator built
- [x] RAG reasoning engine stubs created
- [x] Docker / Infrastructure files created
- [x] Documentation (README, docs/, LICENSE) created
- [x] End-to-end demo verified

---

## Files Created

*Will be updated as files are created.*

| File / Folder | Purpose | Status |
|---|---|---|
| `context.md` | Living project tracker | ✅ Created |
| `backend/` | FastAPI backend | ✅ Created |
| `data/` | Synthetic data, seed data, knowledge base | ✅ Created |
| `docs/` | Architecture and API documentation | ✅ Created |

---

## Tech Stack (Confirmed)

| Layer | Technology |
|---|---|
| Frontend | React.js (Vite), Tailwind CSS, Recharts |
| Backend | FastAPI (Python) |
| Database | PostgreSQL (structured), ChromaDB (vector/RAG) |
| AI/RAG | LangChain, LLM API (OpenAI/Claude, abstracted) |
| Data Gen | Python + Faker |
| Infra | Docker + docker-compose |

---

## Architecture Notes

**Pipeline:** Data Ingestion → Pattern Detection (rule + ML hybrid) → RAG Reasoning (vector DB + LLM) → Trigger Mapping → Personalized Engagement → Feedback Loop

---

## Decisions & Notes

- Stub/mock logic is acceptable where real integration isn't feasible
- No hardcoded API keys or real bank data
- Priority: demo-ready structure over exhaustive features
- LLM provider must be abstracted behind an interface (configurable via `.env`)

---

## Change Log

| Date | Change |
|---|---|
| 2025-07-05 | Project analyzed, context.md created, implementation plan in progress |
