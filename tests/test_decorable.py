from src.pypotage import utils


def test_create_decorated_line():
    last = utils.Decorable()

    line = utils.Decorable(utils.Decorable(last))

    assert line.decorator != last
    assert isinstance(line.decorator, utils.Decorable)
    assert line.last == last


def test_decorated_list():
    last = utils.Decorable()

    line = utils.Decorable(last)

    assert list(line) == [line, last]

    assert utils.Decorable.is_ordered(line) is True
    assert utils.Decorable.sort(line) == line


def test_decorated_unordered_list():
    element1 = utils.Decorable()
    element1.priority = utils.Priority.MIDDLE

    element2 = utils.Decorable(element1)
    element2.priority = utils.Priority.FIRST

    element3 = utils.Decorable(element2)
    element3.priority = utils.Priority.LAST

    assert utils.Decorable.is_ordered(element3) is False
    sorted = utils.Decorable.sort(element3)
    list(sorted) == [element2, element1, element3]
    assert utils.Decorable.is_ordered(element3) is True
