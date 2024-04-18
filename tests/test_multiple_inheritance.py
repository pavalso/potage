import pytest

from typing import Generic, TypeVar

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.pot.ingredients.clear()


def test_1depth_multiple_inheritance():
    class Parent1:
        def test1(self):
            return "Parent1.test"

    class Parent2:
        def test2(self):
            return "Parent2.test"

    @pypotage.prepare
    class Child(Parent1, Parent2):
        pass

    assert pypotage.cook(Child).take_out().test1() == "Parent1.test"
    assert pypotage.cook(Child).take_out().test2() == "Parent2.test"
    assert pypotage.cook(Parent1).take_out().test1() == "Parent1.test"
    assert pypotage.cook(Parent2).take_out().test2() == "Parent2.test"


def test_2depth_multiple_inheritance():
    class Parent1:
        def test1(self):
            return "Parent1.test"

    class Parent2:
        def test2(self):
            return "Parent2.test"

    @pypotage.prepare
    class Child(Parent1, Parent2):
        pass

    @pypotage.prepare(primary=True)
    class GrandChild(Child):
        pass

    assert isinstance(pypotage.cook(GrandChild).take_out(), GrandChild)
    assert isinstance(pypotage.cook(Child).take_out(), GrandChild)
    assert isinstance(pypotage.cook(Parent1).take_out(), GrandChild)
    assert isinstance(pypotage.cook(Parent2).take_out(), GrandChild)


def test_generic_multiple_inheritance():
    T = TypeVar("T")

    class Parent1(Generic[T]):
        def test1(self):
            return "Parent1.test"

    class Parent2(Generic[T]):
        def test2(self):
            return "Parent2.test"

    @pypotage.prepare
    class Child(Parent1, Parent2):
        pass

    assert isinstance(pypotage.cook(Child).take_out(), Child)

    @pypotage.prepare
    class SpecificChild(Parent1[int], Parent2[str]):
        pass

    assert isinstance(pypotage.cook(SpecificChild).take_out(), SpecificChild)
    assert isinstance(pypotage.cook(Parent1[int]).take_out(), SpecificChild)
    pytest.raises(RuntimeError, lambda:
                  pypotage.cook(Parent1[str]).take_out())
    assert isinstance(pypotage.cook(Parent2[str]).take_out(), SpecificChild)
    pytest.raises(RuntimeError, lambda:
                  pypotage.cook(Parent2[int]).take_out())
