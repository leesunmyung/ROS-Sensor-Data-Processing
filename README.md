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
