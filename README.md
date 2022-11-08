## Cityscapes and Cityscapes-C

This repository contains instructions to create the corrupted Cityscapes-Corrupted dataset with tensorflow.

### Steps:

#### 1. Download Cityscapes 

To download the Cityscapes dataset:
1. Create a login to the website https://www.cityscapes-dataset.com. <br>
2. The cityscapes dataset supports multiple tasks. For the semantic segmentation task, download the files: [gtFine_trainvaltest.zip](https://www.cityscapes-dataset.com/file-handling/?packageID=1) and [leftImg8bit_trainvaltest.zip](https://www.cityscapes-dataset.com/file-handling/?packageID=3) which contain the segmentation labels and the raw images respectively. <br>
3. Move the files ([gtFine_trainvaltest.zip](https://www.cityscapes-dataset.com/file-handling/?packageID=1) and [leftImg8bit_trainvaltest.zip](https://www.cityscapes-dataset.com/file-handling/?packageID=3)) to the manual download directory in tensorflow_datasets. For example, if you downloaded the files in the ``~/Downloads`` directory:
```
cd ~/Downloads
mv gtFine_trainvaltest.zip ~/tensorflow_datasets/downloads/manual/
mv leftImg8bit_trainvaltest.zip ~/tensorflow_datasets/downloads/manual/

```

#### 2. Create TF Records for Cityscapes
Tensorflow records is the format tensorflow uses to read datasets.
To create tf records for the cityscapes dataset using the files you just downloaded run: <br> 
```
import tensorflow_datasets as tfds
dataset = 'cityscapes'
builder = tfds.builder(dataset)
builder.download_and_prepare()
```
This step  will use the files in the manual directory and create the tf records using [cityscapes.py](https://github.com/tensorflow/datasets/blob/master/tensorflow_datasets/image/cityscapes.py) in the directory ``~/tensorflow_datasets``.
To check if the tf records were created, run:
```
builder.as_dataset()
```
which should return a dictionary with the keys ``train``, ``test`` and ``validation``.

#### 3. Corrupt  Cityscapes 

To corrupt the Cityscapes dataset install [imagecorruptions](https://github.com/bethgelab/imagecorruptions) and run: <br> 
```
./src/transform_city.sh 
```

This code applies multiple corruptions at different severity levels to the images in cityscapes and stores them in a new directory. 
The images corrupted with gaussian noise with severity 1 will be stored in:
``~/tensorflow_datasets/downloads/manual/leftImg8bit_trainvaltest_gaussian_noise-1``.

#### 4. Create TF Records for Cityscapes-Corrupted
To build tf records for the corrupted dataset using the corrupted images run [src/call_dataset.py](https://github.com/ekellbuch/cityscapes-c/blob/main/src/call_dataset.py).
For example, to build the tf records for the gaussian noise corruption with severity 1 run: <br>
```
import tensorflow_datasets as tfds
dataset ='cityscapes_corrupted/semantic_segmentation_gaussian_noise_1'
builder = tfds.builder(dataset)
builder.download_and_prepare()
```
This step uses the dataset builder in [cityscapes_corrupted/cityscapes_corrupted.py](https://github.com/ekellbuch/cityscapes-c/blob/main/cityscapes_corrupted/cityscapes_corrupted.py), which  was constructed following the [TF Writing Custom Dataset Guide](https://www.tensorflow.org/datasets/add_dataset), to create tf records in the directory ``~/tensorflow_datasets``.

To check if the tf records were created, run:
```
builder.as_dataset()
```
which should return a dictionary with the keys ``validation``.


### References
```
@inproceedings{Cordts2016Cityscapes,
  title={The Cityscapes Dataset for Semantic Urban Scene Understanding},
  author={Cordts, Marius and Omran, Mohamed and Ramos, Sebastian and Rehfeld, Timo and Enzweiler, Markus and Benenson, Rodrigo and Franke, Uwe and Roth, Stefan and Schiele, Bernt},
  booktitle={Proc. of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2016}
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
```

