from typing import Generic, TypeVar, Callable, Any

from dataclasses import dataclass
from math import inf
from inspect import isclass


_B = TypeVar("_B")


@dataclass(repr=False)
class _IngredientData:

    _type: Any
    _id: str


@dataclass(repr=False)
class _IngredientProxy(Generic[_B]):

    _f: Callable

    formula: _IngredientData

    def is_present(self) -> bool:
        return bool(self._f(self.formula._type, self.formula._id))

    def take_out(self) -> _B:
        _ingredients = self._f(self.formula._type, self.formula._id)

        if _ingredients == []:
            raise RuntimeError("No ingredients found")

        return _ingredients[0]() if _ingredients else None

    def __call__(self) -> _B:
        return self.take_out()


@dataclass(repr=False)
class _Ingredient:

    _c: Callable

    lazy: bool = False
    order: int = inf
    primary: bool = False

    @property
    def priority(self) -> int:
        return -inf if self.primary else self.order

    @property
    def type(self) -> Any:
        _annotation = None if not hasattr(self._c, "__annotations__") else \
            self._c.__annotations__.get("return")

        if self.lazy:
            if isclass(self._c.__wrapped__):
                return self._c.__wrapped__

            if _annotation is None:
                raise RuntimeError("Lazy ingredients must explicitly \
                    define their return type")

        if _annotation is not None:
            return _annotation

        return type(self._c())

    def __call__(self):
        return self._c()
