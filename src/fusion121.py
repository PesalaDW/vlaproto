import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel
import json

original_command = input("Enter your command: ")

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

# Dummy rule-based decoder for now
def decode_action(fused_vector, original_command):
    if "red cube" in original_command:
        target_color = "red"
        target_shape = "cube"
    elif "blue ball" in original_command:
        target_color = "blue"
        target_shape = "ball"
    else:
        target_color = "green"
        target_shape = "cube"
    return target_color, target_shape

target_color, target_shape = decode_action(fused_vector, original_command)

action = {
    "color": target_color,
    "shape": target_shape
}

with open("action_command.json", "w") as f:
    json.dump(action, f)


"""
10x series was used to setup the initial code.
110 adds a command control center
120 takes in commands from the user.
    121 fixes an issue in calling the targets(colour and shape)
    It works now!
"""