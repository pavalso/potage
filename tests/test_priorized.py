from src.pypotage import utils


class Priorized1(utils.Priorized):

    priority = utils.Priority.LAST


class Priorized2(utils.Priorized):

    priority = utils.Priority.MIDDLE


class Priorized3(utils.Priorized):

    priority = utils.Priority.FIRST


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


def test_after_and_before_methods():
    class AfterPriorized1(utils.Priorized):

        priority = utils.Priorized.after(Priorized1)

    assert utils.Priorized.is_ordered(
        [Priorized1(), AfterPriorized1()]
    )

    class BeforePriorized1(utils.Priorized):

        priority = utils.Priorized.before(Priorized1)

    assert utils.Priorized.is_ordered(
        [BeforePriorized1(), Priorized1()]
    )
