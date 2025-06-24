from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Load multiple images
image_paths = ["images/image100.png", "images/image101.png"]
images = [Image.open(img_path).convert("RGB") for img_path in image_paths]

# Load model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Process multiple images
inputs = processor(images=images, return_tensors="pt", padding=True)

# Encode
with torch.no_grad():
    image_features = model.get_image_features(**inputs)

print("Image Embedding Shape:", image_features.shape)  # Should be [2, 512]

# Save embeddings
torch.save(image_features, "image_embeddings.pt")
