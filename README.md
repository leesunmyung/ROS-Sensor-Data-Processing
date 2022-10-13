# ROS-Sensor-Data-Processing

## Environment
Ubuntu 18.04, ROS Melodic

## Sensors
* LiDAR: Outser OS1 128CH (1) 
* Camera: GMSL, 1920*1080 (4)
* GPS: RT2000, RTK (1)

## Topic 
* LiDAR: '/point_cloud_transformed', sensor_msgs/PointCloud2
* Camera{num}: '/video_source{num}_resize/image/compressed', sensor_msgs/CompressedImage
* GPS: '/gps_data', Custom msgs

## Output Format
* LiDAR: .pcd
* Camera: .png
* GPS: .csv (Latitude, Longitude, Altitude, Speed, Heading, Angle, Roll, Pitch, etc.)

## Test Vehicle
![image](https://user-images.githubusercontent.com/69629703/195503516-50dbae00-fb95-4b02-8f88-c4c1fb619946.png)

## Reference
* [NIA 49] Denoising data for improving LiDAR point cloud data in adverse weather conditions
* [**Heinzler, R., Piewak, F., Schindler, P., & Stork, W. (2020). CNN-based Lidar Point Cloud De-Noising in Adverse Weather. IEEE Robotics and Automation Letters, 5(2), 2514-2521.**](https://arxiv.org/abs/1912.03874) 
