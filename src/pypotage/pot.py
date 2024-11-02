from typing import Type

from .ingredient import (
    Ingredient,
    IngredientData
)
from .utils import traverse_subclasses


class Pot:

    ingredients: dict[Type, list[Ingredient]]

    def __init__(self) -> None:
        self.ingredients: dict[Type, list[Ingredient]] = {}

    def add(self, ingredient: Ingredient) -> Ingredient:
        _l = self.ingredients.setdefault(
            (ingredient.formula.type, ingredient.formula.id), [])
        _l.insert(0, ingredient)
        return ingredient

    def get(self, formula: IngredientData) -> Ingredient:
        classes = [formula.type]
        classes.extend(traverse_subclasses(formula.type))

        ingredients = []

        for _type in classes:
            ingredient = self.ingredients.get((_type, formula.id))
            if ingredient is not None:
                ingredients.extend(ingredient)

        return ingredients
