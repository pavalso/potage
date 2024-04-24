from typing import Callable, Type
from functools import cache

from .ingredient import (
    Ingredient,
    IngredientData
)
from .utils import traverse_subclasses


class Pot:

    ingredients: dict[Type, list[Ingredient]]

    def __init__(self) -> None:
        self.ingredients: dict[Type, list[Ingredient]] = {}

    def create(self, func: Callable, /,
               _ingredient: Type[Ingredient],
               **kwargs) -> Ingredient:
        ingredient = _ingredient(
            _c=cache(func),
            formula=IngredientData(**kwargs))
        ingredient.formula._type = ingredient.type
        return ingredient

    def add(self, ingredient: Ingredient) -> Ingredient:
        _l = self.ingredients.setdefault(
            (ingredient.formula._type, ingredient.formula._id), [])
        _l.insert(0, ingredient)
        return ingredient

    def get(self, formula: IngredientData) -> Ingredient:
        classes = [formula._type]
        classes.extend(traverse_subclasses(formula._type))

        ingredients = []

        for _type in classes:
            ingredient = self.ingredients.get((_type, formula._id))
            if ingredient is not None:
                ingredients.extend(ingredient)

        return ingredients
