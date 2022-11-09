# coding=utf-8
# Copyright 2022 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ADE20k-Corrupted Datasets."""

import os
import re

import tensorflow as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """\
@inproceedings{zhou2017scene,
title={Scene Parsing through ADE20K Dataset},
author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},
booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
year={2017}
}

@inproceedings{
  hendrycks2018benchmarking,
  title={Benchmarking Neural Network Robustness to Common Corruptions and Perturbations},
  author={Dan Hendrycks and Thomas Dietterich},
  booktitle={International Conference on Learning Representations},
  year={2019},
  url={https://openreview.net/forum?id=HJz6tiCqYm},
}

@article{michaelis2019dragon,
  title={Benchmarking Robustness in Object Detection: 
    Autonomous Driving when Winter is Coming},
  author={Michaelis, Claudio and Mitzkus, Benjamin and 
    Geirhos, Robert and Rusak, Evgenia and 
    Bringmann, Oliver and Ecker, Alexander S. and 
    Bethge, Matthias and Brendel, Wieland},
  journal={arXiv preprint arXiv:1907.07484},
  year={2019}
}


"""

_DESCRIPTION = """\
ADE20K Corrupted
"""

_DOWNLOAD_URL = "gs://ub-ekb/ade20k_corrupted/raw_data/v.0.0"

_TRAIN_URL = {
    "images":
        "http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip",
    "annotations":
        "http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip"
}

_CORRUPTIONS = [
    'gaussian_noise',
    'brightness',
    'contrast',
    'fog',
]

class ADE20kCorruptedConfig(tfds.core.BuilderConfig):
  """BuilderConfig for ADE20k corrupted.

    Args:
      corruption_type (str): name of corruption.
      severity (int): level of corruption.
      right_images (bool): Enables right images for stereo image tasks.
      segmentation_labels (bool): Enables image segmentation labels.
      disparity_maps (bool): Enables disparity maps.
      train_extra_split (bool): Enables train_extra split. This automatically
        enables coarse grain segmentations, if segmentation labels are used.
  """

  def __init__(self,
               *,
               corruption_type,
               severity,
               **kwargs):
    super(ADE20kCorruptedConfig, self).__init__(version='1.0.0', **kwargs)

    self.corruption = corruption_type
    self.severity = severity

    # Setup required zips and their root dir names
    self.zip_root = {}
    self.zip_root['images'] = ('ADEChallengeData2016_{}-{}'.format(corruption_type, severity),)
    self.zip_root['annotations'] = ('ADEChallengeData2016_{}-{}'.format(corruption_type, severity),)


def _make_builder_configs():
  """Construct a list of BuilderConfigs.

  Construct a list of 95 Cifar10CorruptedConfig objects, corresponding to
  the 15 corruption types + 4 extra corruptions and 5 severities.

  Returns:
    A list of ADE20kCorruptedConfig objects.
  """
  config_list = []
  for corruption in _CORRUPTIONS:
    for severity in range(1, 6):
      config_list.append(
          ADE20kCorruptedConfig(
              corruption_type=corruption,
              severity=severity,
              name="ade20k_{}_{}".format(corruption, str(severity)),
              description='ADE20k semantic segmentation dataset. Corruption method: ' + corruption +
              ', severity level: ' + str(severity),
          ))
  return config_list


class ADE20kCorrupted(tfds.core.GeneratorBasedBuilder):
  """Base class for ADE20kCorrupted datasets."""
  #SKIP_REGISTERING = True
  MANUAL_DOWNLOAD_INSTRUCTIONS = """\
  Download files from _DOWNLOAD_URL and place them in the manual directory
  """

  BUILDER_CONFIGS = _make_builder_configs()
  RELEASE_NOTES = {
      '0.0.0': 'ADE20k corruptions',
  }
  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "image": tfds.features.Image(encoding_format="jpeg"),
            "annotations": tfds.features.Image(encoding_format="png")
        }),
        supervised_keys=("image", "annotations"),
        homepage="http://sceneparsing.csail.mit.edu/",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    #dl_paths = dl_manager.download_and_extract({
    #    "images": _TRAIN_URL["images"],
    #    "annotations": _TRAIN_URL["annotations"],
    #})
    dl_paths = {}
    dl_paths['images'] = os.path.join(dl_manager._extract_dir, self.builder_config.zip_root['images'][0])
    dl_paths['annotations'] = os.path.join(dl_manager._extract_dir, self.builder_config.zip_root['annotations'][0])

    #for (split, zip_file) in self.builder_config.zip_root.items():
    #  dl_paths[split] = os.path.join(dl_manager._extracted_dir, zip_file)

    if any(not tf.io.gfile.exists(z) for z in dl_paths.values()):
      msg = 'You must download the dataset files manually and place them in: '
      msg += ', '.join(dl_paths.values())
      raise AssertionError(msg)

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={
                "images_dir_path":
                    os.path.join(dl_paths["images"], "images/validation"),
                "annotations_dir_path":
                    os.path.join(dl_paths["annotations"],
                                 "annotations/validation")
            },
        ),
    ]

  def _generate_examples(self, images_dir_path, annotations_dir_path):
      for image_file in tf.io.gfile.listdir(images_dir_path):
          # get the filename
          image_id = os.path.split(image_file)[1].split(".")[0]
          yield image_id, {
              "image":
                  os.path.join(images_dir_path, "{}.jpg".format(image_id)),
              "annotations":
                  os.path.join(annotations_dir_path, "{}.png".format(image_id))
          }

