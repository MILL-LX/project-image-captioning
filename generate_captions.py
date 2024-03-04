import glob
from os import path
import time

from PIL import Image
from PIL.ExifTags import TAGS
from transformers import pipeline

from lib.util import write_caption_to_exif

image_dir = 'data/input'
output_dir = 'data/output'

models = ['Salesforce/blip-image-captioning-base', 
          'Salesforce/blip-image-captioning-large', 
          'nlpconnect/vit-gpt2-image-captioning']

start = time.perf_counter()
captioners = [pipeline('image-to-text', model=model, max_new_tokens=128) for model in models]
finish = time.perf_counter()
print(f'Model loading took {finish-start:0.4f} seconds.')

with open('captioned_images.md', 'w') as captions_file:

    for image_file_path in glob.glob(image_dir + '/*'):
        start = time.perf_counter()
        image_filename = path.basename(image_file_path)

        captions = ''
        for model, captioner in zip(models, captioners):
            caption = captioner(image_file_path)[0]['generated_text']
            captions += f'{model}: {caption}\n\n'

        captioned_image_file_path = write_caption_to_exif(image_file_path, output_dir, 'This is my file description') 
        print(f'![]({captioned_image_file_path})\n\n{captions}\n', file=captions_file)



        finish = time.perf_counter()
        print(f'Image captioning took {finish-start:0.4f} seconds.')

