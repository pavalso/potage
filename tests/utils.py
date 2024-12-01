from src import pypotage


class RetrieveRawIngredient(pypotage.abc.Waiter):

    priority = pypotage.Priority.LAST

    @classmethod
    def serve(cls_or_self, formula, ingredients):
        return ingredients[0]


class RetrieveRawIngredientChef(pypotage.Chef):

    @classmethod
    def cook(cls_or_self, order):
        return RetrieveRawIngredientOrder.copy_from(order)


class RetrieveRawIngredientOrder(pypotage.Order):

    def take_out(cls_or_self):
        ingredients = cls_or_self.resolve(cls_or_self.formula)

        for waiter in cls_or_self.waiters:
            ingredients = waiter.serve(cls_or_self.formula, ingredients)

        return ingredients[0]
