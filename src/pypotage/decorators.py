from typing import Callable, Union

from .ingredient import (
    Ingredient,
    LazyIngredient,
    NoCallIngredient
)


def ingredient(
        ingredient_type: type[Ingredient]) -> Ingredient:
    def _wrapper(_wrap: Union[Ingredient, Callable]) -> Ingredient:
        return ingredient_type(_wrap)
    if not issubclass(ingredient_type, Ingredient):
        raise TypeError("ingredient_type must be an Ingredient")
    return _wrapper


def _formula_from_callable(_wrap: Union[Ingredient, Callable]) -> Ingredient:
    return Ingredient(_wrap) if not isinstance(_wrap, Ingredient) else _wrap


def lazy(_wrap: Union[Ingredient, Callable] = None) -> Ingredient:
    return ingredient(LazyIngredient)(_wrap) \
        if _wrap is not None \
        else ingredient(LazyIngredient)


def no_call(_wrap: Union[Ingredient, Callable] = None) -> Ingredient:
    return ingredient(NoCallIngredient)(_wrap) \
        if _wrap is not None \
        else ingredient(NoCallIngredient)


def order(value: int) -> Ingredient:
    def _wrap(_wrap: Union[Ingredient, Callable]) -> Ingredient:
        _r = _formula_from_callable(_wrap)
        _r.formula.order = value
        return _r
    return _wrap


def id(value: str) -> Ingredient:
    def _wrap(_wrap: Union[Ingredient, Callable]) -> Ingredient:
        _r = _formula_from_callable(_wrap)
        _r.formula._id = value
        return _r
    return _wrap


def primary(_wrap: Union[Ingredient, Callable] = None) -> Ingredient:
    def _wrapper(_wrap: Union[Ingredient, Callable]) -> Ingredient:
        _r = _formula_from_callable(_wrap)
        _r.formula.primary = True
        return _r
    return _wrapper(_wrap) if _wrap is not None else _wrapper


def type(value: type) -> Ingredient:
    def _wrap(_wrap: Union[Ingredient, Callable]) -> Ingredient:
        _r = _formula_from_callable(_wrap)
        _r.formula._type = value
        return _r
    return _wrap
