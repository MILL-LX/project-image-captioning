import json
import os
import os.path
from pathlib import Path
import time

import piexif
import piexif.helper
from PIL import Image


def outfile_name_from_infile_path(infile_path, tag_string):
    infilename = os.path.basename(infile_path)
    filename, extension = os.path.splitext(infilename)

    # we write heic files as jpg since we expect to display them in a web page
    if extension == '.heic':
         extension += '.jpg' 

    output_filename = filename + f'-{tag_string}' + extension
    return output_filename

def subpath_in_dir(dir, path):
    directory = os.path.normpath(dir)
    path = os.path.normpath(path)

    if path.startswith(directory):
        return path[len(directory) + 1:]
    else:
        return path

def write_caption_to_exif(input_image_path, input_dir, output_dir, caption):
    try:
        infile_subpath = subpath_in_dir(input_dir, input_image_path)
        infile_subdir = os.path.dirname(infile_subpath)
        
        full_output_dir = os.path.join(output_dir, infile_subdir)
        if not os.path.exists(full_output_dir):
            os.makedirs(full_output_dir)

        outfile_name = outfile_name_from_infile_path(input_image_path, 'CAPTIONED')
        full_output_path = os.path.join(full_output_dir, outfile_name)

        # Grab the existing EXIF data, if any
        image = Image.open(input_image_path)
        if image.info.get('exif'):
            exif_data = piexif.load(image.info['exif'])
        else:
            exif_data = {'0th': {}, 'Exif': {}, '1st': {},'thumbnail': None, 'GPS': {}}

        # format teh captions as json
        json_caption = json.dumps(caption)

        # Add the user comment
        exif_data['Exif'][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(json_caption)


        # write the output file with the new exif data
        exif_dat = piexif.dump(exif_data)
        image.save(full_output_path,  exif=exif_dat)

        print(f'wrote {full_output_path}')

        return full_output_path

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

class CaptionsFileWriter:
    def __init__(self, captions_file_path):
        self.captions_file_path = captions_file_path

    def format_captions(self, captions):
        formatted_captions = ''
        for model, caption in captions.items():
            formatted_captions += f'{model}: {caption}\n\n'

        return formatted_captions

    def write_captions(self, captioned_image_path, captions):
        with open(self.captions_file_path, 'a') as captions_file:
            print(f'![{captioned_image_path}]({captioned_image_path})\n\n{self.format_captions(captions)}', file=captions_file)