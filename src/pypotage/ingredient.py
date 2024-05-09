from typing import (
    Generic,
    TypeVar,
    Callable,
    Any,
    Union
)
from dataclasses import dataclass, field
from inspect import isclass
from math import inf
from functools import cache

from .utils import Decorable, Priority


_B = TypeVar("_B")


@dataclass
class IngredientData:

    _type: Any = None
    _id: str = None
    lazy: bool = False
    primary: bool = False
    extra: dict = field(default_factory=dict)

    __order: int = inf

    @property
    def order(self) -> int:
        return -inf if self.primary else self.__order

    @order.setter
    def order(self, value: int) -> None:
        self.__order = value


class Ingredient(Decorable):

    formula: IngredientData

    @property
    def priority(self) -> int:
        return Priority.MIDDLE

    @property
    def type(self) -> Any:
        if self.formula._type is not None:
            return self.formula._type

        if not self.decorator == self.last:
            return self.decorator.type

        _annotation = None if not hasattr(self.last, "__annotations__") else \
            self.last.__annotations__.get("return")

        if _annotation is not None:
            return _annotation

        if hasattr(self.last, "__origin__"):
            return self.last

        if isclass(self.last):
            return self.last

        return None

    def __init__(self, _c: Union["Ingredient", Callable]) -> None:
        super().__init__(_c)
        self.formula = _c.formula \
            if isinstance(_c, Ingredient) \
            else IngredientData()

    @cache
    def __call__(self) -> Any:
        return self.decorator()


class _RootIngredient(Ingredient):

    @property
    def priority(self) -> int:
        return inf

    @property
    def type(self) -> Any:
        return super().type or type(self())


class LazyIngredient(Ingredient):

    def __init__(self, _c: Callable) -> None:
        super().__init__(_c)
        self.formula.lazy = True

    @property
    def type(self) -> type:
        type_ = super().type

        if type_ is not None:
            return type_

        raise RuntimeError("Lazy ingredients must explicitly define a type")


class NoCallIngredient(LazyIngredient):

    def __call__(self) -> None:
        return self.decorator


class IngredientProxy(Decorable, Generic[_B]):

    formula: IngredientData

    @property
    def priority(self) -> int:
        return Priority.MIDDLE

    def __init__(
            self,
            _f: Union[Callable, "IngredientProxy"],
            formula: IngredientData = None) -> None:
        super().__init__(_f)
        self.formula = formula

    def is_present(self) -> bool:
        return bool(self(self.formula))

    def take_out(self, __ingredients: list[Ingredient] = None) -> _B:
        if __ingredients is None:
            __ingredients = self(self.formula)
        return self.decorator.take_out(__ingredients)

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        return self.decorator(formula)


class _RootIngredientProxy(IngredientProxy):

    @property
    def priority(self) -> int:
        return -inf

    def take_out(self, __ingredients: list[Ingredient] = None) -> Any:
        if __ingredients == []:
            raise RuntimeError("No ingredients found")

        return __ingredients[0]()

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        _ingredients = super().__call__(formula)

        _ingredients = sorted(
            _ingredients,
            key=lambda x: x.formula.order
        )

        return _ingredients
