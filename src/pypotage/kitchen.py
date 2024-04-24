from math import inf
from typing import TypeVar

from .chefLine import ChefLine

from .pot import Pot
from .ingredient import (
    Ingredient,
    _OrderedIngredientProxy,
    IngredientProxy,
    IngredientData,
    NoCallIngredient
)


_B = TypeVar("_B")


class Kitchen:

    pot: Pot
    chefLine: ChefLine

    def __init__(self, pot: Pot, chefLine: ChefLine) -> None:
        self.pot = pot
        self.chefLine = chefLine

    def prepare(self, _f: _B = None, /,
                lazy: bool = False, order: int = inf,
                primary: bool = False, _id: str = None,
                no_call: bool = False) -> _B:
        def _wrapper(_f) -> Ingredient:
            # Not so pypotonic as it should be :(
            ingredient = self.pot.create(
                _f, lazy=lazy,
                _ingredient=NoCallIngredient if no_call else Ingredient,
                order=order, primary=primary,
                _id=_id)

            self.pot.add(
                self.chefLine.prepare(ingredient))
            return _f
        return _wrapper(_f) if _f is not None else _wrapper

    def cook(self, _type: _B, _id: str = None) -> IngredientProxy[_B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        chef_line = _OrderedIngredientProxy(
            _f=self.pot.get,
            formula=IngredientData(_type=_t, _id=_id))

        return self.chefLine.cook(chef_line)
