from .order import Order


class ListOrder(Order):

    def take_out(cls_or_self):
        ingredients = cls_or_self.resolve(cls_or_self.formula)

        for waiter in cls_or_self.waiters:
            ingredients = waiter.serve(cls_or_self.formula, ingredients)

        return [ingredient.take_out() for ingredient in ingredients]
