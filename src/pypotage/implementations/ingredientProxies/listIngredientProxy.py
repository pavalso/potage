from .ingredientProxyImpl import IngredientProxyImpl
from ...utils import Priority


class ListIngredientProxy(IngredientProxyImpl):

    priority = Priority.AFTER_FIRST

    def take_out(self, __ingredients = None):
        if __ingredients is None:
            __ingredients = self(self.formula)

        return [ingredient() for ingredient in __ingredients]
