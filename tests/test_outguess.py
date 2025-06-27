import pytest
from stego_plugins import OutGuess, PluginError


def test_outguess_missing_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    with pytest.raises(PluginError):
        OutGuess()
