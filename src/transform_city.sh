#!/bin/bash

# Having downloaded cityscapes dataset corrupt the images and upload them to gcp bucket

CLOUD_FOLDER_NAME="gs://ub-ekb/cityscapes_c/raw_data/v.0.0/"

# Read images for semantic_segmentation task
ZIPPED_FOLDER_NAME="leftImg8bit_trainvaltest"
UNZIPPED_FOLDER_NAME="leftImg8bit"

MANUAL_DIR="${HOME}/tensorflow_datasets/downloads/manual"
CITYSCAPES_EXTRACTED_DIR="${HOME}/tensorflow_datasets/downloads/extracted"

# Directory where cityscapes dataset is extracted by tensorflow_datasets.
CITYSCAPES_DIR="${CITYSCAPES_EXTRACTED_DIR}/ZIP.${ZIPPED_FOLDER_NAME}.zip/${UNZIPPED_FOLDER_NAME}/val"

for corruption in "gaussian_noise" #"shot_noise" "snow" "frost" "brightness" "contrast"
do
  for severity in 1 2 3 4 5
  do
  CITYSCAPES_C_OUT="${MANUAL_DIR}/${ZIPPED_FOLDER_NAME}_${corruption}-${severity}/${UNZIPPED_FOLDER_NAME}/val"
  python transform_city.py $CITYSCAPES_DIR $CITYSCAPES_C_OUT $corruption $severity
  DATADIR="${MANUAL_DIR}/${ZIPPED_FOLDER_NAME}_${corruption}-${severity}"
  pushd $DATADIR
  new_file="${ZIPPED_FOLDER_NAME}_${corruption}-${severity}"
  zipped_file="${ZIPPED_FOLDER_NAME}_${corruption}-${severity}.zip"
  zip -r $zipped_file $UNZIPPED_FOLDER_NAME
  mv $zipped_file ../
  # rm -rf $new_file
  #gsutil cp -r $zipped_file $CLOUD_FOLDER_NAME
  popd
  done
done

# Copy the labels in bucket
#LABEL_DIR="${HOME}/tensorflow_datasets/downloads/manual/gtFine_trainvaltest.zip"
#gsutil cp -r $LABEL_DIR $CLOUD_FOLDER_NAME
