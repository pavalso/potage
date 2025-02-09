from ...abc.formula import Formula
from ...abc.waiterABC import WaiterABC


class GenericWaiter(WaiterABC):

    @staticmethod
    def _get_generic_type(formula: Formula) -> type:
        return formula.extra["__generic_type__"]

    @classmethod
    def serve(cls_or_self, formula, ingredients):
        if not ingredients:
            return ingredients

        _bases = cls_or_self._get_generic_type(formula)

        _matches = []
        for ingredient in ingredients:
            _ingredient_bases = cls_or_self._get_generic_type(ingredient.formula)
            cls_or_self._check_bases(_bases, _matches, ingredient, _ingredient_bases)

        return _matches

    @classmethod
    def _check_bases(cls_or_self, _bases, _matches, ingredient, _ingredient_bases):
        for _ingredient_base in _ingredient_bases:
            _ingredient_type, _ingredient_args = _ingredient_base.__origin__, _ingredient_base.__args__
            for _base in _bases:
                if not hasattr(_base, "__origin__"):
                    continue
                _type, args = _base.__origin__, _base.__args__ or _base.__parameters__
                if not issubclass(_ingredient_type, _type):
                    continue
                args = [arg for arg in args if isinstance(arg, type)]
                _ingredient_args = [arg for arg in _ingredient_args if isinstance(arg, type)]
                if not all([issubclass(pair[0], pair[1]) for pair in zip(_ingredient_args, args)]):
                    continue
                _matches.append(ingredient)
                break
