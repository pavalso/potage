from typing import TypeVar
from enum import IntEnum


def traverse_subclasses(cls):
    try:
        subclasses = set(cls.__subclasses__())
    except:
        return set()

    for subclass in subclasses.copy():
        subclasses.update(traverse_subclasses(subclass))

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
