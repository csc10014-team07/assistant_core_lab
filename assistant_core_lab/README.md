# Study Assistant — backend (Lab 6 reference)

## Setup
```
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
cp .env.example .env
```
## Run the Application (Lab 7 — C.1 Two Servers, Two Terminals)

The assistant runs as two decoupled programs in separate terminals:

### Terminal 1 — Backend (API)
```bash
uvicorn assistant_api.main:create_app --factory --reload
```
- Port: `8000` (http://127.0.0.1:8000)
- OpenAPI Documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### Terminal 2 — Frontend (Streamlit UI)
```bash
streamlit run ui/app.py
```
- Port: `8501` (http://localhost:8501)
- If the API backend is not running, the page displays a red error notice at the top:
  `"The assistant backend is not reachable. Start it with: uvicorn assistant_api.main:create_app --factory"`
- Custom API endpoint (optional): set `ASSISTANT_API_URL=http://<host>:<port>` before launching Streamlit.

## API contract (v1)
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | — | 200 `{"status":"ok","version":...}` | — |
| POST | `/v1/chat` | `{"message": str 1–2000, "session_id": str}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 invalid, 429 rate limit |
| POST | `/v1/feedback` | `{"request_id": str, "rating": -1/0/1, "comment"?: str ≤500}` | 201 feedback with `id`, `created_at` | 422 |
| GET | `/v1/feedback` | header `X-API-Key` | 200 list | 401 |
| GET | `/v1/stats/intents` | header `X-API-Key` | 200 `[{intent, requests, avg_latency_ms, unresolved}]` | 401 |
| GET | `/v1/weather` | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 upstream down |

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Database (Lab 5)
```
python scripts/migrate.py assistant.db      # apply sql/migrations in order
python scripts/seed.py assistant.db 300     # synthetic data only
sqlite3 assistant.db < sql/queries.sql      # the five queries + product questions
```
New endpoint: `GET /v1/stats/intents` (header `X-API-Key`). `POST /v1/feedback` now returns 404 for an unknown `request_id`.

## AI services (Lab 6)
Knowledge base: `data/kb/*.md` (chunked by heading). Prompt: `src/assistant_core/prompts/answer_v1.txt`.
```
LLM_PROVIDER=stub python -m assistant_core "I lost my student card"      # offline
LLM_PROVIDER=ollama LLM_MODEL=llama3.2 python -m assistant_core "..."     # local model (ollama pull llama3.2)
python eval/compare_paths.py                                              # deterministic vs retrieval vs LLM
```
`/v1/chat` responses now include `path` (deterministic | retrieval | llm | tool | abstain), `escalate` and `confidence`.

## Tests
```
pytest -q                          # unit + API tests (external API mocked)
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.
