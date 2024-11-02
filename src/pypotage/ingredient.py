from abc import ABC, abstractmethod
from typing import (
    Generic,
    TypeVar,
    Callable,
    Any
)
from dataclasses import dataclass, field
from math import inf

from .utils import Decorable, Priority, Priorized


_B = TypeVar("_B")


@dataclass
class IngredientData:

    type: Any = None
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


class Flavour(Priorized, ABC):

    @abstractmethod
    def apply_to(self, ingredient: "Ingredient") -> "Ingredient": ...


class Ingredient(Decorable, ABC, Callable):

    formula: IngredientData

    def __init__(
            self,
            formula: IngredientData,
            decorates: Any = None) -> None:
        self.formula = formula

    def apply(self, flavour: Flavour) -> "Ingredient":
        return flavour.apply_to(self)

    def retrieve(self) -> Any:
        return self.decorator()

    def __call__(self) -> Any:
        return self.retrieve()


class IngredientProxy(Decorable, Generic[_B]):

    formula: IngredientData

    @property
    def priority(self) -> int:
        return Priority.MIDDLE

    def __init__(
            self,
            formula: IngredientData = None,
            decorates: Any = None) -> None:
        self.formula = formula

    def is_present(self) -> bool:
        return bool(self(self.formula))

    def take_out(self, __ingredients: list[Ingredient] = None) -> _B:
        if __ingredients is None:
            __ingredients = self(self.formula)
        return self.decorator.take_out(__ingredients)

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        return self.decorator(formula)
