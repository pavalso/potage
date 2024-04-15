import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.pot.ingredients.clear()


def test_prepare_normal_take_out_cases():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str).take_out() == "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    assert pypotage.cook(str).take_out() == "bean2"

    @pypotage.prepare
    def bean3() -> int:
        return 1

    assert pypotage.cook(int).take_out() == 1

    @pypotage.prepare
    def bean4():
        return "bean4"

    assert pypotage.cook(str).take_out() == "bean4"


def test_prepare_ordered_take_out_cases():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str).take_out() == "bean1"

    @pypotage.prepare(order=1)
    def bean2() -> str:
        return "bean2"

    assert pypotage.cook(str).take_out() == "bean2"

    @pypotage.prepare(order=999)
    def bean3() -> str:
        return "bean3"

    assert pypotage.cook(str).take_out() == "bean2"


def test_prepare_primary_take_out_cases():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str).take_out() == "bean1"

    @pypotage.prepare(primary=True)
    def bean2() -> str:
        return "bean2"

    assert pypotage.cook(str).take_out() == "bean2"

    @pypotage.prepare
    def bean3() -> str:
        return "bean3"

    assert pypotage.cook(str).take_out() == "bean2"


def test_defered_take_out():
    proxy = pypotage.cook(str)

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert proxy.take_out() == "bean1"


def test_ingredient_proxy_is_present():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str).is_present()
    assert not pypotage.cook(int).is_present()

    @pypotage.prepare
    def bean2() -> int:
        return 1

    assert pypotage.cook(int).is_present()


def test_cook_allows_subclasses():
    class Bean:
        pass

    class BeanSub(Bean):
        pass

    @pypotage.prepare
    def bean():
        return BeanSub()

    assert pypotage.cook(Bean).is_present()
    assert pypotage.cook(BeanSub).is_present()


def test_cook_lazy():
    class Bean:
        def __init__(self):
            raise Exception("Should be called on take_out() (On lazy beans)")

    def bean():
        return Bean()

    pytest.raises(Exception, pypotage.prepare, bean)

    @pypotage.prepare(lazy=True)
    def bean() -> Bean:
        return Bean()

    assert pypotage.cook(Bean).is_present()
    pytest.raises(Exception, pypotage.cook(Bean).take_out)
