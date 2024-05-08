from typing import (
    Any,
    Iterable,
    Iterator,
    Union)
from abc import ABC
from enum import IntEnum


def traverse_subclasses(cls) -> list:
    if not hasattr(cls, "__subclasses__"):
        return []

    subclasses: list = cls.__subclasses__()

    for subclass in cls.__subclasses__():
        subclasses.extend(traverse_subclasses(subclass))

    return subclasses


class Priority(IntEnum):
    LAST = 0
    BEFORE_LAST = 10000
    MIDDLE = 20000
    AFTER_FIRST = 30000
    FIRST = 40000


class Priorized:

    @property
    def priority(self) -> Priority:
        return Priority.MIDDLE

    @staticmethod
    def sort(line: list["Priorized"], reverse=False) -> list["Priorized"]:
        return sorted(line, key=lambda x: x.priority, reverse=reverse)


# Not thread safe
class Decorable(Priorized, ABC, Iterable):

    _decorator: Any = None
    _last: Any = None
    __iter_last: Any = None

    @property
    def last(self) -> Any:
        if self._last is not None:
            return self._last

        self._last = list(self)[-1]
        return self._last

    @property
    def decorator(self) -> Any:
        return self._decorator

    def __init__(self, decorator: Union["Decorable", Any] = None) -> None:
        self._decorator = decorator

    def __iter__(self) -> Iterator["Decorable"]:
        self.__iter_last = self
        return self

    def __next__(self) -> Any:
        _r = self.__iter_last
        if isinstance(self.__iter_last, Decorable):
            self.__iter_last = self.__iter_last.decorator
            return _r
        self.__iter_last = None
        if _r is not None:
            return _r
        raise StopIteration

    @staticmethod
    def sort(decorable: "Decorable") -> "Decorable":
        line: list[Decorable] = list(decorable)[:-1]
        last = decorable.last
        line = Priorized.sort(line, reverse=False)
        for next in line:
            next._decorator = last
            last = next
        return line[-1]
