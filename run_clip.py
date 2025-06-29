from transformers import CLIPModel, CLIPProcessor

# Load the model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Save to disk
model.save_pretrained("clip-vit-base-patch32")
processor.save_pretrained("clip-vit-base-patch32")