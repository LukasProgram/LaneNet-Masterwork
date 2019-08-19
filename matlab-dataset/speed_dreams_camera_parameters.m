focalLength = [600 650];
principalPoint = [645 375];
imageSize = [720 1280];

camIntrinsics = cameraIntrinsics(focalLength,principalPoint,imageSize);

height = 1.3;
pitch = 1.9;

sensor = monoCamera(camIntrinsics,height,'Pitch',pitch);

