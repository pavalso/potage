from dataclasses import (
    dataclass,
    field
)
from typing import Type
from math import inf

from ..utils import Priority


@dataclass
class Formula:

    type: Type = None
    id: str = None
    lazy: bool = False
    primary: bool = False
    extra: dict = field(default_factory=dict)

    __order: int = Priority.MIDDLE

    @property
    def order(self) -> int:
        return -inf if self.primary else self.__order

    @order.setter
    def order(self, value: int) -> None:
        self.__order = value
