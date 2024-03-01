
import glob
from os import path
import time
from transformers import pipeline

image_dir = 'data/mill_fotos_teste'

models = ['Salesforce/blip-image-captioning-base', 
          'Salesforce/blip-image-captioning-large', 
          'nlpconnect/vit-gpt2-image-captioning']

start = time.perf_counter()
captioners = [pipeline('image-to-text', model=model, max_new_tokens=128) for model in models]
finish = time.perf_counter()
print(f'Model loading took {finish-start:0.4f} seconds.')

with open('captions.txt', 'w') as captions_file:

    for image_file_path in glob.glob(image_dir + '/*'):
        start = time.perf_counter()
        image__filename = path.basename(image_file_path)

        print(image__filename, file=captions_file)

        for model, captioner in zip(models, captioners):
            caption = captioner(image_file_path)[0]['generated_text']
            print(f'\t{model}: {caption}', file=captions_file)

        print('\n', file=captions_file)

        finish = time.perf_counter()
        print(f'Image captioning took {finish-start:0.4f} seconds.')
