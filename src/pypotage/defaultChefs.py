from typing import Generic

from .kitchen import Chef
from .ingredient import IngredientProxy, Ingredient, IngredientData
from .utils import Priority


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
            GenericChef._get_bases(formula.type)
        if hasattr(formula.type, "__origin__"):
            formula.type = formula.type.__origin__
        return formula

    def prepare(self,
                ingredient: Ingredient) -> Ingredient:
        if not self._is_generic(ingredient.formula.type):
            return ingredient
        ingredient.formula = self._modify_formula(ingredient.formula)
        return ingredient

    def cook(self,
             line: IngredientProxy) -> IngredientProxy:
        if self._is_generic(line.formula.type):
            line.formula = self._modify_formula(line.formula)
        return _GenericIngredientProxy(formula=line.formula, decorates=line)


class _ListIngredientProxy(IngredientProxy):

    @property
    def priority(self) -> int:
        return Priority.AFTER_FIRST

    def take_out(self, __ingredients: list[Ingredient] = None) -> list:
        if __ingredients is None:
            __ingredients = self(self.formula)

        return [ingredient() for ingredient in __ingredients]


class ListChef(Chef):

    @property
    def priority(self) -> int:
        return Priority.AFTER_FIRST

    def prepare(self, ingredient: Ingredient) -> Ingredient:
        return ingredient

    def cook(self, line: IngredientProxy) -> IngredientProxy:
        if not getattr(line.formula.type, "__origin__", None) == list:
            return line
        line.formula.type = line.formula.type.__args__[0]
        return _ListIngredientProxy(formula=line.formula, decorates=line)
