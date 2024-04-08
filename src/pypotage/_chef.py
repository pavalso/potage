from typing import TypeVar

from ._ingredient import _IngredientProxy


_B = TypeVar("_B")


class Chef:

    def cook(self,
             line: _IngredientProxy) -> _IngredientProxy[_B]: ...
