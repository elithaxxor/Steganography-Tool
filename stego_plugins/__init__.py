"""Pluggable steganography tool adapters with dynamic discovery."""

from __future__ import annotations

import importlib
import inspect
import os
import pkgutil
import sys
from types import ModuleType
from functools import lru_cache
from typing import Dict, Type, Iterable

from .base import ExternalTool, PluginError


def _iter_modules() -> Iterable[ModuleType]:
    """Yield modules found in the package and any user plugin paths."""
    # built-in plugins bundled with the package
    for _, name, _ in pkgutil.iter_modules(__path__):
        yield importlib.import_module(f"{__name__}.{name}")

    # dynamically load plugins from STEGO_PLUGIN_PATH
    extra_paths = os.environ.get("STEGO_PLUGIN_PATH", "")
    for path in [p for p in extra_paths.split(os.pathsep) if p]:
        if path not in sys.path:
            sys.path.append(path)
        for _, mod_name, _ in pkgutil.iter_modules([path]):
            yield importlib.import_module(mod_name)


@lru_cache(maxsize=1)
def discover_plugins() -> Dict[str, Type[ExternalTool]]:
    """Return a mapping of plugin name to class by scanning this package."""
    plugins: Dict[str, Type[ExternalTool]] = {}
    for module in _iter_modules():
        for obj in module.__dict__.values():
            if inspect.isclass(obj) and getattr(obj, "name", None):
                if obj is ExternalTool or obj is PluginError:
                    continue
                plugins[obj.name] = obj
    return plugins


def reload_plugins() -> Dict[str, Type[ExternalTool]]:
    """Clear the plugin cache and rediscover plugins."""
    discover_plugins.cache_clear()
    return discover_plugins()


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
from .deepsteg import DeepSteg


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
    "DeepSteg",
    "discover_plugins",
    "reload_plugins",
]
