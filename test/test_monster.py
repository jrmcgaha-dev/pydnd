from pydnd import monster


def test_imports():
    assert hasattr(monster, 'typing')
    assert hasattr(monster, 'Creature')
    assert hasattr(monster, 'Roller')


def test_monster():
    assert hasattr(monster, 'Monster')
    assert callable(monster.Monster)
    assert monster.Creature in monster.Monster.__bases__
    sample_monster = monster.Monster()
    assert hasattr(sample_monster, 'alignmnet')
