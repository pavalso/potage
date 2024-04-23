from typing import TypeVar

from .ingredient import Ingredient, IngredientProxy
from .chef import Chef


_B = TypeVar("_B")


class ChefLine:

    chefs: list[Chef]

    def __init__(self, chefs: list[Chef]) -> None:
        self.chefs = chefs

    def add(self, chef: Chef) -> None:
        self.chefs.append(chef)

    def remove(self, chef: Chef) -> None:
        self.chefs.remove(chef)

    def cook(self, line: IngredientProxy[_B]) -> IngredientProxy[_B]:
        for _chef in self.chefs:
            line = _chef.cook(line)
        return line

    def prepare(self, ingredient: Ingredient) -> Ingredient:
        for _chef in self.chefs:
            ingredient = _chef.prepare(ingredient)
        return ingredient
