from ...abc.orderABC import OrderABC


class Order(OrderABC):

    def add(cls_or_self, waiter):
        cls_or_self.waiters.append(waiter)
        return waiter

    def remove(cls_or_self, waiter):
        cls_or_self.waiters.remove(waiter)
        return waiter

    def take_out(cls_or_self):
        ingredients = cls_or_self.resolve(cls_or_self.formula)
        
        for waiter in cls_or_self.waiters:
            ingredients = waiter.serve(cls_or_self.formula, ingredients)

        if not ingredients:
            raise RuntimeError("No meals to serve")

        return ingredients[0].take_out()

    @classmethod
    def copy_from(cls_or_self, order):
        return cls_or_self(formula=order.formula, waiters=order.waiters, resolve=order.resolve)
