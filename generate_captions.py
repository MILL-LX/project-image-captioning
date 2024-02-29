
import glob
from os import path
from transformers import pipeline

image_dir = "data/mill_fotos_teste"

models = ["Salesforce/blip-image-captioning-base", "Salesforce/blip-image-captioning-large", "nlpconnect/vit-gpt2-image-captioning"]
captioners = []
for model in models:
    captioners.append(pipeline("image-to-text", model=model, max_new_tokens=128))

for image_file_path in glob.glob(image_dir + '/*'):
    image__filename = path.basename(image_file_path)

    print("\n\n")
    print(image__filename)

    for i in range(len(captioners)):
        caption = captioners[i](image_file_path)[0]['generated_text']
        print(f'\t{models[i]}: {caption}')



