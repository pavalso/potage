from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from .formula import Formula
from .waiterABC import WaiterABC
from .ingredientABC import IngredientABC


_Waiter = TypeVar("_Waiter", bound=WaiterABC)

@dataclass
class OrderABC(ABC):

    formula: Formula
    waiters: list[WaiterABC]
    resolve: Callable[..., list[IngredientABC]]

    @abstractmethod
    def add(cls_or_self, waiter: _Waiter) -> _Waiter: ...

    @abstractmethod
    def remove(cls_or_self, waiter: WaiterABC) -> None: ...

    @abstractmethod
    def take_out(cls_or_self) -> Any: ...

    @abstractmethod
    def copy_from(cls_or_self, order: "OrderABC") -> None: ...

    def is_prepared(cls_or_self) -> bool:
        try:
            return bool(cls_or_self.take_out())
        except RuntimeError:
            return False
