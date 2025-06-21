from transformers import CLIPTokenizer, CLIPTextModel
import torch

# Load the tokenizer and model (same as before)
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
text_model = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32")

commands = ["Pick up the red cube", "Move the blue ball to the right"]

inputs = tokenizer(commands, return_tensors="pt", padding=True)

with torch.no_grad():
    text_outputs = text_model(**inputs)
    text_embeddings = text_outputs.last_hidden_state[:, 0, :]  # CLS token

print("Text Embedding Shape:", text_embeddings.shape)
print("First command vector:", text_embeddings[0][:10])  # print first 10 dims

#Not doing the saving step that Chat recommended for now. Check doc100 for the prompt response.