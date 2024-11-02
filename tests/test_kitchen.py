from src import pypotage


def test_chef():
    any_proxy = pypotage.ingredients.IngredientProxy(pypotage.IngredientData())

    any_ingredient = pypotage.ingredients.Ingredient(
        pypotage.IngredientData(),
        decorates=lambda: None)

    assert pypotage.Chef().prepare(any_ingredient) == any_ingredient
    assert pypotage.Chef().cook(any_proxy) == any_proxy
