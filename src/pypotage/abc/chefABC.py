from abc import (
    ABC,
    abstractmethod
)

from .ingredientABC import IngredientABC
from .orderABC import OrderABC

from ..utils import Priorized


class ChefABC(ABC, Priorized):

    @classmethod
    @abstractmethod
    def prepare(cls_or_self, ingredient: IngredientABC) -> IngredientABC:
        return ingredient

    @classmethod
    @abstractmethod
    def cook(cls_or_self, order: OrderABC) -> OrderABC:
        return order
