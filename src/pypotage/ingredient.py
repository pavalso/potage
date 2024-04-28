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

from typing_extensions import deprecated

from .utils import Decorable


_B = TypeVar("_B")


@dataclass
class IngredientData:

    _type: Any = None
    _id: str = None
    lazy: bool = False
    order: int = 999999
    primary: bool = False
    extra: dict = field(default_factory=dict)


class Ingredient(Decorable):

    formula: IngredientData

    @property
    def priority(self) -> int:
        return 0

    @property
    def type(self) -> Any:
        if self.formula._type is not None:
            return self.formula._type
        if not self.decorator == self.last:
            return self.decorator.type
        return None

    def __init__(self, _c: Union["Ingredient", Callable]) -> None:
        super().__init__(_c)
        self.formula = _c.formula \
            if isinstance(_c, Ingredient) \
            else IngredientData()

    @cache
    def __call__(self) -> Any:
        return self.decorator()


class TypedIngredient(Ingredient):

    @property
    def type(self) -> Any:
        _type = super().type

        if _type is not None:
            return _type

        _annotation = None if not hasattr(self.last, "__annotations__") else \
            self.last.__annotations__.get("return")

        if _annotation is not None:
            return _annotation

        if hasattr(self.last, "__origin__"):
            return self.last

        if isclass(self.last):
            return self.last

        return None


class _RootIngredient(TypedIngredient):

    @property
    def priority(self) -> int:
        return -inf

    @property
    def type(self) -> Any:
        return super().type or type(self())


class LazyIngredient(TypedIngredient):

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

    @property
    def priority(self) -> int:
        return 100

    def __call__(self) -> None:
        return self.decorator


@dataclass(repr=False)
class IngredientProxy(Generic[_B]):

    _f: "IngredientProxy"

    formula: IngredientData

    def is_present(self) -> bool:
        return bool(self(self.formula))

    def take_out(self, __ingredients: list[Ingredient] = None) -> _B:
        if __ingredients is None:
            __ingredients = self(self.formula)
        return self._f.take_out(__ingredients)

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        return self._f(formula)


class _RootIngredientProxy(IngredientProxy):

    _f: Callable

    def take_out(self, __ingredients: list[Ingredient] = None) -> Any:
        if __ingredients == []:
            raise RuntimeError("No ingredients found")

        return __ingredients[0]()


class _OrderedIngredientProxy(_RootIngredientProxy):

    def __call__(self, formula: IngredientData) -> list[Ingredient]:
        _ingredients = super().__call__(formula)

        _ingredients = sorted(
            _ingredients,
            key=lambda x: -inf if x.formula.primary else x.formula.order
        )

        return _ingredients


@deprecated("Use `Ingredient` instead")
class _Ingredient(Ingredient):
    ...


@deprecated("Use `IngredientProxy` instead")
class _IngredientProxy(IngredientProxy):
    ...


@deprecated("Use `OrderedIngredientProxy` instead")
class _IngredientData(IngredientData):
    ...
