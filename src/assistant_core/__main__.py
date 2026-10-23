import logging
import sys
import time

from pydantic import ValidationError

from assistant_core.config import load_settings
from assistant_core.errors import AssistantError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService

log = logging.getLogger("assistant_core")


def main() -> int:
    try:
        settings = load_settings()
        setup_logging(settings.log_level)
        offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
        handbook = Handbook.from_json(settings.data_dir / "handbook.json")
    except AssistantError as exc:
        print(f"Startup error: {exc}", file=sys.stderr)
        return 1

    service = AssistantService(settings, offices, handbook, StubLLMResponder())

    text = " ".join(sys.argv[1:])
    start = time.perf_counter()
    try:
        r = service.handle(Message(text=text))
    except ValidationError:
        print("Please type a message (1-2000 characters).", file=sys.stderr)
        return 1
    except AssistantError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    log.info(
        "handled",
        extra={
            "intent": r.intent.value,
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "session": "local",
            "degraded": r.degraded,
        },
    )
    print(r.answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
