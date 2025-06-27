from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from .base import ExternalTool, PluginError


class StegDetector(ExternalTool):
    """Adapter for the STEG-Detector tool."""

    name = "steg-detector"
    executable = "STEG-Detector.py"

    async def detect(self, target: Path) -> str:
        process = await self.run([str(target)])
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()
