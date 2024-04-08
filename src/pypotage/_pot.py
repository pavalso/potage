from typing import Callable, Type, TypeVar
from functools import cache
from math import inf

from .chefs.listChef import ListChef

from ._ingredient import _Ingredient, _IngredientProxy, _IngredientData
from .utils import traverse_subclasses
from ._chef import Chef


_B = TypeVar("_B")


class _Pot:

    ingredients: dict[Type, list[_Ingredient]]
    chefs: list[Chef]

    def __init__(self) -> None:
        self.ingredients: dict[Type, list[_Ingredient]] = {}
        self.chefs: list[Chef] = [
            ListChef(),
        ]

    def create(self, func: Callable, /, **kwargs) -> _Ingredient:
        return _Ingredient(_c=cache(func), **kwargs)

    def add(self, ingredient: _Ingredient, _id: str) -> _Ingredient:
        (_l := self.ingredients.setdefault((ingredient.type, _id), [])) \
            .insert(0, ingredient)
        list.sort(_l, key=lambda _b: _b.priority)
        return ingredient

    def get(self, _type: Type, _id: str) -> _Ingredient:
        classes = [_type]
        classes.extend(traverse_subclasses(_type))

        ingredients = []

        for _type in classes:
            if (ingredient := self.ingredients.get((_type, _id))) is not None:
                ingredients.extend(ingredient)

        list.sort(ingredients, key=lambda ingredient: ingredient.priority)

        return ingredients

    def prepare(self, _f: _B = None, /,
                lazy: bool = False, order: int = inf,
                primary: bool = False, _id: str = None) -> _B:
        def _wrapper(_f) -> _Ingredient:
            ingredient = self.create(
                _f, lazy=lazy, order=order, primary=primary)
            self.add(ingredient, _id=_id)
            return _f
        return _wrapper(_f) if _f is not None else _wrapper

    def cook(self, _type: _B, _id: str = None) -> _IngredientProxy[_B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        chef_line = _IngredientProxy(
            _f=self.get,
            formula=_IngredientData(_type=_t, _id=_id))

        for chef in self.chefs:
            chef_line = chef.cook(chef_line)

        return chef_line


pot = _Pot()
