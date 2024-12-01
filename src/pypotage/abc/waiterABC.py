from abc import (
    ABC,
    abstractmethod
)

from .formula import Formula
from ..utils import Priorized
from .ingredientABC import IngredientABC


class WaiterABC(ABC, Priorized):

    def is_present(cls_or_self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def serve(cls_or_self, formula: Formula, ingredients: list[IngredientABC]) -> list[IngredientABC]: ...
