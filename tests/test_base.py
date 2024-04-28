import pytest

from src import pypotage
from src.pypotage import shared


def test_shared():
    assert shared is not None
    assert shared.__version__ is not None


def test_kwargs_deprecated():
    pytest.warns(UserWarning, pypotage.prepare, lambda: None, lazy=True)
