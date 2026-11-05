# Study Assistant — backend (Lab 4 reference)

## Setup
```
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
cp .env.example .env
```
## Run the API
```
uvicorn assistant_api.main:create_app --factory --reload
```
Open http://127.0.0.1:8000/docs for the interactive OpenAPI documentation.

## API contract (v1)
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | — | 200 `{"status":"ok","version":...}` | — |
| POST | `/v1/chat` | `{"message": str 1–2000, "session_id": str}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 invalid, 429 rate limit |
| POST | `/v1/feedback` | `{"request_id": str, "rating": -1/0/1, "comment"?: str ≤500}` | 201 feedback with `id`, `created_at` | 422 |
| GET | `/v1/feedback` | header `X-API-Key` | 200 list | 401 |
| GET | `/v1/weather` | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 upstream down |

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Tests
```
pytest -q                          # unit + API tests (external API mocked)
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.

# Lab 4 – E1: API Verification

## 1. Overview

This section documents the verification of the Study Assistant REST API developed for Lab 4.

The API is built with **FastAPI** and provides endpoints for health checks, chat requests, user feedback, and campus weather information.

The API was tested using Swagger UI and the automated test suite.

## 2. Project Structure

```text
assistant_core_lab/
├── src/
│   └── assistant_core/
├── starter/
│   ├── src/
│   │   └── assistant_api/
│   │       ├── main.py
│   │       ├── ratelimit.py
│   │       ├── schemas.py
│   │       └── weather.py
│   └── tests/
│       └── test_api.py
├── .venv/
├── .env.example
├── requirements.txt
└── pyproject.toml
```

## 3. Environment Setup

Open a terminal in the project root directory.

Set the Python module search path:

```powershell
$env:PYTHONPATH="starter/src;src"
```

Install the required dependencies if they are not already installed:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Configure the required environment variables using the provided `.env.example` file. In particular, configure `API_ADMIN_KEY` for admin-only endpoints.

Do not commit `.env` files or API keys to Git.

## 4. Run the API Server

Start the FastAPI application:

```powershell
.\.venv\Scripts\python.exe -m uvicorn assistant_api.main:create_app --factory --reload
```

When the server starts successfully, it is available at:

```text
http://127.0.0.1:8000
```

Open Swagger UI to interact with and test the endpoints:

```text
http://127.0.0.1:8000/docs
```

## 5. API Endpoint Verification

The following endpoints were verified through Swagger UI.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks whether the API server is running. |
| POST | `/v1/chat` | Sends a message to the assistant. |
| POST | `/v1/feedback` | Submits user feedback. |
| GET | `/v1/feedback` | Retrieves feedback records (admin only). |
| GET | `/v1/weather` | Retrieves campus weather information. |

### 5.1 Health Check

Send a GET request to:

```text
/health
```

Expected result: `200 OK`.

Example response:

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### 5.2 Chat Endpoint

Send a POST request to:

```text
/v1/chat
```

Example request body:

```json
{
  "message": "Where is the library?",
  "session_id": "test-session-01"
}
```

Expected result: `200 OK`.

The response contains the assistant's answer and a generated `request_id`.

### 5.3 Submit Feedback

Send a POST request to:

```text
/v1/feedback
```

Example request body:

```json
{
  "request_id": "test-session-01",
  "rating": 1,
  "comment": "The assistant provided a helpful answer."
}
```

Expected result: `201 Created`.

The response contains the submitted feedback and its generated ID.

### 5.4 Retrieve Feedback (Admin Only)

Send a GET request to:

```text
/v1/feedback
```

This endpoint requires a valid `X-API-Key` header.

In Swagger UI:
1. Open the GET `/v1/feedback` endpoint.
2. Select **Try it out**.
3. Provide the configured admin API key in the `X-API-Key` header if prompted.
4. Select **Execute**.

Expected result: `200 OK` when a valid API key is provided.

A missing or invalid key returns `401 Unauthorized`.

### 5.5 Campus Weather

Send a GET request to:

```text
/v1/weather
```

Expected result:
- `200 OK` when weather data is available.
- `503 Service Unavailable` when the external weather service is unavailable and no usable cached response can be returned.

## 6. Rate Limiting

The `/v1/chat` endpoint includes a per-client rate limiter.

The rate limiter uses the configured `rate_limit_per_min` setting to limit requests from each client within a 60-second window.

When a client exceeds the configured limit, the API returns:

```text
429 Too Many Requests
```

This helps prevent excessive requests from a single client.

## 7. Run Automated Tests

Run the test suite from the project root:

```powershell
$env:PYTHONPATH="starter/src;src"
.\.venv\Scripts\python.exe -m pytest starter/tests -v
```

**Verification result:**

```text
24 passed, 1 warning in 2.02s
```

All 24 tests passed successfully. The warning is a Starlette deprecation warning and does not indicate a test failure.

## 8. Evidence

The following screenshots should be included as evidence for E1:

- Successful `GET /health` request.
- Successful `POST /v1/chat` request showing the response and `request_id`.
- Successful `POST /v1/feedback` request.
- Successful admin `GET /v1/feedback` request.
- Successful `GET /v1/weather` request.
- Automated test result showing `24 passed`.

**Note:** The screenshots should show the actual results obtained from Swagger UI or the terminal.

## 9. Conclusion

The Lab 4 API endpoints were implemented and verified successfully.

The API supports chat requests, feedback submission and retrieval, admin authentication, weather retrieval, and rate limiting.

The automated test suite completed with **24 passed tests**, confirming that the implemented functionality works as expected.
