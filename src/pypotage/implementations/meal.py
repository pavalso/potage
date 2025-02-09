from objproxies import CallbackProxy

from ..abc.mealABC import MealABC
from ..abc.orderABC import OrderABC


class Meal(MealABC, CallbackProxy):

    __slots__ = ("__order__",)

    def __init__(cls_or_self, order: OrderABC):
        object.__setattr__(cls_or_self, "__order__", order)
        
        resolver = order.take_out
        
        super().__init__(resolver)

    def __enter__(self):
        return self.__subject__.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.__subject__.__exit__(exc_type, exc_val, exc_tb)

    def __getattribute__(cls_or_self, name: str, oga=object.__getattribute__):
        if name == "__order__":
            return oga(cls_or_self, name)
        return super().__getattribute__(name)
