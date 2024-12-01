from ...abc.flavourABC import FlavourABC
from ...utils import Priorized
from .staticTypeCheckerFlavour import StaticTypeCheckerFlavour


class LazyFlavour(FlavourABC):

    priority = Priorized.after(StaticTypeCheckerFlavour)

    @classmethod
    def apply_to(cls_or_self, ingredient):
        if ingredient.formula.type is None:
            raise RuntimeError("Lazy ingredients must explicitly \
                define a type")

        ingredient.formula.lazy = True
