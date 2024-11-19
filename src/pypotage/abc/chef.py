from abc import (
    ABC,
    abstractmethod
)

from .meal import Meal
from .packedMeal import PackedMeal
from .ingredientProxy import IngredientProxy

from ..utils import Priorized


class Chef(ABC, Priorized):

    @staticmethod
    @abstractmethod
    def prepare(meal: Meal) -> None: ...

    @staticmethod
    @abstractmethod
    def cook(line: IngredientProxy) -> IngredientProxy: ...

    @staticmethod
    @abstractmethod
    def pack(ingredientProxy: IngredientProxy) -> PackedMeal: ...
