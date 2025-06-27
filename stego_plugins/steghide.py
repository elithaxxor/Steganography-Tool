from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from .base import ExternalTool, PluginError


class StegHide(ExternalTool):
    """Adapter for the ``steghide`` steganography tool."""

    name = "steghide"
    executable = "steghide"

    async def embed(self, carrier: Path, payload: Path, output: Path, password: str | None = None) -> str:
        args: List[str] = ["embed", "-cf", str(carrier), "-ef", str(payload), "-sf", str(output), "-f"]
        if password:
            args += ["-p", password]
        else:
            args += ["-p", ""]
        process = await self.run(args)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()

    async def extract(self, carrier: Path, output: Path, password: str | None = None) -> str:
        args: List[str] = ["extract", "-sf", str(carrier), "-xf", str(output)]
        if password:
            args += ["-p", password]
        else:
            args += ["-p", ""]
        process = await self.run(args)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise PluginError(stderr.decode().strip())
        return stdout.decode().strip()
