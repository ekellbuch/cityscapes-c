import tensorflow_datasets as tfds
import sys
sys.path.append("..")

dataset = 'cityscapes'
builder = tfds.builder(dataset)
builder.as_dataset()
#%%
# set environment variable:
# https://github.com/tensorflow/datasets/issues/3903
import os
os.environ['TFDS_DATA_DIR'] = os.environ.get('TFDS_DATA_DIR',
                           os.path.join(os.environ.get('HOME'), 'tensorflow_datasets'))
#%%
from cityscapes_corrupted.cityscapes_corrupted import CityscapesCorrupted
corruptions =  ["gaussian_noise","fog","brightness","contrast"]
for corruption in corruptions:
  for severity in range(1, 6):
    dataset_name=f'cityscapes_corrupted/semantic_segmentation_{}_{}'.format(corruption, severity)
    builder = tfds.builder(dataset_name)
    builder.download_and_prepare()
    builder.as_dataset()
    print(len(builder.as_dataset('validation').enumerate()))

#%%