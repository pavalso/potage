from src import pypotage


def test_chef():
    any_proxy = pypotage.ingredients.IngredientProxy(lambda: 1)
    any_ingredient = pypotage.ingredients.Ingredient(lambda: 1)

    assert pypotage.Chef().prepare(any_ingredient) == any_ingredient
    assert pypotage.Chef().cook(any_proxy) == any_proxy
