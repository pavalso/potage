import typing

import pytest

from src import pypotage


T = typing.TypeVar("T")


class TestGeneric(typing.Generic[T]):
    ...


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.ingredients.clear()


def test_generic_chef():
    pypotage.prepare(TestGeneric[int])

    pytest.raises(RuntimeError, pypotage.cook(TestGeneric).take_out)

    myGeneric = pypotage.cook(TestGeneric[int]).take_out()
    assert isinstance(myGeneric, TestGeneric)


def test_generic_subclasses():
    class TestGenericSubclass(TestGeneric[T]):
        ...

    pypotage.prepare(TestGenericSubclass[int])
    assert isinstance(
        pypotage.cook(TestGeneric[int]).take_out(), TestGenericSubclass)
    pytest.raises(RuntimeError, pypotage.cook(TestGeneric).take_out)


def test_non_generic_subclasses():
    class TestNonGenericSubclass(TestGeneric[int]):
        ...

    class TestSubclassOfNonGenericSubclass(TestNonGenericSubclass):
        ...

    pypotage.prepare(TestSubclassOfNonGenericSubclass)
    assert isinstance(
        pypotage.cook(TestGeneric[int]).take_out(),
        TestSubclassOfNonGenericSubclass)
    pytest.raises(RuntimeError, pypotage.cook(TestGeneric).take_out)

    assert isinstance(
        pypotage.cook(TestNonGenericSubclass).take_out(),
        TestSubclassOfNonGenericSubclass)


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

    _list_of_generics = pypotage.cook(list[TestGeneric]).take_out()

    assert isinstance(_list_of_generics, list)
    assert all(
        isinstance(x, TestGeneric1) or isinstance(x, TestGeneric2)
        for x in _list_of_generics)
    assert len(_list_of_generics) == 2

    _list_of_intspecifics = pypotage.cook(list[TestGeneric[int]]).take_out()

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
    assert isinstance(
        pypotage.cook(MultipleGeneric[int, str]).take_out(),
        MultipleGeneric)


def test_generic_chef_solo():
    kitchen_ = pypotage.Kitchen(
        pypotage.Pot(),
        [pypotage.chefs.GenericChef()]
    )

    @kitchen_.prepare
    class Bean(TestGeneric[int]):
        ...

    assert isinstance(kitchen_.cook(TestGeneric[int]).take_out(), Bean)
    assert isinstance(kitchen_.cook(Bean).take_out(), Bean)
