from src.pypotage import shared


def test_shared():
    assert shared is not None
    assert shared.__version__ is not None
