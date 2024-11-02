from src import pypotage


class RetrieveRawIngredient(pypotage.IngredientProxy):

    priority = pypotage.Priority.LAST

    def take_out(self, __ingredients=None):
        return __ingredients[0]
