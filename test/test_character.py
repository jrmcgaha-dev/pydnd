from pydnd import _character


def test_imports():
    assert hasattr(_character, "typing")
    assert hasattr(_character, "Creature")
    assert hasattr(_character, "Roller")


def test_character_class():
    assert hasattr(_character, "_Character")
    assert callable(_character._Character)
    assert _character.Creature in _character._Character.__bases__
    sample_character = _character._Character()
    assert hasattr(sample_character, "alignment")
