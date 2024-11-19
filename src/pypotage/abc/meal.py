from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..abc.formula import Formula
from .ingredient import Ingredient
from .rootIngredient import RootIngredient


@dataclass
class Meal(ABC):

    formula: Formula
    ingredients: list[Ingredient]
    
    @property
    def root(self) -> RootIngredient:
        assert isinstance(self.ingredients[0], RootIngredient)
        return self.ingredients[0]

    @abstractmethod
    def add(self, ingredient: Ingredient) -> Ingredient: ...

    @abstractmethod
    def remove(self, ingredient: Ingredient) -> None: ...
