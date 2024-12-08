from abc import (
    ABC,
    abstractmethod
)

from .formula import Formula
from .ingredientABC import IngredientABC


class PotABC(ABC):

    @abstractmethod
    def add(cls_or_self, ingredient: IngredientABC) -> IngredientABC: ...

    @abstractmethod
    def remove(cls_or_self, ingredient: IngredientABC) -> None: ...

    @abstractmethod
    def get(cls_or_self, formula: Formula) -> list[IngredientABC]: ...

    @abstractmethod
    def clear(cls_or_self) -> None: ...
