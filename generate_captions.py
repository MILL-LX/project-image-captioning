import argparse
import os
import shutil

from PIL import Image
from PIL.ExifTags import TAGS
from transformers import pipeline

from lib.util import write_caption_to_exif, timer, CaptionsFileWriter

from pillow_heif import register_heif_opener
register_heif_opener()


@timer
def load_models(models):
    return [pipeline('image-to-text', model=model, max_new_tokens=64, device="cpu") for model in models]

@timer
def make_captions_for_image(models, captioners, image_file_path):
    captions = {}

    with Image.open(image_file_path) as image_to_caption:
        for model, captioner in zip(models, captioners):
            caption = captioner(image_to_caption)[0]['generated_text']
            captions[model] = caption

    return captions

@timer
def process_image(models, captioners, image_file_path, input_dir, output_dir, captions_file_writer):
    captions = make_captions_for_image(models, captioners, image_file_path)
    captioned_image_file_path = write_caption_to_exif(image_file_path, input_dir, output_dir, captions) 
    captions_file_writer.write_captions(captioned_image_file_path, captions)

@timer
def process_images_recursively(input_dir, output_dir, models, captions_writer):
    captioners = load_models(models)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            image_file_path = os.path.join(root, file)
            process_image(models, captioners, image_file_path, input_dir, output_dir, captions_writer)

@timer
def clear_output(output_dir, captions_file):
    try:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        if os.path.exists(captions_file):
            os.remove(captions_file)

        print(f"Output directory '{output_dir}' cleared successfully, and '{captions_file}' deleted.")
    except Exception as e:
        print(f"Error: {e}")

@timer
def parse_arguments():
    parser = argparse.ArgumentParser(description='Image captioning script with optional output clearing.')
    parser.add_argument('--clear-output', action='store_true', help='Clear the output directory and delete the captions file.')
    return parser.parse_args()

@timer
def main():
    args = parse_arguments()

    input_dir = 'data/input'
    output_dir = 'data/output'
    captions_file = 'captioned_images.md'

    models = ['Salesforce/blip-image-captioning-base', 
              'Salesforce/blip-image-captioning-large', 
              'nlpconnect/vit-gpt2-image-captioning']

    if args.clear_output:
        clear_output(output_dir, captions_file)

    captions_writer = CaptionsFileWriter(captions_file)
    process_images_recursively(input_dir, output_dir, models, captions_writer)

if __name__ == "__main__":
    main()
