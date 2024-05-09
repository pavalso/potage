from typing import TypeVar, Callable, Union
from abc import ABC
from dataclasses import dataclass
from warnings import warn

from .pot import Pot
from .ingredient import (
    _RootIngredient,
    Ingredient,
    _RootIngredientProxy,
    IngredientProxy,
    IngredientData
)
from .utils import Decorable, Priorized


_B = TypeVar("_B")
_IPT = TypeVar("_IPT")


@dataclass
class Chef(Priorized, ABC):

    def prepare(self,
                ingredient: Ingredient) -> Ingredient:
        return ingredient

    def cook(self,
             line: IngredientProxy[_IPT]) -> IngredientProxy[_IPT]:
        return line


@dataclass
class ChefLine:

    kitchen: "Kitchen"
    chefs: list[Chef]

    def __post_init__(self) -> None:
        self.chefs = Priorized.sort(self.chefs, reverse=True)

    def add(self, chef: Chef) -> None:
        self.chefs.append(chef)
        self.chefs = Priorized.sort(self.chefs, reverse=True)

    def cook(self, line: IngredientProxy[_B]) -> IngredientProxy[_B]:
        for _chef in self.chefs:
            line = _chef.cook(line)
        return line

    def prepare(self, ingredient: Ingredient) -> Ingredient:
        for _chef in self.chefs:
            ingredient = _chef.prepare(ingredient)
        return ingredient


class Kitchen:

    pot: Pot
    chef_line: ChefLine

    def __init__(self, pot: Pot, chefs: list[Chef]) -> None:
        self.pot = pot
        self.chef_line = ChefLine(self, chefs)

    def prepare(
            self,
            _f: Union[Callable, Ingredient] = None,
            /, **kwargs) -> Callable:
        def _wrapper(_f: Union[Callable, Ingredient]) -> Ingredient:
            if kwargs:
                warn("kwargs are not supported in the prepare decorator")

            ingredient: Ingredient = Decorable.sort(_RootIngredient(_f))

            ingredient.formula._type = ingredient.type
            prepared_ingredient = self.chef_line.prepare(ingredient)

            self.pot.add(prepared_ingredient)

            return ingredient.last
        return _wrapper(_f) if _f is not None else _wrapper

    def cook(self, _type: _B, _id: str = None) -> IngredientProxy[_B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        chef_line = _RootIngredientProxy(
            _f=self.pot.get,
            formula=IngredientData(_type=_t, _id=_id))

        return Decorable.sort(self.chef_line.cook(chef_line))
