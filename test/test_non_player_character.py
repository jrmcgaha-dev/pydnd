from pydnd import non_player_character as npc


def test_imports():
    assert hasattr(npc, 'typing')
    assert hasattr(npc, '_Character')
    assert hasattr(npc, 'Monster')
    assert hasattr(npc, 'Roller')


def test_non_player_character_class():
    assert hasattr(npc, 'NonPlayerCharacter')
    assert callable(npc.NonPlayerCharacter)
    assert npc._Character in npc.NonPlayerCharacter.__bases__
    assert npc.Monster in npc.NonPlayerCharacter.__bases__
    sample_npc = npc.NonPlayerCharacter()
    assert hasattr(sample_npc, 'alignment')
