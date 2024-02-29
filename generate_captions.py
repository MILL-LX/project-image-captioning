
import glob
from transformers import pipeline

image_dir = "data/mill_fotos_teste"

# captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
# captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

for image_filename in glob.glob(image_dir + '/*'):
    print(captioner(image_filename))

