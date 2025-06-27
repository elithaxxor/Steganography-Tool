from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from .base import ExternalTool, PluginError


class Aletheia(ExternalTool):
    """Adapter for the Aletheia steganalysis framework."""

    name = "aletheia"
    executable = "aletheia.py"

    async def detect(self, target: Path) -> str:
        process = await self.run(["auto", str(target)])
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()
