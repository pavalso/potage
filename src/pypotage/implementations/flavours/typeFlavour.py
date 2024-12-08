from ...abc.flavourABC import FlavourABC
from ...utils import Priorized
from .lazyFlavour import LazyFlavour


class TypeFlavour(FlavourABC):

    priority = Priorized.before(LazyFlavour)

    def __init__(self, type: type) -> None:
        self.type = type

    def apply_to(cls_or_self, ingredient):
        ingredient.formula.type = cls_or_self.type
