from objproxies import AbstractProxy

from .orderABC import OrderABC


class MealABC(AbstractProxy):

    __order__: OrderABC
