import glob
from os import path
from PIL import Image
from PIL.ExifTags import TAGS
from transformers import pipeline
from lib.util import write_caption_to_exif, timer, CaptionsWriter


@timer
def load_models(models):
    return [pipeline('image-to-text', model=model, max_new_tokens=64) for model in models]


@timer
def make_captions_for_image(models, captioners, image_file_path):
    image_filename = path.basename(image_file_path)

    captions = ''

    for model, captioner in zip(models, captioners):
        caption = captioner(image_file_path)[0]['generated_text']
        captions += f'{model}: {caption}\n\n'

    return captions

@timer
def process_images(image_dir, output_dir, models, captions_writer):
    captioners = load_models(models)

    for image_file_path in glob.glob(image_dir + '/*'):
        captions = make_captions_for_image(models, captioners, image_file_path)

        captioned_image_file_path = write_caption_to_exif(image_file_path, output_dir, captions) 
        captions_writer.write_captions(captioned_image_file_path, captions)

@timer
def main():
    image_dir = 'data/input'
    output_dir = 'data/output'
    models = ['Salesforce/blip-image-captioning-base', 
              'Salesforce/blip-image-captioning-large', 
              'nlpconnect/vit-gpt2-image-captioning']

    captions_writer = CaptionsWriter('captioned_images.md')
    process_images(image_dir, output_dir, models, captions_writer)

if __name__ == "__main__":
    main()
