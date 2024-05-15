import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.ingredients.clear()


def test_take_out_ingredient_retrieves_latest():
    cooked_str = pypotage.cook(str)

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert cooked_str.take_out() == "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    assert cooked_str.take_out() == "bean2"

    pytest.raises(RuntimeError, pypotage.cook(int).take_out)


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

    assert not cooked_str.is_present()

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert cooked_str.is_present()
