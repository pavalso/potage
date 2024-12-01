import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_prepare_normal_take_out_cases():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str) == "bean1"

    @pypotage.prepare
    def bean2() -> str:
        return "bean2"

    assert pypotage.cook(str) == "bean2"

    @pypotage.prepare()
    def bean3() -> int:
        return 1

    assert pypotage.cook(int) == 1

    @pypotage.prepare
    def bean4():
        return "bean4"

    assert pypotage.cook(str) == "bean4"


def test_prepare_ordered_take_out_cases():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str) == "bean1"

    @pypotage.prepare(
        pypotage.order(1)
    )
    def bean2() -> str:
        return "bean2"

    assert pypotage.cook(str) == "bean2"

    @pypotage.prepare(
        pypotage.order(999)
    )
    def bean3() -> str:
        return "bean3"

    assert pypotage.cook(str) == "bean2"


def test_prepare_primary_take_out_cases():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str) == "bean1"

    @pypotage.prepare(
        pypotage.primary
    )
    def bean2() -> str:
        return "bean2"

    assert pypotage.cook(str) == "bean2"

    @pypotage.prepare
    def bean3() -> str:
        return "bean3"

    assert pypotage.cook(str) == "bean2"


def test_defered_take_out():
    proxy = pypotage.cook(str)

    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert proxy == "bean1"


def test_ingredient_proxy_is_present():
    @pypotage.prepare
    def bean1() -> str:
        return "bean1"

    assert pypotage.cook(str)
    assert not pypotage.is_prepared(pypotage.cook(int))

    @pypotage.prepare
    def bean2() -> int:
        return 1

    assert pypotage.is_prepared(pypotage.cook(int))


def test_cook_allows_subclasses():
    class Bean:
        pass

    class BeanSub(Bean):
        pass

    @pypotage.prepare
    def bean():
        return BeanSub()

    assert pypotage.is_prepared(pypotage.cook(Bean))
    assert pypotage.is_prepared(pypotage.cook(BeanSub))


def test_cook_lazy():
    class Bean:
        def __init__(self):
            raise Exception("Should be called on take_out() (On lazy beans)")

    def bean():
        return Bean()

    pytest.raises(Exception, pypotage.prepare, bean)

    @pypotage.prepare(
        pypotage.lazy
    )
    def bean() -> Bean:
        return Bean()

    pytest.raises(Exception, pypotage.unpack, pypotage.cook(Bean))


def test_cook_lazy_not_annot():
    def bean():
        return 1

    pytest.raises(RuntimeError, pypotage.prepare(pypotage.lazy), bean)

    @pypotage.prepare(
        pypotage.lazy
    )
    class Bean:
        def __init__(self):
            raise Exception("Should be called on take_out() (On lazy beans)")
