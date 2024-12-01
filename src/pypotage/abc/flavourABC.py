from abc import (
    ABC,
    abstractmethod
)

from ..utils import Priorized
from .ingredientABC import IngredientABC


class FlavourABC(ABC, Priorized):

    @abstractmethod
    def apply_to(cls_or_self, ingredient: IngredientABC) -> None: ...
