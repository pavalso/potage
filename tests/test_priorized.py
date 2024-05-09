from src.pypotage import utils


class Priorized1(utils.Priorized):

    @property
    def priority(self) -> int:
        return utils.Priority.LAST


class Priorized2(utils.Priorized):

    @property
    def priority(self) -> int:
        return utils.Priority.MIDDLE


class Priorized3(utils.Priorized):

    @property
    def priority(self) -> int:
        return utils.Priority.FIRST


def test_does_order():
    sorted_priorized = utils.Priorized.sort(
        [Priorized1(), Priorized3(), Priorized2()])

    actual_expected_pairs = zip(
        sorted_priorized,
        [Priorized3, Priorized2, Priorized1])

    all(
        isinstance(actual, expected)
        for actual, expected in actual_expected_pairs
    )


def test_is_ordered():
    assert utils.Priorized.is_ordered(
        [Priorized3(), Priorized2(), Priorized1()]
    ) is True

    assert utils.Priorized.is_ordered(
        [Priorized1(), Priorized2(), Priorized3()]
    ) is False
