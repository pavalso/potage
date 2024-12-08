from typing import Generic

from ...abc.chefABC import ChefABC
from ...abc.formula import Formula
from ..waiters import GenericWaiter


class GenericChef(ChefABC):

    @staticmethod
    def _is_generic(_type: type) -> bool:
        return isinstance(_type, type) and \
            issubclass(_type, Generic) or \
            hasattr(_type, "__origin__") and \
            issubclass(_type.__origin__, Generic)

    @staticmethod
    def _get_bases(_type: type) -> list[tuple[type, tuple[type]]]:
        if hasattr(_type, "__origin__"):
            return (_type,)
        return _type.__orig_bases__

    @staticmethod
    def _modify_formula(formula: Formula) -> Formula:
        formula.extra["__generic_type__"] = \
            GenericChef._get_bases(formula.type)
        if hasattr(formula.type, "__origin__"):
            formula.type = formula.type.__origin__
        return formula

    @classmethod
    def prepare(cls_or_self, ingredient):
        if not GenericChef._is_generic(ingredient.formula.type):
            return
        ingredient.formula = GenericChef._modify_formula(ingredient.formula)

    @classmethod
    def cook(cls_or_self, order):
        if not GenericChef._is_generic(order.formula.type):
            return
        order.formula = GenericChef._modify_formula(order.formula)
        order.add(GenericWaiter)
