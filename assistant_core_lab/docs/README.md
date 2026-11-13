## 1. Run the Tests

Run the complete test suite:

python -m pytest -q

Expected result:

27 passed

## 2. Start the API Server

Run the FastAPI application:

uvicorn assistant_api.main:create_app --factory --reload

The server should start at:

http://127.0.0.1:8000

Open the interactive API documentation:

http://127.0.0.1:8000/docs

3. Test the API Endpoints

### 3.1 Send a Chat Message

Find:

POST /v1/chat

Click Try it out.

Enter the request body:

{
  "message": "Where is the library?",
  "session_id": "huy-lab05-session"
}

Click Execute.

Copy the request_id from the response.

Example response:

{
  "answer": "Library B.201 Mon-Sat 07:00-20:00",
  "intent": "office",
  "sources": [],
  "degraded": false,
  "request_id": "a94b79d4c748"
}

### 3.2 Submit Valid Feedback (201 Created)

Find:

POST /v1/feedback

Replace the example request ID with the ID returned by /v1/chat.

{
  "request_id": "a94b79d4c748",
  "rating": 1,
  "comment": "The answer is helpful."
}

Click Execute.

Expected result:

201 Created

This confirms that feedback was successfully saved.

Valid rating values are -1, 0, and 1.

### 3.3 Submit Invalid Feedback (404 Not Found)

Send another request to POST /v1/feedback:

{
  "request_id": "nope",
  "rating": -1,
  "comment": "Testing an invalid request ID."
}

Click Execute.

Expected result:

404 Not Found

## 4.Checking DB Browser for SQLite

### 4.1 Open database of assistant.db

### 4.2 Open the Browse Data tab.

Select each table from the Table dropdown.

The database contains three main tables:

- Table

- Description

- chat_session

Stores hashed session identifiers and session metadata.

interaction

Stores request IDs, intent, topic, resolution status, and latency.

feedback

Stores feedback request IDs, ratings, comments, and timestamps.

Verify that:

- chat_session contains the created session.

- interaction contains the request ID returned by /v1/chat.

- feedback contains the valid feedback submitted earlier.

- The invalid request ID nope was not saved.