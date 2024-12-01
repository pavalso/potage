from ...abc.flavourABC import FlavourABC
from .lazyFlavour import LazyFlavour


class NoCallFlavour(FlavourABC):

    @classmethod
    def apply_to(cls_or_self, ingredient):
        LazyFlavour.apply_to(ingredient)

        resolve = ingredient.resolve

        ingredient.resolve = lambda: resolve
