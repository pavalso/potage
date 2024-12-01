import pytest

from src import pypotage
from src.pypotage import utils


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_chefs_ordered():
    assert pypotage.Chef.is_ordered(pypotage.kitchen_.chef_line.chefs)


def test_add_chef():
    class TestChef1(pypotage.Chef):
        priority = utils.Priority.LAST

    class TestChef2(pypotage.Chef):
        priority = utils.Priority.MIDDLE

    class TestChef3(pypotage.Chef):
        priority = utils.Priority.FIRST

    test_kitchen = pypotage.Kitchen(pypotage.Pot(), [])
    test_kitchen.chef_line.add(TestChef2)
    test_kitchen.chef_line.add(TestChef3)
    test_kitchen.chef_line.add(TestChef1)

    assert test_kitchen.chef_line.chefs[-1] is TestChef1
    assert pypotage.Chef.is_ordered(test_kitchen.chef_line.chefs)

    new_test_kitchen = pypotage.Kitchen(
        pypotage.Pot(),
        [TestChef1, TestChef3, TestChef1])

    assert new_test_kitchen.chef_line.chefs[-1] is TestChef1
    assert pypotage.Chef.is_ordered(new_test_kitchen.chef_line.chefs)


def test_kitchens_dont_share_chefline():
    class TestChef4(pypotage.Chef):
        priority = utils.Priority.LAST

    test_kitchen = pypotage.Kitchen(pypotage.Pot(), [])

    chef = TestChef4
    test_kitchen.chef_line.add(chef)

    assert chef not in pypotage.kitchen_.chef_line.chefs
