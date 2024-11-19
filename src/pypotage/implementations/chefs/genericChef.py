from typing import Generic

from ...abc.meal import Meal
from ...abc.chef import Chef
from ...abc.ingredientProxy import IngredientProxy
from ...abc.formula import Formula
from ..ingredientProxies import GenericIngredientProxy


class GenericChef(Chef):

    @staticmethod
    def _is_generic(_type: type) -> bool:
        return hasattr(_type, "__origin__") and \
            issubclass(_type.__origin__, Generic)

    @staticmethod
    def _get_bases(_type: type) -> list[tuple[type, tuple[type]]]:
        if hasattr(_type, "__origin__"):
            return [(_type.__origin__, _type.__args__)]
        bases = _type.__orig_bases__
        return [(base.__origin__, base.__args__) for base in bases]

    @staticmethod
    def _modify_formula(formula: Formula) -> Formula:
        formula.extra["__generic_type__"] = \
            GenericChef._get_bases(formula.type)
        if hasattr(formula.type, "__origin__"):
            formula.type = formula.type.__origin__
        return formula

    @staticmethod
    def prepare(meal) -> None:
        if not GenericChef._is_generic(meal.formula.type):
            return
        meal.formula = GenericChef._modify_formula(meal.formula)

    @staticmethod
    def cook(line: IngredientProxy) -> IngredientProxy:
        if not GenericChef._is_generic(line.formula.type):
            return line
        line.formula = GenericChef._modify_formula(line.formula)
        return GenericIngredientProxy(formula=line.formula, decorates=line)
