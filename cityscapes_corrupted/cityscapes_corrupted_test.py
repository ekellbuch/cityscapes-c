"""cityscapes_corrupted dataset."""

import tensorflow_datasets as tfds
#from . import cityscapes_corrupted
import cityscapes_corrupted

class CityscapesCorruptedTest(tfds.testing.DatasetBuilderTestCase):
  """Tests for cityscapes_corrupted dataset."""

  BUILDER_CONFIG_NAMES_TO_TEST = [
      "semantic_segmentation_gaussian_noise_1",
  ]

  SKIP_CHECKSUMS = True
  DATASET_CLASS = cityscapes_corrupted.CityscapesCorrupted
  SPLITS = {
      'validation': 1,  # Number of fake test example
  }

  # If you are calling `download/download_and_extract` with a dict, like:
  #   dl_manager.download({'some_key': 'http://a.org/out.txt', ...})
  # then the tests needs to provide the fake output paths relative to the
  # fake data directory
  # DL_EXTRACT_RESULT = {'some_key': 'output_file1.txt', ...}


if __name__ == '__main__':
  tfds.testing.test_main()
