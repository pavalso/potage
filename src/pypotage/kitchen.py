from abc import ABC
from dataclasses import dataclass
from warnings import warn
from typing import (
    TypeVar,
    Callable,
    Union,
    Type,
    Generic)

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


class PackedMeal(property, Generic[_IPT]):

    def __init__(self, ingredient: IngredientProxy, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ingredient = ingredient

    def is_present(self) -> bool:
        return self.ingredient.is_present()

    def take_out(self) -> _IPT:
        return self.ingredient.take_out()


@dataclass
class Chef(Priorized, ABC):

    def prepare(self,
                ingredient: Ingredient) -> Ingredient:
        return ingredient

    def cook(self,
             line: IngredientProxy) -> IngredientProxy:
        return line


@dataclass
class ChefLine:

    chefs: list[Type[Chef]]

    def __post_init__(self) -> None:
        self.chefs = Priorized.sort(self.chefs)

    def add(self, chef: Chef) -> None:
        self.chefs.append(chef)
        self.chefs = Priorized.sort(self.chefs)

    def cook(self, line: IngredientProxy) -> IngredientProxy:
        for _chef in self.chefs:
            line = _chef.cook(line)
        return line

    def prepare(self, ingredient: Ingredient) -> Ingredient:
        for _chef in self.chefs:
            ingredient = _chef.prepare(ingredient)
        return ingredient

    def pack(self, ingredient: IngredientProxy) -> PackedMeal:
        return PackedMeal(ingredient, lambda _: ingredient.take_out())


class Kitchen:

    pot: Pot
    chef_line: ChefLine

    def __init__(
            self,
            pot: Pot,
            chefs: Union[ChefLine, list[Type[Chef]]]) -> None:
        self.pot = pot
        self.chef_line = chefs \
            if isinstance(chefs, ChefLine) \
            else ChefLine(chefs)

    def prepare(
            self,
            _f: Union[Callable, Decorable] = None,
            /, **kwargs) -> _B:
        def _wrapper(_f: _B) -> Ingredient:
            if kwargs:
                warn("kwargs are not supported in the prepare decorator")

            ingredient: Ingredient = Decorable.sort(_RootIngredient(_f))

            ingredient.formula._type = ingredient.type
            prepared_ingredient = self.chef_line.prepare(ingredient)

            self.pot.add(prepared_ingredient)

            return ingredient.last
        return _wrapper(_f) if _f is not None else _wrapper

    def cook(
            self,
            _type: _B,
            _id: str = None) -> Union[PackedMeal[_B], _B]:
        if not (_t := getattr(_type, "type", None)):
            _t = _type

        chef_line = _RootIngredientProxy(
            _f=self.pot.get,
            formula=IngredientData(_type=_t, _id=_id))

        last = Decorable.sort(self.chef_line.cook(chef_line))

        return self.chef_line.pack(last)
