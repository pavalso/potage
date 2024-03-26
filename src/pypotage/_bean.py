from typing import Generic, TypeVar, Callable, Type

from dataclasses import dataclass
from math import inf
from inspect import isclass


_B = TypeVar("_B")

@dataclass(kw_only=True, repr=False)
class _BeanProxy(Generic[_B]):

    _f: Callable

    def is_present(self) -> bool:
        return bool(self._f())

    def get(self) -> _B:
        _beans = self._f()

        return _beans[0]() if _beans else None

    def __call__(self) -> _B:
        return self.get()

@dataclass(kw_only=True, repr=False)
class _Bean:

    _c: Callable

    lazy: bool = False
    order: int = inf
    primary: bool = False

    @property
    def priority(self) -> int:
        return -inf if self.primary else self.order

    @property
    def type(self) -> Type:
        _annotation = self._c.__annotations__.get("return")

        if self.lazy:
            if isclass(self._c.__wrapped__):
                return self._c.__wrapped__

            if _annotation is None:
                raise RuntimeError("Lazy beans must explicitly define their return type")
            return _annotation

        return type(self._c())

    def __call__(self):
        return self._c()
