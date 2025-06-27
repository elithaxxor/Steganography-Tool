import pytest
from stego_plugins import (
    StegHide,
    Zsteg,
    StegExpose,
    Aletheia,
    StegDetector,
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
