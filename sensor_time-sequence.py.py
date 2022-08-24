#!/usr/bin/python
import rospy
import sys
import os
import cv2
import time
#import pcl
import numpy as np
# from cv_bridge import CvBridge
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, Image, CompressedImage
from inertial_labs_msgs.msg import gps_49
# make LiDAR DATA binary 
# import bitstring
import struct
import shutil

# Topic 
LiDAR_topic = '/point_cloud_transformed' # '/os_cloud_node/points'
Camera0_topic = '/video_source0_resize/image/compressed'
Camera1_topic = '/video_source1_resize/image/compressed'
Camera2_topic = '/video_source2_resize/image/compressed'
Camera3_topic = '/video_source3_resize/image/compressed'
GPS_topic = '/gps_data'

camera0_list = []
camera1_list = []
camera2_list = []
camera3_list = []

gps_file_name = ''
gps_time = ''
gps_info = ''
gps_hour = ''
last_sec = '' 
gps_year = ''
gps_month = ''
gps_day = ''
gps_hour = ''
gps_min = ''
gps_sec = ''

latitude = ''
longitude = ''
altitude = ''
speed = ''
headingangle = ''
roll = ''
pitch = ''

count = -1
start = 0

lidar_path = ''
gps_path = ''
camera_path = ''

def make_folders(path):
    global lidar_path
    global gps_path
    global camera_path

    print(os.getcwd())

    ###### 'S': SUM #######
    scenario = '_S'
    #######################
    
    if not os.path.exists('./data/' + path.split('_')[0]):
        print(path) # 220725_185228
        print(path.split('_')[0])   # 220725
        os.mkdir('./data/' + path.split('_')[0])


    lidar_path = './data/' + path.split('_')[0] + '/' + path + scenario + '/lidar/'  # ./220725/220725_185228_S_T/lidar/
    gps_path = './data/' + path.split('_')[0] + '/' + path + scenario + '/gps/'
    camera_path = './data/' + path.split('_')[0] + '/' + path + scenario + '/image/'
    calibration_result_path = './data/' + path.split('_')[0] + '/' + path + scenario + '/'

    if not os.path.exists(lidar_path):
        os.makedirs(lidar_path)
    if not os.path.exists(gps_path):    
        os.makedirs(gps_path)

    if not os.path.exists(camera_path[:-1] + '_L/'):
        os.makedirs(camera_path[:-1] + '_L/')
    if not os.path.exists(camera_path[:-1] + '_F/'):
        os.makedirs(camera_path[:-1] + '_F/')
    if not os.path.exists(camera_path[:-1] + '_R/'):
        os.makedirs(camera_path[:-1] + '_R/')
    if not os.path.exists(camera_path[:-1] + '_B/'):
        os.makedirs(camera_path[:-1] + '_B/')

    # copy calibration result txt
    shutil.copy('./calibration_result/lidar-image_calib.txt', calibration_result_path)



