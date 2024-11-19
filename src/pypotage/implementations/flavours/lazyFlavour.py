from ...abc.flavour import Flavour
from ...utils import Priorized
from .staticTypeCheckerFlavour import StaticTypeCheckerFlavour


class LazyFlavour(Flavour):

    priority = Priorized.after(StaticTypeCheckerFlavour)

    @classmethod
    def apply_to(cls, meal):
        if meal.formula.type is None:
            raise RuntimeError("Lazy ingredients must explicitly \
                define a type")

        meal.formula.lazy = True
