import pytest

from typing import Callable

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_no_call_ingredient():
    @pypotage.prepare(
        pypotage.no_call
    )
    def test_ingredient() -> Callable:
        raise Exception("Should be raised on take_out")

    func = pypotage.cook(Callable)
    pytest.raises(Exception, func)

    def test_ingredient2():
        ...

    pytest.raises(
        RuntimeError, pypotage.prepare(pypotage.no_call), test_ingredient2)


def test_no_call_class_ingredient():
    @pypotage.prepare(
        pypotage.no_call
    )
    class TestClass:
        def __init__(self) -> None:
            raise Exception("Should be raised on take_out")

    func = pypotage.cook(TestClass)
    pytest.raises(Exception, func)


def test_no_call_lazy_ingredient():
    @pypotage.prepare(
        pypotage.lazy,
        pypotage.no_call
    )
    class TestClass:
        def __init__(self) -> None:
            raise Exception("Should be raised on take_out")

    func = pypotage.cook(TestClass)
    pytest.raises(Exception, func)

    @pypotage.prepare(
        pypotage.lazy,
        pypotage.no_call
    )
    def test_ingredient() -> Callable:
        raise Exception("Should be raised on take_out")

    func = pypotage.cook(Callable)
    pytest.raises(Exception, func)
