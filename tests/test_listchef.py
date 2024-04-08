import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.pot.ingredients.clear()


def test_prepare_list():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    @pypotage.prepare
    def bean3():
        return "bean3"

    assert pypotage.cook(list[str]).take_out() == ["bean3", "bean2", "bean1"]


def test_prepare_list_ordered():
    @pypotage.prepare(order=1)
    def bean1() -> str:
        return "bean1"

    @pypotage.prepare(order=2)
    def bean2() -> str:
        return "bean2"

    @pypotage.prepare(order=3)
    def bean3():
        return "bean3"

    assert pypotage.cook(list[str]).take_out() == ["bean1", "bean2", "bean3"]


def test_prepare_list_primary():
    @pypotage.prepare(primary=True)
    def bean1() -> str:
        return "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    @pypotage.prepare
    def bean3():
        return "bean3"

    assert pypotage.cook(list[str]).take_out() == ["bean1", "bean3", "bean2"]


def test_prepare_list_empty():
    assert pypotage.cook(list[str]).take_out() == []


def test_prepare_lazy_list():
    class Bean:
        def __init__(self):
            raise Exception("Should be called on take_out() (On lazy beans)")

    @pypotage.prepare(lazy=True)
    def bean() -> Bean:
        return Bean()

    assert pypotage.cook(list[Bean]).is_present()
    pytest.raises(Exception, pypotage.cook(list[Bean]).take_out)
