from typing import Generic

from .._chef import Chef
from .._ingredient import IngredientProxy, _B, IngredientData, Ingredient


class _GenericIngredientProxy(IngredientProxy[_B]):

    def _get_generic_type(self, formula: IngredientData) -> type:
        return formula.extra.get("__generic_type__")

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        ingredients = super().__call__(formula)

        ingredients = [
            ingredient for ingredient in ingredients
            if self._get_generic_type(self.formula)
            == self._get_generic_type(ingredient.formula)]

        return ingredients


class GenericChef(Chef):

    def _is_generic(self, _type: type) -> bool:
        return isinstance(_type, type) and \
            issubclass(_type, Generic) or \
            hasattr(_type, "__origin__") and \
            issubclass(_type.__origin__, Generic)

    def _modify_formula(self, formula: IngredientData) -> IngredientData:
        generic_type = None
        _type = formula._type
        if hasattr(formula._type, "__origin__"):
            generic_type = formula._type.__args__
            _type = formula._type.__origin__
        elif hasattr(formula._type, "__orig_bases__"):
            generic_type = formula._type.__orig_bases__[0].__args__
        formula.extra["__generic_type__"] = generic_type
        formula._type = _type
        return formula

    def prepare(self, ingredient: Ingredient) -> Ingredient:
        if not self._is_generic(ingredient.formula._type):
            return ingredient
        ingredient.formula = self._modify_formula(ingredient.formula)
        return ingredient

    def cook(self, line: IngredientProxy) -> IngredientProxy[_B]:
        if self._is_generic(line.formula._type):
            line.formula = self._modify_formula(line.formula)
        return _GenericIngredientProxy(_f=line, formula=line.formula)
