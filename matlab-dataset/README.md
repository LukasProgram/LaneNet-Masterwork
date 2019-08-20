# MATLAB-Dataset-Creation
Use this repo to generate your own lane dataset. As a result, the record consists of a folder of lane images and a ground truth file. The ground file contains accurate information about the location of lane boundaries.

## Data Source
In this project, the data was generated from the Speed Dreams simulation program. First, five racetracks were selected. For each of these five racetracks, recordings are made in which the entire route is driven. Next, the recordings are converted to a series of consecutive images using the following command:


```
ffmpeg -i input.mp4 -vf fps=5  output/image%d.png
```

After creating a dataset from each racetrack, all the images are merged together. Another option is to perform the labeling separately for each racetrack. This has the advantage that labeling with MATLAB is easier with a sequence of sequential images. In such an approach, for five racetracks, five JSON files are created which later must be merged together. 

In our project, all images are merged together before the labeling and also randomized to reduce the likelihood of successive images side by side. The randomizing and renaming tasks of all files is executed with the scripts located in tools.


## Data Labeling
Labeling requires three programs.
-  [MATLAB](https://de.mathworks.com/products/matlab.html)
-  [Automated Driving Toolbox](https://de.mathworks.com/products/automated-driving.html)
-  [Ground Truth Labeler](https://de.mathworks.com/help/driving/ug/get-started-with-the-ground-truth-labeler.html)

After all three programs are integrated, the following steps must be executed to generate a JSON file with the same structure as in [TuSimple](https://github.com/TuSimple/tusimple-benchmark/tree/master/doc/lane_detection).

1. Run MATLAB and the Automated Driving Toolbox
2. Prepare the Lane Detection [Automation Class](https://de.mathworks.com/help/driving/examples/automate-ground-truth-labeling-of-lane-boundaries.html)
3. Load both files (cameraParameters.m , IntersectionFinder.m)
4. Run the script cameraPerameters.m to load all parameters into the MATLAB workspace
5  Run the Ground Truth Labeler application
6. Load an image sequence (the folder with the dataset)
7. Create a [ROI label definition](pictures/roi.png) 
      - Name: LaneBoundaries
      - Shape: Line
      
8. Select the algorithm created in step 2 and run "Automate"
9. Open [Settings](pictures/settings.png) and adjust the parameter values, add the sensor, loaded in step 3.
10.Run the algorithm
11. Adjust lane boundaries if they are wrong detected
12. Export the labeled data into the workspace  (gTruth file)
13. Run the IntersectionFinder.m to generate a JSON file

If problems occur, visit the [GTL]((https://de.mathworks.com/help/driving/examples/automate-ground-truth-labeling-of-lane-boundaries.html)) page, which describes some steps in more detail.

## Refinement
The ground truth file in [TuSimple](https://github.com/TuSimple/tusimple-benchmark/tree/master/doc/lane_detection) has an atypical JSON form which also has to be adapted for the generated JSON file. Therefore, the *generate_label_data_for_training.py* script must be executed, which takes as input the intersection data json from the labeling and outputs a label_data.json. Both files must be located in the same folder.

```
python3 generate_label_data_for_training.py
```
Finally, the file must be examined for errors and the paths must be adjusted (windows and linux path differ).

## Future Work
The camera parameters were determined using a try-and-error method because no information about the sensor components was available in Speed Dreams. Therefore, it may be that other values that have not yet been determined give better results than those in the CameraParameters.m.

