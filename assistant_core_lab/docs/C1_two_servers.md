# Lab 7 — Part C.1: Two Servers, Two Terminals

## 1. Overview & Architecture

In Lab 7, the Study Assistant evolves into a full-stack system consisting of a Streamlit web user interface communicating with the FastAPI backend. 

In accordance with **Part C.1 ("Two servers, two terminals")**:
- The application architecture strictly separates the **presentation layer (frontend)** from the **application and service layer (backend)**.
- The UI never imports `assistant_core` or `assistant_api` directly. All interactions occur exclusively via HTTP requests sent through `ui/api_client.py`.
- Two separate server processes run in parallel in dedicated terminals:
  - **Backend API Server**: Runs on port `8000` via Uvicorn.
  - **Frontend UI Server**: Runs on port `8501` via Streamlit.

```
+---------------------------+                +-------------------------+
|     Browser Client        |                |       FastAPI API       |
|    http://localhost:8501  |                |  http://127.0.0.1:8000  |
+-------------+-------------+                +------------+------------+
              |                                           ^
              v                                           |
+---------------------------+   HTTP (httpx)              |
|    Streamlit UI           | ----------------------------+
|    ui/app.py              |   GET  /health
+---------------------------+   POST /v1/chat
                                POST /v1/feedback
```

---

## 2. Server Startup Instructions

### Terminal 1 — Backend (API)
From the project working directory (`assistant_core_lab`):

```bash
uvicorn assistant_api.main:create_app --factory --reload
```
- **Listening on:** `http://127.0.0.1:8000`
- **Swagger / OpenAPI Documentation:** `http://127.0.0.1:8000/docs`
- **Health Check Endpoint:** `http://127.0.0.1:8000/health` returning `{"status": "ok", "version": "1.0.0"}`

### Terminal 2 — Frontend (Streamlit UI)
From the project working directory (`assistant_core_lab`):

```bash
streamlit run ui/app.py
```
- **Local URL:** `http://localhost:8501`
- **Network URL:** Accessible to other devices on the same local network.

---

## 3. Communication & Health Check Mechanism

### 3.1 The `healthy()` Check
On each page load/rerun in Streamlit, `ui/app.py` queries the backend's `/health` endpoint via `AssistantClient.healthy()`:

```python
# ui/api_client.py
def healthy(self) -> bool:
    try:
        return self._http.get("/health").status_code == 200
    except httpx.HTTPError:
        return False
```

### 3.2 Error State (Backend Offline)
If the API backend is down or not yet started, `self._http.get("/health")` raises `httpx.ConnectError` (subclass of `httpx.HTTPError`). The client catches this and returns `False`.

In `ui/app.py`:
```python
if not client.healthy():
    st.error("The assistant backend is not reachable. Start it with: uvicorn assistant_api.main:create_app --factory")
```
The user is presented with a red alert banner clearly stating that the backend is unreachable along with the exact terminal command required to start it, adhering to the *"Fail politely"* principle.

### 3.3 Connected State (Backend Online)
When Terminal 1 is active, `client.healthy()` receives status code `200`, no warning is displayed, and requests flow smoothly to `/v1/chat`.

---

## 4. Configuration

The UI uses the `ASSISTANT_API_URL` environment variable to configure the backend target address (defaulting to `http://127.0.0.1:8000`):

```bash
# Windows PowerShell
$env:ASSISTANT_API_URL = "http://127.0.0.1:8000"
streamlit run ui/app.py

# Linux / macOS
ASSISTANT_API_URL=http://127.0.0.1:8000 streamlit run ui/app.py
```

---

## 5. Verification Checklist

- [x] Backend starts on port `8000` (`python -m uvicorn assistant_api.main:create_app --factory`).
- [x] Streamlit UI starts on port `8501` (`python -m streamlit run ui/app.py`).
- [x] When backend is down: `client.healthy()` evaluates to `False`, red alert displayed.
- [x] When backend is up: `client.healthy()` evaluates to `True`, red alert dismissed.
- [x] `requirements.txt` updated to include `streamlit`.
