import wave
from pathlib import Path

import pytest

from stego_plugins import AudioLSB, PluginError


def create_sample_wav(path: Path) -> None:
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(8000)
        w.writeframes(bytes([0] * 8000))


def test_audio_embed_extract(tmp_path: Path) -> None:
    carrier = tmp_path / "c.wav"
    create_sample_wav(carrier)
    payload = tmp_path / "p.txt"
    payload.write_text("secret")
    output = tmp_path / "out.wav"
    extract_file = tmp_path / "extracted.txt"

    plugin = AudioLSB()
    import asyncio
    asyncio.run(plugin.embed(carrier, payload, output))
    asyncio.run(plugin.extract(output, extract_file))

    assert extract_file.read_text() == "secret"
