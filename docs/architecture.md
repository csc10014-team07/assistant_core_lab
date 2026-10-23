## Module table
| Module | Responsibility |
|---|---|
| `config.py` | read settings from the environment; validate |
| `errors.py` | named exceptions |
| `models.py` | public contract: `Message`, `Response`, `Intent`, `Source` |
| `router.py` | choose an `Intent` with simple rules |
| `knowledge.py` | office directory (CSV) and handbook (JSON) with search |
| `tools.py` | deterministic tuition calculation |
| `responder.py` | response generation behind one interface (stub LLM, template) |
| `service.py` | `AssistantService.handle(Message) -> Response`, the only entry point |
| `logging_setup.py` | structured JSON logs |
| `__main__.py` | command-line interface |

## The service interface
```text
AssistantService.handle(msg: Message) -> Response
 
Message:  text (1-2000 chars), session_id
Response: answer, intent, sources[], degraded (True if a fallback was used)
Errors:   invalid input -> ValidationError; startup -> ConfigError / DataError;
          provider failures never reach the caller (fallback instead)
```
## Decisions
- Fees are computed in `tools.py`, never by an LLM (exact, testable).
- The LLM sits behind `Responder`; stub needs no key, so tests and CI run offline.
- Configuration comes from the environment; `.env.example` documents every variable.