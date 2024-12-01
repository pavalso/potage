import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


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

    assert pypotage.cook(list[str]) == ["bean3", "bean2", "bean1"]


def test_prepare_list_ordered():
    @pypotage.prepare(
        pypotage.order(1)
    )
    def bean1() -> str:
        return "bean1"

    @pypotage.prepare(
        pypotage.order(2)
    )
    def bean2() -> str:
        return "bean2"

    @pypotage.prepare(
        pypotage.order(3)
    )
    def bean3():
        return "bean3"

    assert pypotage.cook(list[str]) == ["bean1", "bean2", "bean3"]


def test_prepare_list_primary():
    @pypotage.prepare(
        pypotage.primary
    )
    def bean1() -> str:
        return "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    @pypotage.prepare
    def bean3():
        return "bean3"

    assert pypotage.cook(list[str]) == ["bean1", "bean3", "bean2"]


def test_prepare_list_empty():
    assert pypotage.cook(list[str]) == []


def test_prepare_lazy_list():
    class Bean:
        def __init__(self): ...

    @pypotage.prepare(
        pypotage.lazy
    )
    def bean() -> Bean:
        return Bean()

    assert pypotage.is_prepared(pypotage.cook(list[Bean]))
    
    beans = pypotage.cook(list[Bean])
    assert len(beans) == 1
    assert isinstance(beans[0], Bean)


def test_list_chef_solo():
    kitchen_ = pypotage.Kitchen(
        chefs=[pypotage.chefs.ListChef]
    )

    @kitchen_.prepare
    def bean1() -> str:
        return "bean1"

    @kitchen_.prepare
    def bean2() -> str:
        return "bean2"

    assert kitchen_.cook(list[str]) == ["bean2", "bean1"]
