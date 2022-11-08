import tensorflow_datasets as tfds

dataset = 'cityscapes'
builder = tfds.builder(dataset)
builder.as_dataset()
#%%
corruptions =  ["gaussian_noise","fog","brightness","contrast"]
for corruption in corruptions:
  for severity in range(1, 6):
    dataset_name=f'cityscapes_corrupted/semantic_segmentation_{}_{}'.format(corruption, severity)
    builder = tfds.builder(dataset_name)
    builder.download_and_prepare()
    builder.as_dataset()
#%%
