from abc import ABC, abstractmethod
from typing import TypeVar

from ._ingredient import IngredientProxy, Ingredient


_B = TypeVar("_B")


class Chef(ABC):

    @abstractmethod
    def prepare(self,
                ingredient: Ingredient) -> Ingredient:
        return ingredient

    @abstractmethod
    def cook(self,
             line: IngredientProxy[_B]) -> IngredientProxy[_B]:
        return line
