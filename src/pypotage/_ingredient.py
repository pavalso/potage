from typing import Generic, TypeVar, Callable, Any
from dataclasses import dataclass, field
from math import inf
from inspect import isclass

from typing_extensions import deprecated


_B = TypeVar("_B")


@dataclass(repr=False)
class IngredientData:

    _type: Any = None
    _id: str = None
    lazy: bool = False
    order: int = inf
    primary: bool = False
    extra: dict = field(default_factory=dict)


@dataclass(repr=False)
class Ingredient:

    _c: Callable

    formula: IngredientData

    @property
    def priority(self) -> int:
        return -inf if self.formula.primary else self.formula.order

    @property
    def type(self) -> Any:
        _annotation = None if not hasattr(self._c, "__annotations__") else \
            self._c.__annotations__.get("return")

        if _annotation is not None:
            return _annotation

        if hasattr(self._c.__wrapped__, "__origin__"):
            return self._c.__wrapped__

        if self.formula.lazy:
            if isclass(self._c.__wrapped__):
                return self._c.__wrapped__

            raise RuntimeError("Lazy ingredients must explicitly \
                define their return type")

        return type(self._c())

    def __call__(self):
        return self._c()


class NoCallIngredient(Ingredient):

    def __init__(self, _c: Callable, formula: IngredientData) -> None:
        def _nocall(*args, **kwargs):
            return _c
        self.__wrapped__ = _c
        _nocall.__annotations__ = _c.__annotations__
        _nocall.__wrapped__ = _c.__wrapped__
        super().__init__(_nocall, formula)

    @property
    def type(self) -> Any:
        if isclass(self._c.__wrapped__):
            return self._c.__wrapped__

        _annotation = None if not hasattr(self._c, "__annotations__") else \
            self._c.__annotations__.get("return")

        if _annotation is not None:
            return _annotation

        if hasattr(self._c.__wrapped__, "__origin__"):
            return self._c.__wrapped__

        raise RuntimeError(
            "No call ingredients must explicitly be annotated or wrap a class")


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

        _ingredients = sorted(_ingredients, key=lambda x: x.priority)

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
