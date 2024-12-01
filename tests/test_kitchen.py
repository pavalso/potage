from src import pypotage


def test_chef():
    any_ingredient = pypotage.Ingredient(
        formula=pypotage.Formula(),
        resolve=lambda: None)

    any_order = pypotage.Order(pypotage.Formula(), [], lambda: any_ingredient)

    assert pypotage.Chef.prepare(any_ingredient) == any_ingredient
    assert pypotage.Chef.cook(any_order) == any_order
