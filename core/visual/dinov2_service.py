import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import imagehash
from typing import Dict, Any


class VisualFeatureExtractor:
    def __init__(self, model_name: str = "dinov2_vits14"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[VisualFeatureExtractor] Model yukleniyor ({model_name}) - Cihaz: {self.device}...")

        # Meta DINOv2 kucuk ViT modeli
        self.model = torch.hub.load('facebookresearch/dinov2', model_name).to(self.device)
        self.model.eval()

        # DINOv2 girdi boyutu (224x224) ve ImageNet normalizasyonu
        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def extract_dinov2_vector(self, image: Image.Image) -> np.ndarray:
        """Goruntu icin L2 normalize edilmis 384 boyutlu DINOv2 embedding cikarir."""
        img_rgb = image.convert("RGB")
        tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)

        with torch.no_grad():
            embedding = self.model(tensor)
            # Cosine similarity icin L2 normalizasyonu
            embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)

        return embedding.cpu().numpy().flatten()

    def extract_phash(self, image: Image.Image) -> str:
        """Hizli on filtreleme icin Perceptual Hash (pHash) dizesi cikarir."""
        return str(imagehash.phash(image))

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Hem DINOv2 hem pHash cikarir."""
        with Image.open(image_path) as img:
            vector = self.extract_dinov2_vector(img)
            phash_str = self.extract_phash(img)

        return {
            "embedding": vector,
            "phash": phash_str
        }