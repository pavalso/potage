import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_cache_works():
    cook = pypotage.cook(int)
    x = 0

    @pypotage.prepare
    def bean1():
        nonlocal x
        x += 1
        return x

    assert cook == 2 # As prepare is implicitly called, x is incremented by 1 and once cook is called, x is incremented by 1 again
    assert cook == 2 # As no more prepare has been called, x is not incremented again

    @pypotage.prepare
    def bean2() -> int:
        nonlocal x
        x += 1
        return x

    assert cook == 3 # Now, bean2 is lazily prepared so x is only incremented by 1 when cook is called


def test_cache_works_lazy():
    cook = pypotage.cook(int)
    x = None

    @pypotage.prepare
    def bean1() -> int:
        nonlocal x

        if x == 1:
            raise RuntimeError("Called with wrong value")

        x = 1
        return x

    assert cook == 1
    assert cook == 1 # If cache is not working, this will raise RuntimeError("Called with wrong value") an exception

    @pypotage.prepare
    def bean2() -> int:
        nonlocal x

        if x == 2:
            raise RuntimeError("Called with wrong value")

        x = 2
        return x

    assert cook == 2
    assert cook == 2 # If cache is not working, this will raise RuntimeError("Called with wrong value") an exception


def test_cache_raises_exception():
    cook = pypotage.cook(int)
    x = 0

    pytest.raises(RuntimeError, pypotage.unpack, cook)

    @pypotage.prepare
    def bean1() -> int:
        nonlocal x

        if x == 1:
            raise Exception("Unexpected error")
        else:
            x = 1
            raise RuntimeError("Expected error")

    pytest.raises(RuntimeError, pypotage.unpack, cook)
    pytest.raises(RuntimeError, pypotage.unpack, cook)


def test_cache_works_with_heritance():
    @pypotage.prepare
    class Parent: ...

    cook = pypotage.cook(Parent)

    assert isinstance(pypotage.unpack(cook), Parent)

    @pypotage.prepare(
        pypotage.order(pypotage.Priority.BEFORE_LAST)
    )
    class Child(Parent): ...

    assert isinstance(pypotage.unpack(cook), Child)

    @pypotage.prepare(
        pypotage.order(pypotage.Priority.LAST)
    )
    class GrandChild(Child): ...

    assert isinstance(pypotage.unpack(cook), GrandChild)


def test_cache_works_with_heritance_lazy():
    class Parent: ...

    cook = pypotage.cook(Parent)

    pytest.raises(Exception, pypotage.unpack, cook)

    @pypotage.prepare(
        pypotage.order(pypotage.Priority.LAST)
    )
    class Child(Parent): ...

    @pypotage.prepare
    def bean1() -> Parent:
        raise RuntimeError("Unexpected error")

    assert isinstance(pypotage.unpack(cook), Child)
