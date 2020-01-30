from pydnd import creature


def test_imports():
    assert 'typing' in creature.__dict__


def test_class_existence():
    assert callable(creature.Creature)
