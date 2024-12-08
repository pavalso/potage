import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_chef():
    any_ingredient = pypotage.Ingredient(
        formula=pypotage.Formula(),
        resolve=lambda: None)

    any_order = pypotage.Order(pypotage.Formula(), [], lambda: any_ingredient)

    assert pypotage.Chef.prepare(any_ingredient) == any_ingredient
    assert pypotage.Chef.cook(any_order) == any_order


def test_kitchen_utilities():
    bean = pypotage.cook(str)

    assert pypotage.is_cooked(bean)
    assert not pypotage.is_prepared(bean)
    assert pypotage.get_order(bean) is not None
    pytest.raises(Exception, pypotage.unpack, bean)

    @pypotage.prepare
    def bean1() -> str: return "bean1"

    assert pypotage.is_cooked(bean)
    assert pypotage.is_prepared(bean)
    assert pypotage.unpack(bean) == "bean1"

    assert not pypotage.is_cooked("bean1")
    assert pypotage.is_prepared("bean1")
    pytest.raises(Exception, pypotage.get_order, "bean1")
    assert pypotage.unpack("bean1") == "bean1"
