import pytest

from typing import Generic, TypeVar

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


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

    assert pypotage.cook(Child).test1() == "Parent1.test"
    assert pypotage.cook(Child).test2() == "Parent2.test"
    assert pypotage.cook(Parent1).test1() == "Parent1.test"
    assert pypotage.cook(Parent2).test2() == "Parent2.test"


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

    @pypotage.prepare(
        pypotage.primary
    )
    class GrandChild(Child):
        pass

    assert isinstance(pypotage.cook(GrandChild), GrandChild)
    assert isinstance(pypotage.cook(Child), GrandChild)
    assert isinstance(pypotage.cook(Parent1), GrandChild)
    assert isinstance(pypotage.cook(Parent2), GrandChild)


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

    assert isinstance(pypotage.cook(Child), Child)
    assert isinstance(pypotage.cook(Parent1), Child)
    assert isinstance(pypotage.cook(Parent2), Child)

    @pypotage.prepare
    class SpecificChild(Parent1[int], Parent2[str]):
        pass

    assert isinstance(pypotage.cook(SpecificChild), SpecificChild)
    assert isinstance(pypotage.cook(Parent1[int]), SpecificChild)
    pytest.raises(RuntimeError, pypotage.unpack, pypotage.cook(Parent1[str]))
    assert isinstance(pypotage.cook(Parent2[str]), SpecificChild)
    pytest.raises(RuntimeError, pypotage.unpack, pypotage.cook(Parent2[int]))


def test_generic_multiple_inheritance_list():
    T = TypeVar("T")

    class Parent1(Generic[T]):
        def test1(self):
            return "Parent1.test"

    class Parent2(Generic[T]):
        def test2(self):
            return "Parent2.test"

    @pypotage.prepare(
        pypotage.no_call
    )
    class Child(Parent1, Parent2):
        pass

    @pypotage.prepare(
        pypotage.no_call
    )
    class SpecificChild(Parent1[int], Parent2[str]):
        pass

    assert SpecificChild in pypotage.cook(list[Parent1[int]])
    assert SpecificChild in pypotage.cook(list[Parent2[str]])
    assert SpecificChild not in pypotage.cook(list[Parent1[str]])
    assert SpecificChild not in pypotage.cook(list[Parent2[int]])

    assert Child in pypotage.cook(list[Parent1])
    assert Child not in pypotage.cook(list[Parent1[int]])

    @pypotage.prepare(
        pypotage.no_call
    )
    class ChildOfSpecificChild(SpecificChild):
        pass

    assert ChildOfSpecificChild in pypotage.cook(list[Parent1[int]])
    assert ChildOfSpecificChild in pypotage.cook(list[Parent2[str]])
