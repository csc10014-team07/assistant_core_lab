from pathlib import Path

import pytest

from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService

DATA = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def service():
    settings = Settings()
    offices = OfficeDirectory.from_csv(DATA / "offices.csv")
    handbook = Handbook.from_json(DATA / "handbook.json")
    return AssistantService(settings, offices, handbook, StubLLMResponder())
