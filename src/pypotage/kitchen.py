from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
    Union,
    Type,
    Callable,
    overload
)

from typing_extensions import Self

from .pot import Pot
from .ingredient import (
    Flavour,
    Ingredient,
    IngredientProxy,
    IngredientData
)
from .ingredientProxies import _RootIngredientProxy
from .flavours import (
    ForcedTypeFlavour,
    StaticTypeCheckerFlavour
)
from .utils import Priorized


_B = TypeVar("_B")


class PackedMeal(property, Generic[_B]):

    def __init__(self, ingredient: IngredientProxy, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ingredient = ingredient

    def is_present(self) -> bool:
        return self.ingredient.is_present()

    def take_out(self) -> _B:
        return self.ingredient.take_out()

    @overload
    def __get__(
        self,
        instance: None,
        owner: Union[type, None] = None) -> Self: ...

    @overload
    def __get__(
        self,
        instance: Any,
        owner: Union[type, None] = None) -> _B: ...

    def __get__(
            self,
            instance: Any,
            owner: Union[type, None] = None) -> Union[_B, Self]:
        return super().__get__(instance, owner)


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

    def __init__(self, chefs: list[Type[Chef]] = None) -> None:
        self.chefs = chefs or []
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
            pot: Pot = None,
            chefs: Union[ChefLine, list[Type[Chef]]] = None) -> None:
        self.pot = pot or Pot()
        self.chef_line = chefs \
            if isinstance(chefs, ChefLine) \
            else ChefLine(chefs)

    def prepare(
            self,
            _f: Callable = None,
            *flavours: list[Flavour]) -> Callable:
        def _wrapper(_f: Callable) -> Callable:
            ingredient = Ingredient(
                formula=IngredientData(),
                decorates=_f
            )

            ordered_flavours = Priorized.sort([
                ForcedTypeFlavour,
                StaticTypeCheckerFlavour,
                *flavours])

            for flavour in ordered_flavours:
                ingredient = ingredient.apply(flavour)

            ingredient = Ingredient.sort(ingredient)[0]

            self.chef_line.prepare(
                ingredient=ingredient
                )

            self.pot.add(ingredient)

            return _f

        called_decorator = _f is None  # @pypotage.prepare()

        if called_decorator:
            return _wrapper

        flavoured = isinstance(_f, Flavour) or \
            isinstance(_f, type) and issubclass(_f, Flavour)

        if flavoured:
            flavours = [_f, *flavours]
            return _wrapper

        return _wrapper(_f)

    def cook(
            self,
            type: _B,
            id: str = None,
            proxies: list[IngredientProxy] = None
            ) -> PackedMeal[_B]:
        if not (_t := getattr(type, "type", None)):
            _t = type

        order = _RootIngredientProxy(
            formula=IngredientData(type=_t, id=id),
            decorates=self.pot.get)

        cooked_order = self.chef_line.cook(order)
        cooked_order = IngredientProxy.from_list(cooked_order, proxies)

        ordered_proxies = IngredientProxy.sort(cooked_order)

        return self.chef_line.pack(ordered_proxies[0])
