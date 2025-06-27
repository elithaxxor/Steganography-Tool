"""Pluggable steganography tool adapters with dynamic discovery."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Dict, Type

from .base import ExternalTool, PluginError


def _iter_modules() -> list[ModuleType]:
    for _, name, _ in pkgutil.iter_modules(__path__):
        yield importlib.import_module(f"{__name__}.{name}")


def discover_plugins() -> Dict[str, Type]:
    """Return a mapping of plugin name to class by scanning this package."""
    plugins: Dict[str, Type] = {}
    for module in _iter_modules():
        for obj in module.__dict__.values():
            if inspect.isclass(obj) and getattr(obj, "name", None):
                if obj is ExternalTool or obj is PluginError:
                    continue
                plugins[obj.name] = obj
    return plugins


# Import common plugins so they remain accessible at module level
from .outguess import OutGuess
from .steghide import StegHide
from .zsteg import Zsteg
from .stegexpose import StegExpose
from .aletheia import Aletheia
from .steg_detector import StegDetector
from .audio_lsb import AudioLSB
from .watermark import Watermark
from .network_stego import NetworkStego


__all__ = [
    "ExternalTool",
    "PluginError",
    "OutGuess",
    "StegHide",
    "Zsteg",
    "StegExpose",
    "Aletheia",
    "StegDetector",
    "AudioLSB",
    "Watermark",
    "NetworkStego",
    "discover_plugins",
]
