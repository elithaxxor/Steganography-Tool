import os
from pathlib import Path

import pytest

from stego_plugins.deepsteg import DeepSteg, MODEL_URL


def test_deepsteg_download(monkeypatch, tmp_path):
    downloaded = {}

    def fake_urlretrieve(url, filename):
        downloaded['url'] = url
        Path(filename).write_bytes(b'model')

    monkeypatch.setattr('stego_plugins.deepsteg.urllib.request.urlretrieve', fake_urlretrieve)

    model_path = tmp_path / 'deepsteg_model.pt'
    ds = DeepSteg(model_path)
    assert model_path.exists()
    assert downloaded['url'] == MODEL_URL
    assert ds.model_path == model_path
