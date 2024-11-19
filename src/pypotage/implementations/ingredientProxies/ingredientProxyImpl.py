from typing import Any

from pypotage.utils import (
    Priority,
    Decorable
)

from ...abc.formula import Formula
from ...abc.ingredientProxy import IngredientProxy


class IngredientProxyImpl(IngredientProxy, Decorable):

    priority = Priority.MIDDLE

    def __init__(
            self,
            formula: Formula = None,
            decorates: Any = None) -> None:
        self.formula = formula

    def is_present(self) -> bool:
        return bool(self(self.formula))

    def take_out(self, __ingredients = None):
        if __ingredients is None:
            __ingredients = self(self.formula)
        return self.decorator.take_out(__ingredients)

    def __call__(self, formula):
        return self.decorator(formula)
