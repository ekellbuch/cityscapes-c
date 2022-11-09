#!/bin/bash

# After having download the Cityscapes dataset in $MANUAL_DIR
# This code transforms the dataset by corrupting with a specific corruption and severity.

# Read images for semantic_segmentation task
ZIPPED_FOLDER_NAME="leftImg8bit_trainvaltest"
UNZIPPED_FOLDER_NAME="leftImg8bit"

MANUAL_DIR="${HOME}/tensorflow_datasets/downloads/manual"
CITYSCAPES_EXTRACTED_DIR="${HOME}/tensorflow_datasets/downloads/extracted"

# Directory where cityscapes dataset is extracted by tensorflow_datasets.
CITYSCAPES_DIR="${CITYSCAPES_EXTRACTED_DIR}/ZIP.${ZIPPED_FOLDER_NAME}.zip/${UNZIPPED_FOLDER_NAME}/val"

# Possible corruptions:
# gaussian_noise, shot_noise, impulse_noise, defocus_blur,
# glass_blur, motion_blur, zoom_blur, snow, frost, fog,
# brightness, contrast, elastic_transform, pixelate,
# jpeg_compression, speckle_noise, gaussian_blur, spatter,
# saturate

# Process each corruption:
for corruption in "gaussian_noise" "fog" "brightness" "contrast"
do
  for severity in  1 2 3 4 5
do
  # Create a new directory for this corruption and severity which will be in $MANUAL_DIR
  new_file="${ZIPPED_FOLDER_NAME}_${corruption}-${severity}"
  DATADIR="${MANUAL_DIR}/${new_file}"
  # set directory where the corrupted files should be stored temporarily (following the convention of cityscapes)
  CITYSCAPES_C_OUT="${DATADIR}/${UNZIPPED_FOLDER_NAME}/val"
  # Call transform_city.py to corrupt the cityscapes dataset in $CITYSCAPES_DIR and store the output in $CITYSCAPES_C_OUT.
  python transform_city.py $CITYSCAPES_DIR $CITYSCAPES_C_OUT $corruption $severity

  # zip the directory with corrupted images
  pushd ${DATADIR}
  zipped_file="${new_file}.zip"
  zip -r $zipped_file leftImg8bit
  mv $zipped_file ..
  popd
  done
done
