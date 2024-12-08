from abc import (
    ABC,
    abstractmethod
)

from .formula import Formula
from ..utils import Priorized
from .ingredientABC import IngredientABC


class WaiterABC(ABC, Priorized):

    @abstractmethod
    def serve(cls_or_self, formula: Formula, ingredients: list[IngredientABC]) -> list[IngredientABC]: ...
