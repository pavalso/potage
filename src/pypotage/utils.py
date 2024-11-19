from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Iterator,
    Protocol,
    TypeVar,
    Union)
from abc import ABCMeta
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


_B = TypeVar("_B", bound="Priorized")

class Priorized:

    priority: int = Priority.MIDDLE

    @staticmethod
    def sort(line: list[_B], reverse=False) -> list[_B]:
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
        obj.decorator = decorates
        return obj

    def __new__(
            cls,
            name, bases, namespace, **kwds):
        return super().__new__(cls, name, bases, namespace, **kwds)


class Decorable(Priorized, metaclass=DecorableMeta):

    decorator: Any = None

    @property
    def last(self) -> Any:
        return list(self)[-1].decorator

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
            next.decorator = last
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
            decorable.decorator = _old
            _old = decorable

        return Decorable.sort(_old)[0]



class Chainned(Protocol):

    def __call__(self, next: "Chain") -> Any:
        ...


@dataclass(kw_only=True)
class Chain(Callable):
    __chain__: list[Chainned] = field(default_factory=list)
    __index__: int = 0

    def __call__(self, *args, **kwargs) -> Any:
        """Allows to be passed to the next ingredient in the chain. Keeps track of the chain."""
        if self.__index__ >= len(self.__chain__):
            raise StopIteration
        self.__index__ += 1
        kwargs["next"] = self
        return self.__chain__[self.__index__](*args, **kwargs)
