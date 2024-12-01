import pytest

from src import pypotage


class _TestChef(pypotage.Chef):
    @classmethod
    def prepare(cls_or_self, ingredient):
        ingredient.formula.id = "test"
        ingredient.formula.type = str
        return ingredient

    @classmethod
    def cook(cls_or_self, order):
        order.formula.type = str
        return order


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_preparechefline_works():
    @pypotage.prepare
    def bean_1():
        return 1

    assert pypotage.cook(int) == 1

    pypotage.kitchen_.chef_line.add(_TestChef)

    @pypotage.prepare
    def bean_2():
        return 1

    assert pypotage.cook(str, "test") == 1
