from objproxies import CallbackProxy

from ..abc.ingredientProxy import IngredientProxy
from ..abc.packedMeal import PackedMeal


class PackedMealImpl(PackedMeal, CallbackProxy):

    @property
    def __class__(self):
        return \
            super().__getattribute__("__class__") \
            if self.__ingredient__.is_present() else \
            self.__ingredient__.formula.type

    def __init__(self, ingredient: IngredientProxy):
        func = ingredient.take_out
        object.__setattr__(self, "__ingredient__", ingredient)
        super().__init__(func)

    def __getattribute__(self, attr, oga=object.__getattribute__):
        if attr in ("__ingredient__", "__class__"):
            return oga(self, attr)
        return super().__getattribute__(attr, oga)
