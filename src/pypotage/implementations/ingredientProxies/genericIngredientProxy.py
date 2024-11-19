from ...abc.formula import Formula
from .ingredientProxyImpl import IngredientProxyImpl


class GenericIngredientProxy(IngredientProxyImpl):

    def _get_generic_type(self, formula: Formula) -> type:
        return formula.extra.get("__generic_type__")

    def __call__(self, formula):
        ingredients = super().__call__(formula)

        if not ingredients:
            return ingredients

        _bases = self._get_generic_type(self.formula)

        if _bases is None:
            return ingredients

        _matches = []
        for ingredient in ingredients:
            _ingredient_bases = self._get_generic_type(ingredient.formula)
            for _ingredient_type, _ingredient_args in _ingredient_bases:
                for _type, args in _bases:
                    if not issubclass(_ingredient_type, _type):
                        continue
                    if args != _ingredient_args:
                        continue
                    _matches.append(ingredient)

        return _matches