import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel

image_features = torch.load("image_embeddings.pt")
text_features = torch.load("text_embeddings.pt")

# Normalize
image_embeddings = F.normalize(image_features, dim=-1)
text_embeddings = F.normalize(text_features, dim=-1)

# Concatenate
combined = torch.cat([image_embeddings, text_embeddings], dim=-1)  # shape: [batch, 1024]

# Define MLP (you can tune hidden dims or add dropout)
fusion_mlp = nn.Sequential(
    nn.Linear(1024, 512),
    nn.ReLU(),
    nn.Linear(512, 128),  # This is now the fused multimodal representation
)

fused_vector = fusion_mlp(combined)  # shape: [batch, 128]
