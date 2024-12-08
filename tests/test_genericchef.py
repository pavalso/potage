import typing

import pytest

from src import pypotage


T = typing.TypeVar("T")


class TestGeneric(typing.Generic[T]):
    ...


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_generic_chef():
    pypotage.prepare(TestGeneric[int])

    assert isinstance(pypotage.cook(TestGeneric), TestGeneric)
    assert isinstance(pypotage.cook(TestGeneric[int]), TestGeneric)


def test_generic_subclasses():
    class TestGenericSubclass(TestGeneric[T]):
        ...
    
    pytest.raises(RuntimeError, pypotage.unpack, pypotage.cook(TestGeneric[int]))

    pypotage.prepare(TestGenericSubclass[int])

    assert isinstance(pypotage.cook(TestGeneric[int]), TestGenericSubclass)
    assert isinstance(pypotage.cook(TestGenericSubclass[int]), TestGenericSubclass)

    pytest.raises(RuntimeError, pypotage.unpack, pypotage.cook(TestGeneric[str]))

    pypotage.prepare(TestGenericSubclass[str])
    
    assert isinstance(pypotage.cook(TestGeneric[str]), TestGenericSubclass)


def test_non_generic_subclasses():
    class TestNonGenericSubclass(TestGeneric[int]):
        ...

    class TestSubclassOfNonGenericSubclass(TestNonGenericSubclass):
        ...

    pypotage.prepare(TestSubclassOfNonGenericSubclass)

    assert isinstance(pypotage.cook(TestGeneric[int]), TestSubclassOfNonGenericSubclass)
    assert isinstance(pypotage.cook(TestGeneric), TestSubclassOfNonGenericSubclass)
    assert isinstance(pypotage.cook(TestNonGenericSubclass), TestSubclassOfNonGenericSubclass)


def test_list_of_generics():
    @pypotage.prepare
    class TestGeneric1(TestGeneric):
        ...

    @pypotage.prepare
    class TestGeneric2(TestGeneric):
        ...

    @pypotage.prepare
    class TestGeneric3(TestGeneric[int]):
        ...

    @pypotage.prepare
    class TestGeneric4(TestGeneric[int]):
        ...

    _list_of_generics = pypotage.cook(list[TestGeneric])

    assert isinstance(_list_of_generics, list)
    assert all(
        isinstance(x, TestGeneric1) or isinstance(x, TestGeneric2) or isinstance(x, TestGeneric3) or isinstance(x, TestGeneric4)
        for x in _list_of_generics)
    assert len(_list_of_generics) == 4

    _list_of_intspecifics = pypotage.cook(list[TestGeneric[int]])

    assert isinstance(_list_of_intspecifics, list)
    assert all(
        isinstance(x, TestGeneric3) or isinstance(x, TestGeneric4)
        for x in _list_of_intspecifics)
    assert len(_list_of_intspecifics) == 2


def test_multiple_generic_class():
    K = typing.TypeVar("K")

    class MultipleGeneric(typing.Generic[T, K]):
        ...

    pypotage.prepare(MultipleGeneric[int, str])
    assert isinstance(pypotage.cook(MultipleGeneric[int, str]), MultipleGeneric)


def test_generic_chef_solo():
    kitchen_ = pypotage.Kitchen(
        chefs=[pypotage.chefs.GenericChef]
    )

    @kitchen_.prepare
    class Bean(TestGeneric[int]):
        ...

    assert isinstance(kitchen_.cook(TestGeneric[int]), Bean)
    assert isinstance(kitchen_.cook(Bean), Bean)
