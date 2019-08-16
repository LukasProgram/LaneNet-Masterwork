
labelData = gTruth.LabelData;
laneBoundaries = labelData.LaneBoundaries;
[roadPicturesLength,z] = size(laneBoundaries);

roadPictureIndex = 1;
laneIndex = 1;  %need to be 1 when next picture is taken
lanePointIndex = 1; %need to be 1 when next lane is taken

intersectionList = []; %list with the intersection data of all lanes
oneSubLaneIntersectionList = []; %list with the intersection data of one sublane
oneLaneIntersectionList = []; %list with the intersection data of one lane
mergedSublanesIntersectionList = []; %merged intersection list of all sublanes
onePictureLaneIntersectionList = [[]]; %list with the intersection data of one picture
finalJsonLaneDataStructure = ''; %final structure expored in a json file

h_sampleData = [];
h_sampleIndex = 10;
while h_sampleIndex < 720
    h_sampleData = [h_sampleData, h_sampleIndex];
    h_sampleIndex = h_sampleIndex + 10;
end


while roadPictureIndex <= roadPicturesLength % loop over all pictures
    picturePath = gTruth.DataSource.Source(roadPictureIndex:roadPictureIndex);
    picturePath = strjoin(picturePath);
    roadPicture = laneBoundaries{roadPictureIndex, 1}; 
    [roadPictureLanesAmount,z] = size(roadPicture);

       while laneIndex <= roadPictureLanesAmount % loop over all lanes in a picture
           
            oneLaneFromThePicture = roadPicture{laneIndex, 1};
            [lanePoints, z] = size(oneLaneFromThePicture);
        
            while lanePointIndex <= lanePoints -1   % loop over all point in a lane (-1 because the last point is accessed in the loop as the pointB)
                pointA = oneLaneFromThePicture(lanePointIndex,1:2); % get the row table data of the current point
                pointAx = pointA(1);
                pointAy = pointA(2);
                pointB = oneLaneFromThePicture(lanePointIndex+1,1:2);
                pointBx = pointB(1);
                pointBy = pointB(2);
                lineAB = [[pointAx,pointBx];[pointAy,pointBy]]; 
                
                % first compare line
                pointCx = 0;
                pointCy = 10;
                pointDx = 1280;
                pointDy = 10;
                
                thresholdStepValue = 10;
                maxThreshold = 720;
                
                
                while pointCy < maxThreshold % check pointCy or pointDy, both variables has the same value
                    lineCD = [[pointCx,pointDx];[pointCy,pointDy]];
                    intersectionPoint = InterX(lineAB,lineCD);
            
                    if isempty(intersectionPoint) ~= 1
                    intersectionPointX = intersectionPoint(1:1); % get the first and the second value of the intersection
                    %intersectionPointX = round(intersectionPointX);  % when rounded values are required then uncomment this line
                    intersectionPointY = intersectionPoint(2:2);
                    intersectionPointY = round(intersectionPointY); % value is rounded to avoid numbers with decimal places 
                    else
                    intersectionPointX = -2;
                    intersectionPointY = pointCy;  
                    end
                    
                    % The intersectionList contains all information about
                    % the lanes data. Since the list size ist not known at
                    % the beginning, it is increasing every loop and
                    % calculation is very slow. Uncomment only when really
                    % required.
                    %intersectionList = [intersectionList; [roadPictureIndex laneIndex lanePointIndex intersectionPointX intersectionPointY]]; %table with all lane information of a picture                 
                    oneLaneIntersectionList = [oneLaneIntersectionList; [ intersectionPointX, intersectionPointY]]; %intersection list of one lane                
                    
                    pointCy = pointCy + thresholdStepValue;
                    pointDy = pointDy + thresholdStepValue;
                end
            
                lanePointIndex = lanePointIndex + 1;
                
            end

            yStepValue = 10;
            while yStepValue < 720  % merge all intersection points from the sublanes to one lane
                yStepValuesFromOneLane = oneLaneIntersectionList(any(oneLaneIntersectionList==yStepValue,2),:);
                [yStepValues, z] = size(yStepValuesFromOneLane); % determine the length of the table becaue when lenght is 1 there is no max

                if yStepValues==1
                    maxValue = yStepValuesFromOneLane(1);
                else
                    [maxValue, maxPosition] = max(yStepValuesFromOneLane);
                end
                
                mergedSublanesIntersectionList = [mergedSublanesIntersectionList; maxValue];
                yStepValue = yStepValue + 10;
            end
            
            mergedSublanesIntersectionRow = {mergedSublanesIntersectionList(:,1).'}; % get the column with the x intersection data and convert it to row representation

            lanePointIndex = 1;
            laneIndex = laneIndex + 1;
            onePictureLaneIntersectionList = [onePictureLaneIntersectionList mergedSublanesIntersectionRow];
            oneLaneIntersectionList = []; % reset the list to get all lane data from only one lane 
            mergedSublanesIntersectionList = [];
       end 
       
       lanesDataStructure = struct("lanes", [], "h_sample", h_sampleData, "raw_file", picturePath); %json lanes data structure for one picture
       lanesDataStructure.lanes = onePictureLaneIntersectionList; % append the lanes data
       
       finalJsonLaneDataStructure = [finalJsonLaneDataStructure, lanesDataStructure]; %structs of each picture are merged together
       
       laneIndex = 1;
       fprintf('roadPictureIndex == %6.2i.\n',roadPictureIndex); 
       roadPictureIndex = roadPictureIndex +1;
       onePictureLaneIntersectionList = []; % reset the list to get alway only all lane data from one picture
end

savejson('',finalJsonLaneDataStructure,'jsonIntersecionData'); % data exported as json file
