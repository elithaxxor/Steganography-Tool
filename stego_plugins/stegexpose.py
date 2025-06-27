from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from .base import ExternalTool, PluginError


class StegExpose(ExternalTool):
    """Adapter for the ``stegexpose`` detection tool."""

    name = "stegexpose"
    executable = "stegexpose"

    async def detect(self, target: Path) -> str:
        process = await self.run([str(target)])
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()
