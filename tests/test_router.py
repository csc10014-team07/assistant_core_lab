from assistant_core.models import Intent
from assistant_core.router import route


def test_greeting():
    assert route("hello", set()) == Intent.GREETING


def test_fee():
    assert route("tuition fee", set()) == Intent.FEE


def test_office():
    assert route("where is library", {"library"}) == Intent.OFFICE


def test_rule():
    assert route("thesis registration", set()) == Intent.RULE
