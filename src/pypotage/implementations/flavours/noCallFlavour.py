from ...abc.ingredient import Ingredient
from .lazyFlavour import LazyFlavour


class NoCallFlavour(LazyFlavour):

    class NoCallIngredient(Ingredient):

        @classmethod
        def __call__(cls, next):
            return next

    @classmethod
    def apply_to(cls, meal):
        LazyFlavour.apply_to(meal)

        meal.add(cls.NoCallIngredient)
