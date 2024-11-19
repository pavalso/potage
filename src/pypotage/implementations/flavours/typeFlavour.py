from ...abc.flavour import Flavour
from ...utils import Priorized
from .lazyFlavour import LazyFlavour


class TypeFlavour(Flavour):

    priority = Priorized.before(LazyFlavour)

    def __init__(self, type: type) -> None:
        self.type = type

    def apply_to(self, meal):
        meal.formula.type = self.type
