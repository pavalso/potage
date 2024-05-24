import pytest

from src import pypotage


class _TestChef(pypotage.Chef):
    def prepare(self, ingredient):
        ingredient.formula.id = "test"
        ingredient.formula.type = str
        return ingredient

    def cook(self, line):
        line.formula.type = str
        return line


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.ingredients.clear()


def test_preparechefline_works():
    @pypotage.prepare
    def bean_1():
        return 1

    assert pypotage.cook(int).take_out() == 1

    pypotage.kitchen_.chef_line.add(_TestChef())

    @pypotage.prepare
    def bean_2():
        return 1

    assert pypotage.cook(str, "test").take_out() == 1
