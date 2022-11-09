"""ade20k_corrupted dataset.
To run test

"""

import tensorflow_datasets as tfds
import ade20k_corrupted

class ADE20kCorruptedTest(tfds.testing.DatasetBuilderTestCase):
  """Tests for ade20k_corrupted dataset."""

  BUILDER_CONFIG_NAMES_TO_TEST = [
      "ade20k_gaussian_noise_1",
  ]

  SKIP_CHECKSUMS = True
  DATASET_CLASS = ade20k_corrupted.ADE20kCorrupted
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
