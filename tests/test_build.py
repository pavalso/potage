import pypotage


def test_context():
    assert pypotage.prepare is not None
    assert pypotage.cook is not None
    assert pypotage.pot is not None
