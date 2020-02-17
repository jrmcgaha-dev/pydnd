from pydnd import player


def test_imports():
    assert hasattr(player, 'typing')
    assert hasattr(player, '_Character')
    assert hasattr(player, 'Roller')


def test_player_class():
    assert hasattr(player, 'Player')
    assert callable(player.Player)
    assert player._Character in player.Player.__bases__
    sample_player = player.Player()
    assert hasattr(sample_player, 'alignment')
