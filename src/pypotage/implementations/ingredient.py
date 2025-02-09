from ..abc.ingredientABC import IngredientABC


class Ingredient(IngredientABC):

    def take_out(cls_or_self):
        return cls_or_self.resolve()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.formula.type} -> {self.resolve})"
