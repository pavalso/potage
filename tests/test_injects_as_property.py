import pytest

from src import pypotage


@pytest.fixture(autouse=True)
def reset():
    pypotage.kitchen_.pot.clear()


def test_usable_as_property():
    class Tests:

        test_attribute = pypotage.cook(str)

    test_object = Tests()

    pytest.raises(RuntimeError, test_object.test_attribute)

    @pypotage.prepare
    def test() -> str:
        return "test"

    assert test_object.test_attribute == "test"
