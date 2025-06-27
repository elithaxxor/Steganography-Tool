from stego import PLUGIN_MAP
from stego_plugins import OutGuess


def test_plugin_map():
    assert PLUGIN_MAP["outguess"] is OutGuess
