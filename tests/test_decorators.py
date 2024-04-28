import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.ingredients.clear()


def test_id_decorator():
    @pypotage.prepare
    @pypotage.id("bean1")
    def bean1() -> str:
        return "bean1"

    pytest.raises(RuntimeError, pypotage.cook(str).take_out)
    assert pypotage.cook(str, "bean1").is_present()


def test_type_decorator():
    @pypotage.prepare
    @pypotage.type(str)
    def bean1() -> int:
        return "bean1"

    pytest.raises(RuntimeError, pypotage.cook(int).take_out)
    assert pypotage.cook(str).is_present()


def test_custom_ingredient_decorator():
    pytest.raises(TypeError, pypotage.ingredient, "str")
    pytest.raises(TypeError, pypotage.ingredient, str)

    class CustomIngredient(pypotage.ingredients.Ingredient):
        ...

    @pypotage.ingredient(CustomIngredient)
    def bean1() -> str:
        return "bean1"

    assert isinstance(
        pypotage.ingredient(CustomIngredient)(bean1), CustomIngredient)
