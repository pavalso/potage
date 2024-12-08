from abc import (
    ABC,
    abstractmethod
)
from typing import Callable

from objproxies import AbstractProxy

from .formula import Formula
from .chefABC import ChefABC
from .waiterABC import WaiterABC
from .orderABC import OrderABC
from .flavourABC import FlavourABC
from .ingredientABC import IngredientABC


class ChefLineABC(ABC):

    chefs: list[ChefABC]

    @abstractmethod
    def add(cls_or_self, chef: ChefABC) -> ChefABC: ...

    @abstractmethod
    def remove(cls_or_self, chef: ChefABC) -> None: ...

    @abstractmethod
    def cook(cls_or_self, formula: Formula, func: Callable, waiters: list[WaiterABC]) -> OrderABC: ...

    @abstractmethod
    def prepare(cls_or_self, formula: Formula, func: Callable, flavours: list[FlavourABC]) -> IngredientABC: ...

    @abstractmethod
    def pack(cls_or_self, order: OrderABC) -> AbstractProxy: ...
