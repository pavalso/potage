from ...abc.chefABC import ChefABC
from .genericChef import GenericChef
from ..waiters import ListOrder


class ListChef(ChefABC):

    priority = ChefABC.before(GenericChef)

    @classmethod
    def cook(cls_or_self, order):
        if not getattr(order.formula.type, "__origin__", None) == list:
            return
        order.formula.type = order.formula.type.__args__[0]

        return ListOrder.copy_from(order)
