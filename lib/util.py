import os.path
from pathlib import Path
import time

import piexif
import piexif.helper
from PIL import Image


def outfile_name_from_infile_path(infile_path, tag_string):
    infilename = os.path.basename(infile_path)
    filename, extension = os.path.splitext(infilename)
    output_filename = filename + f'-{tag_string}' + extension
    return output_filename


def write_caption_to_exif(input_image_path, output_dir, caption):
    try:
        # Generate the output file path
        outfile_name = outfile_name_from_infile_path(input_image_path, 'CAPTIONED')
        outfile_path = f'{output_dir}/{outfile_name}'

        # Grab the existing EXIF data, if any
        image = Image.open(input_image_path)
        if image.info.get('exif'):
            exif_data = piexif.load(image.info['exif'])
        else:
            exif_data = {'0th': {}, 'Exif': {}, '1st': {},'thumbnail': None, 'GPS': {}}

        # Add the user comment
        exif_data['Exif'][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(caption)


        # write the output file with the new exif data
        exif_dat = piexif.dump(exif_data)
        image.save(outfile_path,  exif=exif_dat)

        print(f'wrote {outfile_path}')

        return outfile_path

    except Exception as e:
        print(f'An error occurred writing caption to EXIF data: {e}')

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'{func.__name__} took {end_time - start_time:0.4f} seconds.')
        return result
    return wrapper

class CaptionsWriter:
    def __init__(self, captions_file_path):
        self.captions_file_path = captions_file_path

    def write_captions(self, captioned_image_path, captions):
        with open(self.captions_file_path, 'a') as captions_file:
            print(f'![]({captioned_image_path})\n\n{captions}\n', file=captions_file)