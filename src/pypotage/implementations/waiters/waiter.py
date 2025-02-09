from ...abc.waiterABC import WaiterABC
from ...utils import Priority

class Waiter(WaiterABC):

    priority = Priority.LAST

    @classmethod
    def serve(cls_or_self, formula, ingredients):
        ingredients = [
            ingredient
            for ingredient in ingredients
            if ingredient.formula.id == formula.id]

        ingredients = sorted(
            ingredients,
            key=lambda ingredient: ingredient.formula.order,
            reverse=True
        )

        return ingredients
