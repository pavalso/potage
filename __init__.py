from src import pypotage


#if __name__ == "__main__":
#    @pypotage.prepare(no_call=True)
#    class Test:
#        def __init__(self):
#            print("Test.__init__")
#
#    @pypotage.prepare(no_call=True, lazy=True)
#    def test() -> str:
#        print("test")
#        return "test"
#
#    t = pypotage.cook(Test).take_out()
#    s = pypotage.cook(Test).take_out()
#
#    print(t())
#    print(s())


from abc import ABC, abstractmethod
from dataclasses import field
from typing import Any, Callable
from math import inf
from inspect import isclass


class IngredientFactory:

    def __init__(self) -> None:
        self.ingredients: dict[
            Callable,
            tuple[
                pypotage.ingredients.IngredientData,
                list[Ingredient]
                ]
            ] = {}

    def add(
            self,
            _f: Callable,
            ingredient: "Ingredient") -> None:
        _data = self.ingredients.setdefault(
            _f,
            (ingredient.formula, [_RootIngredient(_f, ingredient.formula)])
            )
        _data[1].append((ingredient))
        _data[1].sort(key=lambda x: x.priority)

    def get(
            self, _f: Callable) -> tuple[
                pypotage.ingredients.IngredientData,
                list["Ingredient"]]:
        return self.ingredients.get(
            _f, [pypotage.ingredients.IngredientData(), []])

    def type(self, _f: Callable) -> Any:
        ingredients = self.get(_f)[1]
        for ingredient in ingredients:
            _type = ingredient.type
            if _type is not None:
                return _type

    def prepare(self, _f: "Ingredient" | Callable) -> Callable:
        if not isinstance(_f, Ingredient):
            _f = _RootIngredient(_f, pypotage.ingredients.IngredientData())

        formula = _f.formula
        _buf = []
        while isinstance(_f, Ingredient):
            _buf.append(_f)
            _f.formula = formula
            _f = _f._c
        _data = self.ingredients.setdefault(_f, (formula, _buf))
        _data[1].sort(key=lambda x: x.priority)
        return _f


factory = IngredientFactory()


class Ingredient(ABC):

    _c: "Ingredient" | Callable

    formula: pypotage.ingredients.IngredientData

    def __init__(self, _c: "Ingredient" | Callable) -> None:
        self._c = _c

    @property
    def priority(self) -> int:
        return -inf if self.formula.primary else self.formula.order

    @property
    def type(self) -> Any:
        _annotation = None if not hasattr(self._c, "__annotations__") else \
            self._c.__annotations__.get("return")

        if _annotation is not None:
            return _annotation

        if hasattr(self._c, "__origin__"):
            return self._c

        if isclass(self._c):
            return self._c

        return None
    
    

    def __call__(self):
        return self._c()


class _RootIngredient(Ingredient):

    @property
    def priority(self) -> int:
        return inf

    @property
    def type(self) -> Any:
        return type(self())


class Lazy(Ingredient):

    @property
    def type(self) -> Any:
        type_ = super().type

        if type_ is not None:
            return type_

        raise RuntimeError("Lazy ingredients must explicitly \
            define their return type")


class NoCall(Lazy):

    ...


@factory.prepare
@Lazy
@NoCall
def Test() -> str:
    print("Test.__init__")
    return "test"


print(factory.type(Test))
