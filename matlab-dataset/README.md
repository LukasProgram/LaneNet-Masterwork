# MATLAB-Dataset-Creation
Use this repo to generate your own lane dataset. As a result, the record consists of a folder of lane images and a ground truth file. The ground file contains accurate information about the location of lane boundaries.

## Data Source
In this project, the data was generated from the Speed Dreams simulation program. First, five racetracks were selected. For each of these five racetracks, recordings are made in which the entire route is driven. Next, the recording is converted to a series of consecutive images using the following command:


```
ffmpeg -i input.mp4 -vf fps=5  output/image%d.png
```

After creating a dataset from each racetrack, all the images are merged together. Another option is to perform the labeling separately for each racetrack. This has the advantage that labeling with MATLAB is easier with a sequence of sequential images. In such an approach, for 5 racetracks, 5 JSON files are created which later must be merged together. 

In our project, all images are merged together before the labeling and also randomized to reduce the likelihood of successive images side by side. The randomizing and renaming tasks of all files is executed with the scripts located in tools.


## Data Labeling

  
