import pytest

from typing import Callable

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.pot.ingredients.clear()


def test_no_call_ingredient():
    @pypotage.prepare(no_call=True)
    def test_ingredient() -> Callable:
        raise Exception("Should be raised on take_out")

    func = pypotage.cook(Callable).take_out()
    pytest.raises(Exception, func)

    def test_ingredient2():
        ...

    pytest.raises(
        RuntimeError, pypotage.prepare, test_ingredient2, no_call=True)


def test_no_call_class_ingredient():
    @pypotage.prepare(no_call=True)
    class TestClass:
        def __init__(self) -> None:
            raise Exception("Should be raised on take_out")

    func = pypotage.cook(TestClass).take_out()
    pytest.raises(Exception, func)


def test_no_call_lazy_ingredient():
    @pypotage.prepare(
        no_call=True, lazy=True)
    class TestClass:
        def __init__(self) -> None:
            raise Exception("Should be raised on take_out")

    func = pypotage.cook(TestClass).take_out()
    pytest.raises(Exception, func)

    @pypotage.prepare(
        no_call=True, lazy=True)
    def test_ingredient() -> Callable:
        raise Exception("Should be raised on take_out")

    func = pypotage.cook(Callable).take_out()
    pytest.raises(Exception, func)
