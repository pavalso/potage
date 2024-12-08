from ..abc.ingredientABC import IngredientABC


class Ingredient(IngredientABC):

    def take_out(cls_or_self):
        return cls_or_self.resolve()
