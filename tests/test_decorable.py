from src.pypotage import utils


def do_nothing():
    pass


def test_create_decorated_line():
    line = utils.Decorable(utils.Decorable(do_nothing))

    assert line.decorator != do_nothing
    assert isinstance(line.decorator, utils.Decorable)
    assert line.last == do_nothing


def test_decorated_list():
    decorable_1 = utils.Decorable(do_nothing)
    decorable_2 = utils.Decorable(decorable_1)

    assert list(decorable_2) == [decorable_2, decorable_1]
    assert utils.Decorable.is_ordered(decorable_2) is True
    assert utils.Decorable.sort(decorable_2) == [decorable_2, decorable_1]

    decorable_2.priority = utils.Priority.LAST
    assert utils.Decorable.sort(decorable_2) == [decorable_1, decorable_2]


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


def test_decorated_():
    class Decorable1(utils.Decorable):
        priority = utils.Priority.FIRST

    class Decorable2(utils.Decorable):
        priority = utils.Priority.MIDDLE

    class Decorable3(utils.Decorable):
        priority = utils.Priority.LAST

    decorable = utils.Decorable.from_list(
        last=do_nothing,
        line=[Decorable3, Decorable2, Decorable1])

    assert len(list(decorable)) == 3
    assert utils.Decorable.is_ordered(decorable) is True
    assert decorable.last == do_nothing

    new_decorable = utils.Decorable.from_list(
        last=decorable,
        line=[Decorable3, Decorable2, Decorable1])

    assert len(list(new_decorable)) == 6
    assert new_decorable.last == do_nothing
