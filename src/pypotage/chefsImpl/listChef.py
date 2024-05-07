from ..kitchen import Chef
from ..ingredient import IngredientProxy, _B, Ingredient


class _ListIngredientProxy(IngredientProxy):

    def take_out(self, __ingredients: list[Ingredient] = None) -> list[_B]:
        if __ingredients is None:
            __ingredients = self(self.formula)

        return [ingredient() for ingredient in __ingredients]


class ListChef(Chef):

    def prepare(self, ingredient: Ingredient) -> Ingredient:
        return ingredient

    def cook(self, line: IngredientProxy) -> IngredientProxy[_B]:
        if not getattr(line.formula._type, "__origin__", None) == list:
            return line
        line.formula._type = line.formula._type.__args__[0]
        return _ListIngredientProxy(_f=line, formula=line.formula)
