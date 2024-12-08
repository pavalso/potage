import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_id_decorator():
    @pypotage.prepare(
        pypotage.id("bean1")
    )
    def bean1() -> str:
        return "bean1"

    assert not pypotage.is_prepared(pypotage.cook(str))
    assert pypotage.is_prepared(pypotage.cook(str, "bean1"))


def test_type_decorator():
    @pypotage.prepare(
        pypotage.type(str)
    )
    def bean1() -> int:
        return "bean1"

    assert not pypotage.is_prepared(pypotage.cook(int))
    assert pypotage.is_prepared(pypotage.cook(str))


def test_custom_flavour_creation():
    class TestFlavour(pypotage.Flavour):

        @classmethod
        def apply_to(cls_or_self, ingredient):
            ingredient.resolve = lambda: "test"

    @pypotage.prepare(
        TestFlavour
    )
    def test_ingredient() -> str: ...

    assert pypotage.cook(str) == "test"


def test_custom_flavour_accepts_arguments():
    class TestArgsFlavour(pypotage.Flavour):

        def __init__(self, value: int):
            self.value = value

        def apply_to(cls_or_self, ingredient):
            ingredient.resolve = lambda: cls_or_self.value

    @pypotage.prepare(
        TestArgsFlavour(42)
    )
    def test_ingredient() -> str: ...

    assert pypotage.cook(str) == 42

    @pypotage.prepare(
        TestArgsFlavour(value=25)
    )
    def test_ingredient() -> str: ...

    assert pypotage.cook(str) == 25


def test_custom_flavour_accepts_kwargs():
    class TestKwargsFlavour(pypotage.Flavour):

        def __init__(self, value: int = 1):
            self.value = value

        def apply_to(cls_or_self, ingredient):
            ingredient.resolve = lambda: cls_or_self.value

    @pypotage.prepare(
        TestKwargsFlavour()
    )
    def test_ingredient1() -> str: ...

    assert pypotage.cook(str) == 1

    @pypotage.prepare(
        TestKwargsFlavour(value=25)
    )
    def test_ingredient2() -> str: ...

    assert pypotage.cook(str) == 25

    @pypotage.prepare(
        TestKwargsFlavour(15)
    )
    def test_ingredient3() -> str: ...

    assert pypotage.cook(str) == 15
