from abc import (
    ABC,
    abstractmethod
)

from .chef import Chef
from .ingredient import Ingredient
from .ingredientProxy import IngredientProxy
from .packedMeal import PackedMeal
from .flavour import Flavour
from .meal import Meal


class ChefLine(ABC):

    @abstractmethod
    def add(self, chef: Chef) -> Chef: ...

    @abstractmethod
    def remove(self, chef: Chef) -> None: ...

    @abstractmethod
    def cook(self, line: IngredientProxy) -> IngredientProxy: ...

    @abstractmethod
    def prepare(self, ingredients: list[Ingredient], flavours: list[Flavour]) -> Meal: ...

    @abstractmethod
    def pack(self, ingredient: IngredientProxy) -> PackedMeal: ...
