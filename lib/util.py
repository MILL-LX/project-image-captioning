import os.path
from pathlib import Path

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
