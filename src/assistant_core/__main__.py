import sys
import time

from assistant_core.logging_config import setup_logging


def handle_query(query: str):
    if "tuition" in query.lower():
        return "Your tuition is 9,450,000 VND.", "fee"
    return "Sorry, I don't understand.", "unknown"


def main():
    logger = setup_logging()

    query = " ".join(sys.argv[1:])

    start = time.perf_counter()
    answer, intent = handle_query(query)
    latency = (time.perf_counter() - start) * 1000

    logger.info(
        "handled",
        extra={
            "intent": intent,
            "latency_ms": round(latency, 1),
            "session": "local",
            "degraded": False,
        },
    )

    print(answer)


if __name__ == "__main__":
    main()