def Camera0_callback(msg):  # Left Camera
    # img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
    # img = np.frombuffer(msg.data, dtype=np.uint8).reshape(720, 1280, -1)
    np_arr = np.fromstring(msg.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    camera0_list.append(img)

    if(len(camera0_list) > 2):
        camera0_list.pop(0)


def Camera1_callback(msg):  # Front Camera
    np_arr = np.fromstring(msg.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    camera1_list.append(img)

    if(len(camera1_list) > 2):
        camera1_list.pop(0)


def Camera2_callback(msg):  # Right Camera
    np_arr = np.fromstring(msg.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    camera2_list.append(img)

    if(len(camera2_list) > 2):
        camera2_list.pop(0)


def Camera3_callback(msg):  # Back Camera
    np_arr = np.fromstring(msg.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    camera3_list.append(img)

    if(len(camera3_list) > 2):
        camera3_list.pop(0)


def GPS_callback(msg):
    global start
    global gps_file_name
    global gps_hour
    global gps_info
    global count
    global last_sec
    global gps_sec
    global gps_year
    global gps_month
    global gps_day
    global gps_min
    global latitude
    global longitude
    global altitude
    global speed
    global headingangle 
    global roll 
    global pitch

    if (count == -1):
        count = 0
        print("count -1 -> 0", count)

    gps_hour = int(msg.Time[0:2]) + 9
    gps_hour = gps_hour if (gps_hour < 24) else (gps_hour - 24) 
    gps_min = int(msg.Time[2:4])
    gps_sec = int(msg.Time[4:6])

    gps_year = int(msg.Time[10:12])
    gps_month = int(msg.Time[12:14])
    gps_day = int(msg.Time[14:])

    latitude = msg.Latitude
    longitude = msg.Longitude
    altitude = msg.Altitude
    speed = msg.Speed
    headingangle = msg.HeadingAngle
    roll = msg.Roll
    pitch = msg.Pitch

    # gps_file_name = 'GPS_%02d%02d%02d_%02d%02d%02d_%04d' % (gps_year, gps_month, gps_day, gps_hour, gps_min, gps_sec, count)

    # while os.path.exists(gps_path + gps_file_name + '.csv'):
    #     print("exist")
    #     count += 1
    #     gps_file_name = 'GPS_%02d%02d%02d_%02d%02d%02d_%04d' % (gps_year, gps_month, gps_day, gps_hour, gps_min, gps_sec, count)

    # gps_file_name = 'GPS_%02d%02d%02d_%02d%02d%02d_%04d' % (gps_year, gps_month, gps_day, gps_hour, gps_min, gps_sec, count)

    # gps_time = '%02d%02d%02d.%d' % (gps_hour, gps_min, gps_sec, count)

    # gps_info = gps_time + ',%.8f,%.8f,%.2f,%.2f,%.2f,%.2f,%.2f' % (latitude, longitude, altitude, speed * 3.6, headingangle, roll, pitch)

    # gps_string.append(gps_info)

    # if(len(gps_string) > 2):
    #     gps_string.pop(0)  


def save_img(sensor_file_name):
    global camera_path 

    if (len(camera0_list) > 0) and (len(camera1_list) > 0) and (len(camera2_list) > 0) and (len(camera3_list) > 0):
        img0 = camera0_list[len(camera0_list)-1]    # Left
        img1 = camera1_list[len(camera1_list)-1]    # Front
        img2 = camera2_list[len(camera2_list)-1]    # Right
        img3 = camera3_list[len(camera3_list)-1]    # Back

        cv2.imwrite(camera_path[:-1] + '_L/' + sensor_file_name + '_L.png', img0)
        cv2.imwrite(camera_path[:-1] + '_F/' + sensor_file_name + '_F.png', img1)
        cv2.imwrite(camera_path[:-1] + '_R/' + sensor_file_name + '_R.png', img2)
        cv2.imwrite(camera_path[:-1] + '_B/' + sensor_file_name + '_B.png', img3)

        print('save img: ', camera_path[:-1] + '_L/' + sensor_file_name + '_L.png')
        print('save img: ', camera_path[:-1] + '_F/' + sensor_file_name + '_F.png')
        print('save img: ', camera_path[:-1] + '_R/' + sensor_file_name + '_R.png')
        print('save img: ', camera_path[:-1] + '_B/' + sensor_file_name + '_B.png')


def save_gps():
    global start
    global gps_info
    global gps_file_name
    global gps_path
    global count

    sensor_file_name = ''

    if (start == 1):
        print(os.getcwd())
        path = gps_file_name.split('_')[1] + '_' + gps_file_name.split('_')[2]    # example: 220725_185224
        make_folders(path)
        start = 0

    gps_file_name_fix = gps_file_name
    f = open(gps_path + gps_file_name_fix + '.csv','w') 
    f.write(gps_info) 
    f.close()

    print('save gps: ', gps_path + gps_file_name_fix + '.csv')
    sensor_file_name = gps_file_name_fix[4:]

    return sensor_file_name

index = 0
def convert_pcl(data, sensor_file_name):
    lidar_str = lidar_path + sensor_file_name + '.pcd'

    global index
    index = index +1



    header = '''# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z reflectivity
SIZE 4 4 4 4
TYPE F F F F
COUNT 1 1 1 1
WIDTH %d
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS %d
DATA binary'''
    header = header + '\n'
    header_byte = str.encode(header)


    # with open(lidar_str % index, 'wb') as f:
    with open(lidar_str, 'wb') as f:
        # f.write( bytearray( header_byte % (data.width, data.height, data.width*data.height)))
        f.write( ( header_byte % (data.width * data.height, data.width * data.height)))
        
        for p in pc2.read_points(data, skip_nans=True): 

            p0 = struct.pack('<f',p[0])
            p1 = struct.pack('<f',p[1])
            p2 = struct.pack('<f',p[2])
            p3 = struct.pack('<f',float(p[5]))

            f.write(p0)
            f.write(p1)
            f.write(p2)
            f.write(p3)

        f.close()
    
    print('save pcd: ', ' ', lidar_str)
    

def LiDAR_callback(msg):
    global count
    global last_sec
    global gps_sec
    global gps_year
    global gps_month
    global gps_day
    global gps_hour
    global gps_min
    global gps_file_name
    global gps_time
    global gps_info

    if (last_sec != gps_sec):
        count = 0
    else:
        count = count + 1        

    last_sec = gps_sec

    print("-------------------------------------------------------------", count)

    gps_file_name = 'GPS_%02d%02d%02d_%02d%02d%02d_%04d' % (gps_year, gps_month, gps_day, gps_hour, gps_min, gps_sec, count)

    gps_time = '%02d%02d%02d.%d' % (gps_hour, gps_min, gps_sec, count)

    gps_info = gps_time + ',%.8f,%.8f,%.2f,%.2f,%.2f,%.2f,%.2f' % (latitude, longitude, altitude, speed * 3.6, headingangle, roll, pitch)
    
    sensor_file_name = save_gps()
    # save_pcd(msg, sensor_file_name)    # no intensity
    convert_pcl(msg, sensor_file_name)   # yes intensity
    save_img(sensor_file_name)
    

# def save_pcd(cloud, sensor_file_name):
#     global lidar_path

#     p = pcl.PointCloud(np.array(list(pc2.read_points(cloud, field_names=("x", "y", "z", "intensity"))), dtype=np.float32)[:, 0:3])
#     lidar_str = lidar_path + sensor_file_name + '.pcd'
#     # p.to_file(bytes(lidar_str, 'utf-8' ))
#     # p.to_file(bytes(lidar_str, 'utf-8' ))

#     pcl.save_XYZRGBA(p, lidar_str)
#     print('save pcd: ', ' ', lidar_str)


def main():
    global start
    start = 1

    rospy.init_node('time_sequence', anonymous=False)
    rospy.Subscriber(LiDAR_topic, PointCloud2, LiDAR_callback)

    # Callback Camera
    rospy.Subscriber(Camera0_topic, CompressedImage, Camera0_callback)
    rospy.Subscriber(Camera1_topic, CompressedImage, Camera1_callback)
    rospy.Subscriber(Camera2_topic, CompressedImage, Camera2_callback)
    rospy.Subscriber(Camera3_topic, CompressedImage, Camera3_callback)
    
    # Callback GPS
    rospy.Subscriber(GPS_topic, gps_49, GPS_callback)

    # rospy.spin()
    rate = rospy.Rate(10) # hz

    while not rospy.is_shutdown():
        # save
        rate.sleep()

if __name__ == '__main__':
    main()

