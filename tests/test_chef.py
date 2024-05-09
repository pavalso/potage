import pytest

from src import pypotage
from src.pypotage import utils


class TestChef1(pypotage.Chef):

    @property
    def priority(self) -> int:
        return utils.Priority.LAST


class TestChef2(pypotage.Chef):

    @property
    def priority(self) -> int:
        return utils.Priority.MIDDLE


class TestChef3(pypotage.Chef):

    @property
    def priority(self) -> int:
        return utils.Priority.FIRST


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.ingredients.clear()


def is_ordered(priorized: list[utils.Priorized]) -> bool:
    return all(
        priorized[i].priority >= priorized[i + 1].priority
        for i in range(len(priorized) - 1)
    )


def test_ingredients_order():
    assert is_ordered(pypotage.kitchen_.chef_line.chefs)


def test_add_ingredient():
    test_kitchen = pypotage.Kitchen(pypotage.Pot(), [])
    test_kitchen.chef_line.add(TestChef2())
    test_kitchen.chef_line.add(TestChef3())
    test_kitchen.chef_line.add(TestChef1())

    assert isinstance(test_kitchen.chef_line.chefs[-1], TestChef1)

    new_test_kitchen = pypotage.Kitchen(
        pypotage.Pot(),
        [TestChef1(), TestChef3(), TestChef1()])

    assert isinstance(new_test_kitchen.chef_line.chefs[-1], TestChef1)


def test_kitchens_dont_share_chefline():
    test_kitchen = pypotage.Kitchen(pypotage.Pot(), [])

    chef = TestChef1()
    test_kitchen.chef_line.add(chef)

    assert chef not in pypotage.kitchen_.chef_line.chefs
