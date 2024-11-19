from ...abc.flavour import Flavour
from ...utils import Priority


class ForcedTypeFlavour(Flavour):

    priority = Priority.LAST

    @classmethod
    def apply_to(cls, meal):
        if meal.formula.type is not None:
            return

        ingr_return = meal.root()

        if hasattr(ingr_return, "__orig_class__"):
            meal.formula.type = ingr_return.__orig_class__
        else:
            meal.formula.type = type(ingr_return)
