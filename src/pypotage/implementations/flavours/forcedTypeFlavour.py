from ...abc.flavourABC import FlavourABC
from ...utils import Priority


class ForcedTypeFlavour(FlavourABC):

    priority = Priority.LAST

    @classmethod
    def apply_to(cls_or_self, ingredient):
        if ingredient.formula.type is not None:
            return

        ingr_return = ingredient.resolve()

        if hasattr(ingr_return, "__orig_class__"):
            ingredient.formula.type = ingr_return.__orig_class__
        else:
            ingredient.formula.type = type(ingr_return)
