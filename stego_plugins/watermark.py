from __future__ import annotations

import base64
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image, PngImagePlugin

from .base import PluginError


class Watermark:
    """Embed and verify AES-GCM watermarks in PNG metadata."""

    name = "watermark"

    def __init__(self, key: bytes | None = None) -> None:
        self.key = key or AESGCM.generate_key(bit_length=128)
        self.aesgcm = AESGCM(self.key)

    async def embed(self, carrier: Path, text: str, output: Path) -> str:
        img = Image.open(carrier)
        meta = PngImagePlugin.PngInfo()
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, text.encode(), None)
        meta.add_text("watermark", base64.b64encode(nonce + ciphertext).decode())
        img.save(output, pnginfo=meta)
        return "ok"

    async def extract(self, carrier: Path) -> str:
        img = Image.open(carrier)
        data = img.info.get("watermark")
        if not data:
            raise PluginError("Watermark not found")
        raw = base64.b64decode(data)
        nonce, ct = raw[:12], raw[12:]
        text = self.aesgcm.decrypt(nonce, ct, None)
        return text.decode()
