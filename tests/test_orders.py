import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_create_order():
    order = pypotage.Order(
        formula=pypotage.Formula(),
        waiters=[pypotage.Waiter],
        resolve=lambda: None
    )

    assert order.formula is not None
    assert order.waiters is not None
    assert len(order.waiters) == 1
    assert order.waiters[0] is pypotage.Waiter
    assert order.resolve is not None


def test_remove_waiter():
    order = pypotage.Order(
        formula=pypotage.Formula(),
        waiters=[pypotage.Waiter],
        resolve=lambda: None
    )

    assert len(order.waiters) == 1

    order.remove(pypotage.Waiter)

    assert len(order.waiters) == 0


def test_add_waiter():
    order = pypotage.Order(
        formula=pypotage.Formula(),
        waiters=[pypotage.Waiter],
        resolve=lambda: None
    )

    assert len(order.waiters) == 1

    order.add(pypotage.Waiter)

    assert len(order.waiters) == 2
