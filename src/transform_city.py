"""
Apply corruptions to cityscapes images.
"""
from imagecorruptions import corrupt, get_corruption_names
import fire
import numpy as np
from PIL import Image
import os
from pathlib import Path
IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm']
import shutil
from tqdm import tqdm
import multiprocessing
from functools import partial

def is_image_file(filename):
  """Checks if a file is an image.
  Args:
    filename (string): path to a file
  Returns:
    bool: True if the filename ends with a known image extension
  """
  filename_lower = filename.lower()
  return any(filename_lower.endswith(ext) for ext in IMG_EXTENSIONS)


def pil_loader(path):
  # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
  with open(path, 'rb') as f:
    img = Image.open(f)
    # Following https://github.com/bethgelab/imagecorruptions/blob/master/test_demo.py
    #return img.convert('RGB')
    return np.asarray(img)


def main(in_dir, out_dir, corruption, severity):
  in_dir = os.path.expanduser(in_dir)
  for (dirpath, dirnames, filenames) in os.walk(in_dir):
    transform_files = partial (transform_file, dirpath, out_dir, corruption, severity)
    pool = multiprocessing.Pool(max(1, multiprocessing.cpu_count() - 1))
    zip(*pool.map(transform_files, filenames))

def transform_file(dirpath, out_dir, corruption, severity, filename):
  image_file = os.path.join(dirpath, filename)
  if is_image_file(image_file):
    save_path = os.path.join(out_dir, *image_file.rsplit('/', 2)[1:])
    if not Path(save_path).parent.exists():
      try:
        os.makedirs(str(Path(save_path).parent))
    image = pil_loader(image_file)
    corrupted = corrupt(image, corruption_name=corruption, severity=severity)
    Image.fromarray(np.uint8(corrupted)).save(save_path, quality=85, optimize=True)
  else:
    print('Could not corrupt {}'.format(image_file))
    #shutil(image_file, save_path)
  return

if __name__ == "__main__":
    fire.Fire(main)