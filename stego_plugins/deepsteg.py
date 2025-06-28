from __future__ import annotations

import asyncio
from pathlib import Path

from .base import PluginError


class DeepSteg:
    """GPU-accelerated steganalysis using a pre-trained model."""

    name = "deep-steg"
    default_model = Path(__file__).with_name("deepsteg_model.pt")

    def __init__(self, model_path: Path | None = None) -> None:
        try:
            import torch
            from PIL import Image
            from torchvision import transforms
        except Exception as exc:  # pragma: no cover - optional deps
            raise PluginError(f"Missing deep learning dependencies: {exc}")

        self.torch = torch
        self.Image = Image
        self.transforms = transforms

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = Path(model_path or self.default_model)
        if not self.model_path.exists():
            raise PluginError(f"Model file not found: {self.model_path}")
        try:
            self.model = torch.jit.load(str(self.model_path), map_location=self.device)
            self.model.eval()
        except Exception as exc:
            raise PluginError(f"Failed to load model: {exc}")

        self.preprocess = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])

    async def detect(self, target: Path) -> str:
        return await asyncio.to_thread(self._detect_sync, target)

    def _detect_sync(self, target: Path) -> str:
        img = self.Image.open(target).convert("RGB")
        tensor = self.preprocess(img).unsqueeze(0).to(self.device)
        with self.torch.no_grad():
            prob = float(self.model(tensor).squeeze().cpu())
        return f"{prob:.4f}"
