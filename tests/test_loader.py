from stego import PLUGIN_MAP
from stego_plugins import OutGuess, discover_plugins


def test_plugin_map():
    discovered = discover_plugins()
    assert PLUGIN_MAP["outguess"] is OutGuess
    assert "outguess" in discovered
