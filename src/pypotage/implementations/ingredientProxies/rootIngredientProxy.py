from typing import Callable

from .ingredientProxyImpl import IngredientProxyImpl
from ...abc.ingredient import Ingredient
from ...utils import Priority

class RootIngredientProxy(IngredientProxyImpl):

    priority = Priority.LAST

    decorator: Callable[..., list[Ingredient]]

    def take_out(self, __ingredients = None):
        if __ingredients == []:
            raise RuntimeError("No ingredients found")

        return __ingredients[0].retrieve()

    def __call__(self, formula):
        _ingredients = self.decorator(formula)

        _ingredients = [
            ingredient
            for ingredient in _ingredients
            if ingredient.formula.id == formula.id]

        _ingredients = sorted(
            _ingredients,
            key=lambda x: x.formula.order
        )

        return _ingredients
