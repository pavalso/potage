from typing import Any
from math import inf

from .ingredient import Ingredient, IngredientData, IngredientProxy


class _RootIngredientProxy(IngredientProxy):

    priority = -inf

    def take_out(self, __ingredients: list[Ingredient] = None) -> Any:
        if __ingredients == []:
            raise RuntimeError("No ingredients found")

        return __ingredients[0].retrieve()

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        _ingredients = super().__call__(formula)

        _ingredients = sorted(
            _ingredients,
            key=lambda x: x.formula.order
        )

        return _ingredients
