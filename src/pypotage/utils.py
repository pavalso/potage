from typing import (
    Any,
    Iterable,
    Iterator,
    Union)
from abc import ABC, abstractmethod
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


# Not thread safe
class Decorable(ABC, Iterable):

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

    @property
    @abstractmethod
    def priority(self) -> int: ...

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
        line.sort(key=lambda x: x.priority)
        for next in line:
            next._decorator = last
            last = next
        return line[-1]
