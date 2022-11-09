#!/bin/bash


CLOUD_FOLDER_NAME="gs://ub-ekb/tensorflow_datasets/cityscapes_corrupted/tfrecords/v.0.0/cityscapes_corrupted"
MANUAL_DIR="${HOME}/tensorflow_datasets/cityscapes_corrupted"

# export TFDS_DATA_DIR="${HOME}/tensorflow_datasets"
#for corruption in "gaussian_noise" #"shot_noise" "snow" "frost" "brightness" "contrast"
for corruption in "fog" "brightness" "contrast"
do
  for severity in 1 2 3 4 5
  do
  new_file="semantic_segmentation_${corruption}_${severity}"
  cloud_file="${CLOUD_FOLDER_NAME}/${new_file}"
  local_file="${MANUAL_DIR}/${new_file}"
  echo "${local_file}"
  echo  "${cloud_file}"
  gsutil cp -r $local_file $cloud_file
  done
done

# local /Users/ekellbuch/tensorflow_datasets/cityscapes_corrupted/semantic_segmentation_fog_1/1.0.0
# cloud gs://ub-ekb/tensorflow_datasets/cityscapes_corrupted/tfrecords/v.0.0/cityscapes_corrupted/semantic_segmentation_gaussian_noise_4/1.0.0/features.json