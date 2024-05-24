from typing import Any
from math import inf

from .utils import (
    Priority,
    Priorized)
from .ingredient import (
    Ingredient,
    Flavour
)


class ForcedTypeFlavour(Flavour):

    priority: Priority = -inf

    @staticmethod
    def apply_to(ingredient: Ingredient) -> Ingredient:
        if ingredient.formula.type is not None:
            return ingredient

        ingr_return = ingredient()
        ingredient.formula.type = type(ingr_return)

        return ingredient


class StaticTypeCheckerFlavour(Flavour):

    priority: Priority = inf

    @staticmethod
    def apply_to(ingredient: Ingredient) -> Ingredient:
        # If is a function
        if hasattr(ingredient.last, "__annotations__"):
            ingredient.formula.type = \
                ingredient.last.__annotations__.get("return")
            return ingredient

        # Covers if it is a class or a generic type
        ingredient.formula.type = ingredient.last
        return ingredient


class LazyFlavour(Flavour):

    priority = Priorized.after(StaticTypeCheckerFlavour)

    @staticmethod
    def apply_to(ingredient: Ingredient) -> Ingredient:
        if ingredient.formula.type is None:
            raise RuntimeError("Lazy ingredients must explicitly \
                define a type")

        ingredient.formula.lazy = True
        return ingredient


class OrderFlavour(Flavour):

    def __init__(self, order: int) -> None:
        self.order = order

    def apply_to(self, ingredient: Ingredient) -> Ingredient:
        ingredient.formula.order = self.order
        return ingredient


class PrimaryFlavour(Flavour):

    @staticmethod
    def apply_to(ingredient: Ingredient) -> Ingredient:
        ingredient.formula.primary = True
        return ingredient


class IdFlavour(Flavour):

    def __init__(self, id: str) -> None:
        self.id = id

    def apply_to(self, ingredient: Ingredient) -> Ingredient:
        ingredient.formula.id = self.id
        return ingredient


class TypeFlavour(Flavour):

    def __init__(self, type: Any) -> None:
        self.type = type

    def apply_to(self, ingredient: Ingredient) -> Ingredient:
        ingredient.formula.type = self.type
        return ingredient


class NoCallFlavour(Flavour):

    class NoCallIngredient(Ingredient):

        priority = Priority.LAST

        def retrieve(self) -> Any:
            return self.decorator

    @staticmethod
    def apply_to(ingredient: Ingredient) -> Ingredient:
        ingredient = LazyFlavour.apply_to(ingredient)

        return NoCallFlavour.NoCallIngredient(
            formula=ingredient.formula,
            decorates=ingredient)
