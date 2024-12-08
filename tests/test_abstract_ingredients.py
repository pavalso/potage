import abc

import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_take_out_abstract():
    class test(metaclass=abc.ABCMeta):
        @classmethod
        @abc.abstractmethod
        def test(self): ...

    @pypotage.prepare
    class test2(test):
        def test(self):
            return "test"

    assert pypotage.cook(test).test() == "test"


def test_prepare_not_decorator_abstract_class():
    class test(metaclass=abc.ABCMeta):
        @classmethod
        @abc.abstractmethod
        def test(self): ...

    class test2(test):
        def test(self):
            return "test"

    pypotage.prepare(test2)
    assert pypotage.cook(test).test() == "test"


def test_prepare_ABC():
    class test(abc.ABC):
        @abc.abstractmethod
        def test(self): ...

    class test2(test):
        def test(self):
            return "test"

    pypotage.prepare(test2)
    assert pypotage.cook(test).test() == "test"

    @pypotage.prepare
    class test3(test):
        def test(self):
            return "test"

    assert pypotage.cook(test3).test() == "test"
