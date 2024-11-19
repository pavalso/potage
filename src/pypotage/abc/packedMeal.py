from abc import ABC

from objproxies import AbstractProxy

from .ingredientProxy import IngredientProxy


class PackedMeal(ABC, AbstractProxy):

    __slots__ = "__ingredient__"

    __ingredient__: IngredientProxy
