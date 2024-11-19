from ..abc.meal import Meal


class MealImpl(Meal):

    def add(self, ingredient) -> None:
        self.ingredients.append(ingredient)

    def remove(self, ingredient) -> None:
        self.ingredients.remove(ingredient)
