from transformers import CLIPTokenizer, CLIPTextModel
import torch

# Load model
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32")

# Text input
commands = ["Pick up the red cube", "Move the blue ball to the right"]

# Tokenize
inputs = tokenizer(commands, return_tensors="pt", padding=True)

# Encode
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :]  # CLS token

print("Command Embedding Shape:", embeddings.shape)  # Should be [2, 512]
