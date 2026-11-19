# Lab 5 — Part E.3: The Repository (One Place for All Database Code)

## 1. Overview & Architecture

In Lab 5, persistence is introduced to store assistant interactions and feedback without retaining sensitive personal data. Part **E.3** introduces the **Repository Pattern** to encapsulate all database operations:

- **Separation of Concerns:** The API endpoints (`assistant_api/main.py`) never construct or execute raw SQL statements directly. Instead, all database interactions are delegated to methods on `Repository` (`assistant_api/db.py`).
- **Privacy by Design:** In accordance with data protection regulations, raw session identifiers (which may correlate with student identity or device info) are never stored in plain text. They are hashed using a salted SHA-256 function (`hash_session`).
- **Atomic Transactions:** Multiple database changes belonging to a single operation (e.g. creating a new session record and logging an interaction) are grouped inside a single `Session` and committed atomically (`db.commit()`).

---

## 2. Implementation: `Repository.record_interaction`

The `Repository` class in `src/assistant_api/db.py` implements the core persistence method `record_interaction`:

```python
class Repository:
    """All database access goes through here — the API never writes SQL."""

    def __init__(self, engine, salt: str):
        self.engine, self.salt = engine, salt

    def record_interaction(
        self,
        raw_session: str,
        request_id: str,
        intent: str,
        topic: str | None,
        resolved: bool,
        degraded: bool,
        latency_ms: float,
    ) -> None:
        sid = hash_session(raw_session, self.salt)
        with Session(self.engine) as db:  # one transaction
            if db.get(ChatSession, sid) is None:
                db.add(ChatSession(id=sid))
            db.add(
                Interaction(
                    request_id=request_id,
                    session_id=sid,
                    intent=intent,
                    topic=topic,
                    resolved=resolved,
                    degraded=degraded,
                    latency_ms=latency_ms,
                )
            )
            db.commit()
```

### Key Mechanisms:
1. **Salted Hash Hashing:**
   `sid = hash_session(raw_session, self.salt)` produces a deterministic 16-character SHA-256 hash. The same session identifier always produces the same hash, allowing interaction grouping across requests without exposing user identity.
2. **First-Message Check:**
   `if db.get(ChatSession, sid) is None:` checks whether this is the first interaction in a conversation session. If so, a new row is added to the `chat_session` table.
3. **Metadata Logging:**
   An `Interaction` record is created with request identifier, hashed session reference, intent classification, topic/source ID, resolution status, degradation flag, and response latency.
4. **Transaction Integrity:**
   Wrapping the operations inside `with Session(self.engine) as db:` and completing with `db.commit()` guarantees atomicity (all changes succeed or none do).

---

## 3. Integration with the FastAPI Application

In `src/assistant_api/main.py`:

- The application factory `create_app` accepts an optional `repo: Repository | None = None`. If none is passed (e.g. during production startup), an engine is created from `settings.database_url` and initialized with `init_db(engine)`.
- In the `POST /v1/chat` endpoint, interaction latency is measured using `time.perf_counter()`, and `repo.record_interaction(...)` is called before returning the `ChatResponse`:

```python
@app.post("/v1/chat", response_model=ChatResponse, ...)
def chat(req: ChatRequest, request: Request) -> ChatResponse:
    ...
    start = time.perf_counter()
    resp = service.handle(Message(text=req.message, session_id=req.session_id))
    request_id = uuid.uuid4().hex[:12]
    repo.record_interaction(
        req.session_id,
        request_id,
        resp.intent.value,
        topic=resp.sources[0].id if resp.sources else None,
        resolved=resp.intent.value != "unknown",
        degraded=resp.degraded,
        latency_ms=round((time.perf_counter() - start) * 1000, 2),
    )
    return ChatResponse(**resp.model_dump(), request_id=request_id)
```

---

## 4. Unit Testing & Verification

Unit tests for E.3 are located in `tests/test_db.py`:

```python
def test_session_id_is_hashed():
    repo, engine = make_repo()
    repo.record_interaction("student-42", "r1", "fee", None, True, False, 3.0)
    with Session(engine) as db:
        s = db.exec(select(ChatSession)).one()
    assert s.id == hash_session("student-42", "salt") and "student-42" not in s.id


def test_one_session_many_interactions():
    repo, engine = make_repo()
    for i in range(3):
        repo.record_interaction("s", f"r{i}", "rule", "H26-5.3", True, False, 10.0)
    with Session(engine) as db:
        assert len(db.exec(select(ChatSession)).all()) == 1
        assert len(db.exec(select(Interaction)).all()) == 3
```

- `test_session_id_is_hashed`: Verifies that the raw session ID is never stored in plain text and matches the salted SHA-256 output.
- `test_one_session_many_interactions`: Verifies that multiple interactions under the same session ID reuse the single existing `ChatSession` record while appending individual `Interaction` rows.
