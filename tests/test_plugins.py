import pytest
from stego_plugins import (
    StegHide,
    Zsteg,
    StegExpose,
    Aletheia,
    StegDetector,
    DeepSteg,
    PluginError,
)


def test_steghide_missing_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    with pytest.raises(PluginError):
        StegHide()


def test_zsteg_missing_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    with pytest.raises(PluginError):
        Zsteg()


def test_stegexpose_missing_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    with pytest.raises(PluginError):
        StegExpose()


def test_aletheia_missing_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    with pytest.raises(PluginError):
        Aletheia()


def test_steg_detector_missing_binary(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None)
    with pytest.raises(PluginError):
        StegDetector()


def test_deepsteg_missing_deps(monkeypatch):
    import builtins

    orig_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("torch"):
            raise ModuleNotFoundError("no module named 'torch'")
        return orig_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(PluginError):
        DeepSteg()

