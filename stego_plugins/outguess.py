from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from .base import ExternalTool, PluginError


class OutGuess(ExternalTool):
    """Adapter for the `outguess` steganography tool."""

    name = "outguess"
    executable = "outguess"

    async def embed(self, carrier: Path, payload: Path, output: Path) -> str:
        process = await self.run(["-d", str(payload), str(carrier), str(output)])
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()

    async def extract(self, carrier: Path, output: Path) -> str:
        process = await self.run(["-r", str(carrier), str(output)])
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()
