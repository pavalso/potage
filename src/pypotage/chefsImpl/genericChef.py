from typing import Generic

from ..kitchen import Chef
from ..ingredient import IngredientProxy, IngredientData, Ingredient, _B


class _GenericIngredientProxy(IngredientProxy):

    def _get_generic_type(self, formula: IngredientData) -> type:
        return formula.extra.get("__generic_type__")

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        ingredients = super().__call__(formula)

        if not ingredients:
            return ingredients

        _bases = self._get_generic_type(self.formula)

        if _bases is None:
            return ingredients

        _matches = []
        for ingredient in ingredients:
            _ingredient_bases = self._get_generic_type(ingredient.formula)
            for _ingredient_type, _ingredient_args in _ingredient_bases:
                for _type, args in _bases:
                    if not issubclass(_ingredient_type, _type):
                        continue
                    if args != _ingredient_args:
                        continue
                    _matches.append(ingredient)

        return _matches


class GenericChef(Chef):

    @staticmethod
    def _is_generic(_type: type) -> bool:
        return isinstance(_type, type) and \
            issubclass(_type, Generic) or \
            hasattr(_type, "__origin__") and \
            issubclass(_type.__origin__, Generic)

    @staticmethod
    def _get_bases(_type: type) -> list[tuple[type, tuple[type]]]:
        if hasattr(_type, "__origin__"):
            return [(_type.__origin__, _type.__args__)]
        bases = _type.__orig_bases__
        return [(base.__origin__, base.__args__) for base in bases]

    @staticmethod
    def _modify_formula(formula: IngredientData) -> IngredientData:
        formula.extra["__generic_type__"] = \
            GenericChef._get_bases(formula._type)
        if hasattr(formula._type, "__origin__"):
            formula._type = formula._type.__origin__
        return formula

    def prepare(self,
                ingredient: Ingredient) -> Ingredient:
        if not self._is_generic(ingredient.formula._type):
            return ingredient
        ingredient.formula = self._modify_formula(ingredient.formula)
        return ingredient

    def cook(self,
             line: IngredientProxy) -> IngredientProxy[_B]:
        if self._is_generic(line.formula._type):
            line.formula = self._modify_formula(line.formula)
        return _GenericIngredientProxy(_f=line, formula=line.formula)
