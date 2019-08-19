# LaneNet-Lane-Detection 
A Deep Neural Network for real time lane detection mainly based on the paper https://arxiv.org/abs/1802.05591.
This implementation is an extension of [MaybeShewill](https://github.com/MaybeShewill-CV/lanenet-lane-detection),that uses as input data images generated from the simulation program [Speed Dreams](http://www.speed-dreams.org/)

## Installation
This software has been tested on ubuntu 16.04(x64), python3.5, cuda-10.0, cudnn-7.4.1.5 with a RTX-2080 GPU and a TITAN V. 
To install this software you need at least tensorflow 1.10.0 or higher (works for 1.11 and 1.12 as well)
```
pip3 install -r requirements.txt
```

## Test model
In order to test the network download the trained lanenet model weights files from [model_weights](www.google.de).
Move the file in the folder model/speed_dreams

Testing a single image on the trained model can be executed with the following command

```
python tools/test_lanenet.py --is_batch False --batch_size 1 
--weights_path path/to/your/model_weights_file 
--image_path data/tusimple_test_image/0.jpg
```
The results are as follows:

`Test Input Image`

![Test Input](/data/tusimple_test_image/0.jpg)

`Test Lane Mask Image`

![Test Lane_Mask](/data/source_image/lanenet_mask_result.png)

`Test Lane Binary Segmentation Image`

![Test Lane_Binary_Seg](/data/source_image/lanenet_binary_seg.png)

`Test Lane Instance Segmentation Image`

![Test Lane_Instance_Seg](/data/source_image/lanenet_instance_seg.png)

`Test Lane Instance Embedding Image`

![Test Lane_Embedding](/data/source_image/lanenet_embedding.png)

If you want to test the model on a whole dataset you may call
```
python tools/test_lanenet.py --is_batch True --batch_size 2 --save_dir data/tusimple_test_image/ret 
--weights_path path/to/your/model_weights_file 
--image_path data/tusimple_test_image/
```
If you set the save_dir argument the result will be saved in that folder or the result will not be saved but be 
displayed during the inference process holding on 3 seconds per image. I test the model on the whole tusimple lane 
detection dataset and make it a video. You may catch a glimpse of it bellow.
`Tusimple test dataset gif`
![tusimple_batch_test_gif](/data/source_image/lanenet_batch_test.gif)

## Train your own model
#### Data Preparation
Firstly you need to organize your training data refer to the data/training_data_example folder structure. And you need 
to generate a train.txt and a val.txt to record the data used for training the model. 

The training samples are consist of three components. A binary segmentation label file and a instance segmentation label
file and the original image. The binary segmentation use 255 to represent the lane field and 0 for the rest. The 
instance use different pixel value to represent different lane field and 0 for the rest.

All your training image will be scaled into the same scale according to the config file.

#### Train model
In my experiment the training epochs are 200000, batch size is 8, initialized learning rate is 0.0005 and decrease by 
multiply 0.1 every 100000 epochs. About training parameters you can check the global_configuration/config.py for details. 
You can switch --net argument to change the base encoder stage. If you choose --net vgg then the vgg16 will be used as 
the base encoder stage and a pretrained parameters will be loaded and if you choose --net dense then the dense net will 
be used as the base encoder stage instead and no pretrained parameters will be loaded. And you can modified the training 
script to load your own pretrained parameters or you can implement your own base encoder stage. 
You may call the following script to train your own model

```
python tools/train_lanenet.py --net vgg --dataset_dir data/training_data_example/
```
You can also continue the training process from the snapshot by
```
python tools/train_lanenet.py --net vgg --dataset_dir data/training_data_example/ --weights_path path/to/your/last/checkpoint
```

You may monitor the training process using tensorboard tools

During my experiment the `Total loss` drops as follows:  
![Training loss](/data/source_image/total_loss.png)

The `Binary Segmentation loss` drops as follows:  
![Training binary_seg_loss](/data/source_image/binary_seg_loss.png)

The `Instance Segmentation loss` drops as follows:  
![Training instance_seg_loss](/data/source_image/instance_seg_loss.png)
