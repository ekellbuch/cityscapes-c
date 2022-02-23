## Cityscapes and Cityscapes-C

This repository construct cityscapes-c dataset compatible with tensorflow_datasets for semantic segmentation.

### Steps:

#### Download Cityscapes 

Create a login and download cityscapes from https://www.cityscapes-dataset.com/
For a semantic segmentation task download: gtFine_trainvaltest.zip and leftImg8bit_trainvaltest.zip
The files should be placed in the tensorflow dataset download directory.
This directory is by default set as ```$HOME$/tensorflow_datasets/downloads```

#### Build/Process Cityscapes 

To build the cityscapes dataset and create tf records using the tensorflow_datasets default builder run:
```
import tensorflow_datasets as tfds
dataset = 'cityscapes'
builder = tfds.builder(dataset)
builder.download_and_prepare()
```
#### Corrupt  Cityscapes 

To corrupts cityscapes dataset (for the semantic_segmentation task) run <br> 
```
./src/transform_city.sh 
```

#### Build/Process  Cityscapes-Corrupted
To build the cityscapes-corrupted dataset and create tf records run <br>
```
import tensorflow_datasets as tfds
dataset ='cityscapes_corrupted/semantic_segmentation_gaussian_noise_2'
builder = tfds.builder(dataset)
builder.download_and_prepare()
```
This command uses the custom dataset builder provided, and located in cityscapes_corrupted/cityscapes_corrupted.py
The builder was constructed following the [TF Writing Custom Dataset Guide](https://www.tensorflow.org/datasets/add_dataset).

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

