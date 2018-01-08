from PIL import Image
from resizeimage import resizeimage
import os
import argparse
import math

def calc_width(current_image_size, current_file_size, target_file_size):

    if current_file_size <= target_file_size:
        return None
    else:
        ratio = math.sqrt(target_file_size / current_file_size)
        ratio_width = int(current_image_size[0] * ratio)
        return ratio_width

def resize_image(file_path, dest_path, file_size=100):
    try:
        with Image.open(file_path) as im:
            result_width = calc_width(im.size, os.path.getsize(file_path), file_size * 1024)
            if not result_width is None:
                im = resizeimage.resize_width(im, result_width, Image.ANTIALIAS)
            im.save(dest_path, 'JPEG')

    except IOError as err:
        print("source file: " + file_path + " is not image file.")

def main(dir, dest_dir, resize=100):
    list_files = os.listdir(dir)
    for file_name in list_files:
        source_path = os.path.join(dir, file_name)
        index = file_name.find('.')
        if index != -1 or index != 0:
            name = file_name[:index]
            dest_path = os.path.join(dest_dir, name + ".jpg")
            resize_image(source_path, dest_path, file_size = resize)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Image resize')
    parser.add_argument('--resize', help='Resize image size, the size unit is kilobytes')
    parser.add_argument('--sourcedir', help='Resize images directory path')
    parser.add_argument('--resultdir', help='Result images directory path')
    FLAGS, unparsed = parser.parse_known_args()
    resize = FLAGS.resize
    work_dir = FLAGS.sourcedir
    result_dir = FLAGS.resultdir
    if resize is None or work_dir is None or result_dir is None:
        parser.print_help()
    else:
        main(dir = work_dir, dest_dir = result_dir, resize=100)
