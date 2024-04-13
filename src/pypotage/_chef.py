from abc import ABC, abstractmethod
from typing import TypeVar

from ._ingredient import _IngredientProxy, _Ingredient


_B = TypeVar("_B")


class Chef(ABC):

    @abstractmethod
    def prepare(self,
                ingredient: _Ingredient) -> _Ingredient:
        return ingredient

    @abstractmethod
    def cook(self,
             line: _IngredientProxy[_B]) -> _IngredientProxy[_B]:
        return line
