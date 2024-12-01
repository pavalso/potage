import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_take_out_ingredient_retrieves_latest():
    cooked_str = pypotage.cook(str)

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert cooked_str == "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    assert cooked_str == "bean2"

    pytest.raises(RuntimeError, pypotage.unpack, pypotage.cook(int))


def test_cook_inside_class_is_property():
    class Test:
        cooked_str = pypotage.cook(str)

    test = Test()

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert test.cooked_str == "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    assert test.cooked_str == "bean2"


def test_packed_meal_is_present():
    cooked_str = pypotage.cook(str)

    assert not pypotage.is_prepared(cooked_str)

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.is_prepared(cooked_str)
