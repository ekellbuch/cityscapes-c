#!/bin/bash

# Given downloaded Cityscapes dataset in $MANUAL_DIR
# Transform dataset by corrupting with a specific corruption and severity.
# Finally upload this to a gcp bucket $CLOUD_FOLDER_NAME

CLOUD_FOLDER_NAME="gs://ub-ekb/ade20k_c/raw_data/v.0.0/"

# Read images for semantic_segmentation task:
# we do not need to corrupt the labels, only the images
ZIPPED_FOLDER_NAME="streethazard"
UNZIPPED_FOLDER_NAME="images"

MANUAL_DIR="${HOME}/tensorflow_datasets/downloads/manual"
EXTRACTED_DIR="${HOME}/tensorflow_datasets/downloads/extracted"

# Directory where dataset is extracted by tensorflow_datasets.
ADE20K_DIR="${EXTRACTED_DIR}/${ZIPPED_FOLDER_NAME}"


OUTPUT_NAME="ADEChallengeData2016"
# Possible corruptions:
# gaussian_noise, shot_noise, impulse_noise, defocus_blur,
# glass_blur, motion_blur, zoom_blur, snow, frost, fog,
# brightness, contrast, elastic_transform, pixelate,
# jpeg_compression, speckle_noise, gaussian_blur, spatter,
# saturate

# Corruptions processed:
# gaussian_noise
#for corruption in "shot_noise" "snow" "frost" "brightness" "contrast"


for corruption in "brightness"
do
  for severity in 1 2 3 4 5
  do
  # duplicate the data directory
  cp -r $ADE20K_DIR $ADE20K_DIR"_"$corruption"-"$severity
  # remove training directories
  rm -rf $ADE20K_DIR"_"$corruption"-"$severity"/train/images/training"
  rm -rf $ADE20K_DIR"_"$corruption"-"$severity"/train/annotations/training"

  # remove validation and test data which will be replaced
  rm -rf $ADE20K_DIR"_"$corruption"-"$severity"/train/images/validation/t4"
  rm -rf $ADE20K_DIR"_"$corruption"-"$severity"/test/images/test/t5-6"

  # for the validation data, update the images
  DATA_IN="${ADE20K_DIR}/train/images/validation/t4"
  DATA_OUT="${ADE20K_DIR}_${corruption}-${severity}/train/images/validation"
  # Call transform_city.py to corrupt the dataset in DATA_IN and store the output in DATA_OUT.
  python transform_city.py $DATA_IN $DATA_OUT $corruption $severity

  # for the test data, update the images
  DATA_IN="${ADE20K_DIR}/test/images/test/t5-6"
  DATA_OUT="${ADE20K_DIR}_${corruption}-${severity}/test/images/test"
  # Call transform_city.py to corrupt the dataset in DATA_IN and store the output in DATA_OUT.
  python transform_city.py $DATA_IN $DATA_OUT $corruption $severity
  done
done

# Copy the dataset in bucket
#LABEL_DIR="${HOME}/tensorflow_datasets/downloads/manual/gtFine_trainvaltest.zip"
#gsutil cp -r $LABEL_DIR $CLOUD_FOLDER_NAME
