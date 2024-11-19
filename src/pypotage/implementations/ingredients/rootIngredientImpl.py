from typing import Any, Callable

from ...abc.rootIngredient import RootIngredient


class RootIngredientImpl(RootIngredient):

    def __init__(self, resolve) -> None:
        self.resolve = resolve

    def __call__(self, next = None) -> Any:
        return self.resolve()
