import tensorflow_datasets as tfds
dataset = 'cityscapes'
ds_info = tfds.builder(dataset).info

dataset_name='cityscapes_corrupted/semantic_segmentation_gaussian_noise_2'
builder = tfds.builder(dataset_name)
builder.download_and_prepare()

#%%
