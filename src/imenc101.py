from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Load image from file
image = Image.open("images/image100.png").convert("RGB")

# Load model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Process the image (resizes, normalizes, etc.)
inputs = processor(images=image, return_tensors="pt")

# Encode
with torch.no_grad():
    image_features = model.get_image_features(**inputs)

print("Image Embedding Shape:", image_features.shape)  # Should be [1, 512]
