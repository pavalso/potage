from functools import cache

from ...abc.flavourABC import FlavourABC
from .lazyFlavour import LazyFlavour


class SingletonFlavour(FlavourABC):

    @classmethod
    def apply_to(cls_or_self, ingredient):
        LazyFlavour.apply_to(ingredient)

        resolve = ingredient.resolve

        ingredient.resolve = cache(resolve)
