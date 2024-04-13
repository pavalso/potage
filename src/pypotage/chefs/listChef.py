from .._chef import Chef
from .._ingredient import _IngredientProxy, _B, _Ingredient


class _ListIngredientProxy(_IngredientProxy):

    def take_out(self) -> list[_B]:
        ingredients: list[_Ingredient] = self._f(
            self.formula._type, self.formula._id)

        return [ingredient() for ingredient in ingredients]


class ListChef(Chef):

    def prepare(self, ingredient: _Ingredient) -> _Ingredient:
        return super().prepare(ingredient)

    def cook(self, line: _IngredientProxy) -> _IngredientProxy[_B]:
        if not getattr(line.formula._type, "__origin__", None) == list:
            return line
        line.formula._type = line.formula._type.__args__[0]
        return _ListIngredientProxy(_f=line._f, formula=line.formula)
