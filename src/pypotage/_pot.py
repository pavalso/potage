from typing import Callable, Type, TypeVar
from functools import cache
from math import inf

from .chefs.listChef import ListChef
from .chefs.genericChef import GenericChef
from ._ingredient import (
    Ingredient,
    _OrderedIngredientProxy,
    IngredientProxy,
    IngredientData
)
from .utils import traverse_subclasses
from ._chef import Chef


_B = TypeVar("_B")


class _Pot:

    ingredients: dict[Type, list[Ingredient]]
    chefs: list[Chef]

    def __init__(self) -> None:
        self.ingredients: dict[Type, list[Ingredient]] = {}
        self.chefs: list[Chef] = [
            ListChef(),
            GenericChef()
        ]

    def create(self, func: Callable, /, **kwargs) -> Ingredient:
        ingredient = Ingredient(
            _c=cache(func),
            formula=IngredientData(**kwargs))
        ingredient.formula._type = ingredient.type
        return ingredient

    def add(self, ingredient: Ingredient) -> Ingredient:
        _l = self.ingredients.setdefault(
            (ingredient.formula._type, ingredient.formula._id), [])
        _l.insert(0, ingredient)
        return ingredient

    def get(self, formula: IngredientData) -> Ingredient:
        classes = [formula._type]
        classes.extend(traverse_subclasses(formula._type))

        ingredients = []

        for _type in classes:
            ingredient = self.ingredients.get((_type, formula._id))
            if ingredient is not None:
                ingredients.extend(ingredient)

        return ingredients

    def prepare(self, _f: _B = None, /,
                lazy: bool = False, order: int = inf,
                primary: bool = False, _id: str = None) -> _B:
        def _wrapper(_f) -> Ingredient:
            ingredient = self.create(
                _f, lazy=lazy, order=order, primary=primary, _id=_id)

            for chef in self.chefs:
                ingredient = chef.prepare(ingredient)

            self.add(ingredient)
            return _f
        return _wrapper(_f) if _f is not None else _wrapper

    def cook(self, _type: _B, _id: str = None) -> IngredientProxy[_B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        chef_line = _OrderedIngredientProxy(
            _f=self.get,
            formula=IngredientData(_type=_t, _id=_id))

        for chef in self.chefs:
            chef_line = chef.cook(chef_line)

        return chef_line


pot = _Pot()
