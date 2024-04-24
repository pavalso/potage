from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from .ingredient import IngredientProxy, Ingredient


_B = TypeVar("_B")


@dataclass
class Chef(ABC):

    @abstractmethod
    def prepare(self,
                ingredient: Ingredient) -> Ingredient:
        return ingredient

    @abstractmethod
    def cook(self,
             line: IngredientProxy[_B]) -> IngredientProxy[_B]:
        return line
