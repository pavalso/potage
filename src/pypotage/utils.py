from typing import (
    Any,
    Iterator,
    Union)
from abc import ABCMeta
from enum import IntEnum

from typing_extensions import Self


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

    priority: int = Priority.MIDDLE

    @staticmethod
    def sort(line: list["Priorized"], reverse=False) -> list["Priorized"]:
        return sorted(line, key=lambda x: x.priority, reverse=not reverse)

    @staticmethod
    def is_ordered(line: list["Priorized"]) -> bool:
        return all(
            line[i].priority >= line[i + 1].priority
            for i in range(len(line) - 1)
        )

    @staticmethod
    def after(cls: "Priorized") -> int:
        return cls.priority - 1

    @staticmethod
    def before(cls: "Priorized") -> int:
        return cls.priority + 1


class DecorableMeta(ABCMeta):

    def __call__(cls, *args, **kwds):
        obj = cls.__new__(cls, *args, **kwds)
        decorates = kwds.get("decorates", None)
        if "decorates" in kwds:
            del kwds["decorates"]
        elif len(args) > 0:
            decorates = args[0]
            args = args[1:]
        obj.__init__(*args, **kwds)
        obj._decorator = decorates
        return obj

    def __new__(
            cls,
            name, bases, namespace, **kwds) -> Self:
        instance = super().__new__(cls, name, bases, namespace, **kwds)
        return instance


class Decorable(Priorized, metaclass=DecorableMeta):

    _decorator: Any = None

    @property
    def last(self) -> Any:
        return list(self)[-1].decorator

    @property
    def decorator(self) -> Any:
        return self._decorator

    def __init__(self, decorates=None) -> None:
        super().__init__()

    def __iter__(self) -> Iterator["Decorable"]:
        self.__iter_last = self
        return self

    def __next__(self) -> Any:
        _r = self.__iter_last
        if isinstance(self.__iter_last, Decorable):
            self.__iter_last = self.__iter_last.decorator
            return _r
        raise StopIteration

    @staticmethod
    def sort(decorable: "Decorable") -> list["Decorable"]:
        line: list[Decorable] = list(decorable)
        last = decorable.last
        line = Priorized.sort(line)
        for next in line[::-1]:
            next._decorator = last
            last = next
        return line

    @staticmethod
    def is_ordered(decorable: "Decorable") -> bool:
        return Priorized.is_ordered(list(decorable)[:-1])

    @staticmethod
    def from_list(
            last: Union["Decorable", Any],
            line: list["Decorable"]) -> "Decorable":
        if not line:
            return last

        sorted_line: list[Decorable] = Priorized.sort(line, reverse=True)

        _old = last
        for decorable in sorted_line:
            ret = decorable(decorates=_old)
            _old = ret

        return Decorable.sort(_old)[0]
