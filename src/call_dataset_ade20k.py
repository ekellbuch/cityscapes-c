
from tensorflow_datasets.core.registered import _DATASET_REGISTRY
#_DATASET_REGISTRY.pop('ad_e20k_corrupted')
print(_DATASET_REGISTRY.keys())
#%%

import numpy as np
import matplotlib.pyplot as plt

import tensorflow_datasets as tfds
import sys
sys.path.append("..")
from ade20k_corrupted import ADE20kCorrupted
print(ADE20kCorrupted.name)
from ade20k_corrupted import ADE20k
print(ADE20k.name)
# set environment variable:
# https://github.com/tensorflow/datasets/issues/3903
import os
os.environ['TFDS_DATA_DIR'] = os.environ.get('TFDS_DATA_DIR',
                           os.path.join(os.environ.get('HOME'), 'tensorflow_datasets'))

#%%
import tensorflow_datasets as tfds
dataset='ad_e20k'
train_split='train[:32]'
data_dir='gs://ub-ekb/tensorflow_datasets/ad_e20k/tfrecords/v.0.0'
tfds.builder(dataset, data_dir=data_dir, try_gcs=True)
#tfds.load(dataset)
#%%

sys.path.append('../ade20k_corrupted')
#%%

from ade20k_corrupted import ADE20kCorrupted
corruptions = ['gaussian_noise','fog','brightness','contrast']
for corrution in corruptions:
    for noise in range(1, 6):
        dataset_name = 'ad_e20k_corrupted/ade20k_{}_{}'.format(corruptions,noise)
        ds_info = tfds.builder(dataset_name).info
        builder = tfds.builder(dataset_name)
        builder.download_and_prepare()
        print(len(builder.as_dataset('validation').enumerate()))

#%%
def plot(builder):
    #  visualize  dataset
    dataset = builder.as_dataset()
    dataset = list(dataset['validation'])
    batch = dataset[0]

    for batch in dataset[:10]:
        import numpy as nps
        image = batch['image']
        label = batch['annotations']

        label = label.numpy()
        print(np.unique(label))


        instance_segmentation_blue = label[:,:,2]
        instance_mask =  np.unique(instance_segmentation_blue, return_inverse=True)[1]
        desired_shape = list(instance_segmentation_blue.shape) + [1]
        instance_mask = np.reshape(instance_mask, desired_shape)
        instance_mask = instance_mask.astype(np.uint8)
        fig, axarr = plt.subplots(1, 2)
        ax = axarr[0]
        ax.imshow(image)
        ax = axarr[1]
        ax.imshow(instance_mask)
        plt.tight_layout()
        plt.show()
    return
