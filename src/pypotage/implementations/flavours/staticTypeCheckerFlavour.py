from inspect import isclass

from ...abc.flavour import Flavour
from ...utils import Priority


class StaticTypeCheckerFlavour(Flavour):

    priority = Priority.FIRST

    @classmethod
    def apply_to(cls, meal):
        og_function = meal.root.resolve

        # If is a function
        if hasattr(og_function, "__annotations__") \
                and "return" in og_function.__annotations__:
            meal.formula.type = og_function.__annotations__.get("return")
            return

        # Covers if it is a class or a generic type
        if isclass(og_function):
            meal.formula.type = og_function
            return
