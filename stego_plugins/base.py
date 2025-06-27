from __future__ import annotations

import asyncio
import shutil
from pathlib import Path
from typing import List


class PluginError(Exception):
    """Raised when a plugin operation fails."""


class ExternalTool:
    """Base class for external steganography tools."""

    name: str
    executable: str

    def __init__(self) -> None:
        if not shutil.which(self.executable):
            raise PluginError(f"Required tool '{self.executable}' not found in PATH")

    async def run(self, args: List[str]) -> asyncio.subprocess.Process:
        process = await asyncio.create_subprocess_exec(
            self.executable,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        return process

    async def embed(self, *args: str) -> str:
        raise NotImplementedError

    async def extract(self, *args: str) -> str:
        raise NotImplementedError
