from __future__ import annotations

import asyncio
import wave
from pathlib import Path

from .base import PluginError


class AudioLSB:
    """Simple LSB WAV steganography."""

    name = "audio-lsb"

    def __init__(self) -> None:
        pass

    async def embed(self, carrier: Path, payload: Path, output: Path) -> str:
        with wave.open(str(carrier), 'rb') as w:
            params = w.getparams()
            frames = bytearray(w.readframes(w.getnframes()))
        with open(payload, 'rb') as f:
            data = f.read() + b'<<<END>>>'
        bits = ''.join(f'{byte:08b}' for byte in data)
        if len(bits) > len(frames):
            raise PluginError('Carrier too small')
        for i, bit in enumerate(bits):
            frames[i] = (frames[i] & 0xFE) | int(bit)
        with wave.open(str(output), 'wb') as w:
            w.setparams(params)
            w.writeframes(bytes(frames))
        return 'ok'

    async def extract(self, carrier: Path, output: Path) -> str:
        with wave.open(str(carrier), 'rb') as w:
            frames = bytearray(w.readframes(w.getnframes()))
        bits = [str(frames[i] & 1) for i in range(len(frames))]
        bytes_out = [int(''.join(bits[i:i+8]), 2) for i in range(0, len(bits), 8)]
        data = bytes(bytes_out)
        end = data.find(b'<<<END>>>')
        if end == -1:
            raise PluginError('End marker not found')
        with open(output, 'wb') as f:
            f.write(data[:end])
        return 'ok'
