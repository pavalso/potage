from inspect import isclass

from ...abc.flavourABC import FlavourABC
from ...utils import Priority


class StaticTypeCheckerFlavour(FlavourABC):

    priority = Priority.FIRST

    @classmethod
    def apply_to(cls_or_self, ingredient):
        resolver = ingredient.resolve

        # If is a function
        if hasattr(resolver, "__annotations__") \
                and "return" in resolver.__annotations__:
            ingredient.formula.type = resolver.__annotations__.get("return")
            return

        # Covers if it is a class or a generic type
        if isclass(resolver):
            ingredient.formula.type = resolver
            return
