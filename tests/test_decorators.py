import pytest

from src import pypotage
from tests.utils import RetrieveRawIngredient


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.ingredients.clear()


def test_id_decorator():
    @pypotage.prepare(
        pypotage.id("bean1")
    )
    def bean1() -> str:
        return "bean1"

    pytest.raises(RuntimeError, pypotage.cook(str).take_out)
    assert pypotage.cook(str, "bean1").is_present()


def test_type_decorator():
    @pypotage.prepare(
        pypotage.type(str)
    )
    def bean1() -> int:
        return "bean1"

    pytest.raises(RuntimeError, pypotage.cook(int).take_out)
    assert pypotage.cook(str).is_present()


def test_custom_flavour_creation():
    class TestFlavour(pypotage.Flavour):

        @staticmethod
        def apply_to(
                ingredient: pypotage.Ingredient) -> pypotage.Ingredient:
            ingredient.formula.extra["__test__"] = True
            return ingredient

    @pypotage.prepare(
        TestFlavour
    )
    def test_ingredient() -> str:
        return "test"

    assert pypotage.cook(str, proxies=[RetrieveRawIngredient]).take_out() \
        .formula.extra["__test__"]


def test_custom_flavour_accepts_arguments():
    class TestArgsFlavour(pypotage.Flavour):

        def __init__(self, value: int):
            self.value = value

        def apply_to(
                self,
                ingredient: pypotage.Ingredient) -> pypotage.Ingredient:
            ingredient.formula.extra["__test__"] = self.value
            return ingredient

    @pypotage.prepare(
        TestArgsFlavour(42)
    )
    def test_ingredient() -> str:
        return "test"

    assert pypotage.cook(str, proxies=[RetrieveRawIngredient]).take_out() \
        .formula.extra["__test__"] == 42


def test_custom_flavour_accepts_kwargs():
    class TestKwargsFlavour(pypotage.Flavour):

        def __init__(self, value: int = 1):
            self.value = value

        def apply_to(
                self,
                ingredient: pypotage.Ingredient) -> pypotage.Ingredient:
            ingredient.formula.extra["__test__"] = self.value
            return ingredient

    @pypotage.prepare(
        TestKwargsFlavour()
    )
    def test_ingredient1() -> str:
        return "test"

    assert pypotage.cook(str, proxies=[RetrieveRawIngredient]).take_out() \
        .formula.extra["__test__"] == 1

    @pypotage.prepare(
        TestKwargsFlavour(value=25)
    )
    def test_ingredient2() -> str:
        return "test"

    assert pypotage.cook(str, proxies=[RetrieveRawIngredient]).take_out() \
        .formula.extra["__test__"] == 25

    @pypotage.prepare(
        TestKwargsFlavour(15)
    )
    def test_ingredient3() -> str:
        return "test"

    assert pypotage.cook(str, proxies=[RetrieveRawIngredient]).take_out() \
        .formula.extra["__test__"] == 15
