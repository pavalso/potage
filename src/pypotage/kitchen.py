from typing import TypeVar, Callable, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass
from warnings import warn

from .pot import Pot
from .ingredient import (
    _RootIngredient,
    Ingredient,
    _OrderedIngredientProxy,
    IngredientProxy,
    IngredientData
)


_B = TypeVar("_B")
_IPT = TypeVar("_IPT")


@dataclass
class Chef(ABC):

    kitchen: "Kitchen"

    @abstractmethod
    def prepare(self,
                ingredient: Ingredient) -> Ingredient: ...

    @abstractmethod
    def cook(self,
             line: IngredientProxy[_IPT]) -> IngredientProxy[_IPT]: ...


@dataclass
class ChefLine:

    kitchen: "Kitchen"
    chefs: list[Chef]

    def __post_init__(self) -> None:
        self.chefs = [chef(self.kitchen) for chef in self.chefs]

    def add(self, chef: Chef) -> None:
        self.chefs.append(chef(self.kitchen))

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
    chefLine: ChefLine

    def __init__(self, pot: Pot, chefs: list[type[Chef]]) -> None:
        self.pot = pot
        self.chefLine = ChefLine(self, chefs)

    def prepare(
            self,
            _f: Union[Callable, Ingredient] = None,
            /, **kwargs) -> Callable:
        def _wrapper(_f: Union[Callable, Ingredient]) -> Ingredient:
            if kwargs:
                warn("kwargs are not supported in the prepare decorator")

            ingredient = _RootIngredient(_f)

            line = [
                ingredient
                for ingredient
                in ingredient
                if type(ingredient) is not Ingredient][:-1]
            _f = line[-1].decorator
            line.sort(key=lambda x: x.priority)
            last = line[-1]
            last._decorator = _f
            for next in line[:-1][::-1]:
                next._decorator = last
                last = next

            ingredient.formula._type = ingredient.type
            prepared_ingredient = self.chefLine.prepare(ingredient)

            self.pot.add(prepared_ingredient)

            return ingredient.last
        return _wrapper(_f) if _f is not None else _wrapper

    def cook(self, _type: _B, _id: str = None) -> IngredientProxy[_B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        chef_line = _OrderedIngredientProxy(
            _f=self.pot.get,
            formula=IngredientData(_type=_t, _id=_id))

        return self.chefLine.cook(chef_line)
