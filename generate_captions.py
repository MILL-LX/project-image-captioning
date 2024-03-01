
import glob
from os import path
from transformers import pipeline

image_dir = 'data/mill_fotos_teste'

models = ['Salesforce/blip-image-captioning-base', 
          'Salesforce/blip-image-captioning-large', 
          'nlpconnect/vit-gpt2-image-captioning']

captioners = [pipeline('image-to-text', model=model, max_new_tokens=128) for model in models]

with open('captions.txt', 'w') as captions_file:

    for image_file_path in glob.glob(image_dir + '/*'):
        image__filename = path.basename(image_file_path)

        print(image__filename, file=captions_file)

        for model, captioner in zip(models, captioners):
            caption = captioner(image_file_path)[0]['generated_text']
            print(f'\t{model}: {caption}', file=captions_file)

        print('\n', file=captions_file)
