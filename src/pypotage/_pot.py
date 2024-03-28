from typing import Callable, Type, TypeVar
from functools import cache, partial
from math import inf

from ._ingredient import _Ingredient, _IngredientProxy
from .utils import traverse_subclasses


_B = TypeVar("_B")


class _Pot:
    ingredients: dict[Type, list[_Ingredient]] = {}

    @classmethod
    def create(cls, func: Callable, /, **kwargs) -> _Ingredient:
        return _Ingredient(_c=cache(func), **kwargs)

    @classmethod
    def add(cls, ingredient: _Ingredient, _id: str) -> _Ingredient:
        (_l := cls.ingredients.setdefault((ingredient.type, _id), [])).append(ingredient)
        list.sort(_l, key=lambda _b: _b.priority)
        return ingredient

    @classmethod
    def get(cls, _type: Type, _id: str) -> _Ingredient:
        classes = [_type]
        classes.extend(traverse_subclasses(_type))

        ingredients = []

        for _type in classes:
            if (ingredient := cls.ingredients.get((_type, _id))) is not None:
                ingredients.extend(ingredient)

        list.sort(ingredients, key=lambda ingredient: ingredient.priority)

        return ingredients

    @classmethod
    def prepare(cls, _f: _B = None,
             /, lazy: bool = False, order: int = inf, primary: bool = False, _id: str = None) -> _B:
        def _wrapper(_f) -> _Ingredient:
            ingredient = cls.create(_f, lazy=lazy, order=order, primary=primary)
            cls.add(ingredient, _id=_id)
            return _f
        print(_f)
        return _wrapper(_f) if _f is not None else _wrapper

    @classmethod
    def cook(cls, _type: _B, _id: str = None) -> _IngredientProxy[_B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        return _IngredientProxy(_f=partial(cls.get, _t, _id))

pot = _Pot()
