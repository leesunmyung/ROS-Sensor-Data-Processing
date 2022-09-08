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

lidar_stamp = ''
lidar_list = []

c0_list = []
c1_list = []
c2_list = []
c3_list = []


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
    shutil.copy('./calibration_result_os2/lidar-image_calib.txt', calibration_result_path)



def Camera0_callback(msg):  # Left Camera
    # img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
    # img = np.frombuffer(msg.data, dtype=np.uint8).reshape(720, 1280, -1)

    global c0_list
    c0_list.append(msg)

    if(len(c0_list) > 4):
        c0_list.pop(0)


def Camera1_callback(msg):  # Front Camera
    global c1_list
    c1_list.append(msg)

    if ((len(c1_list)) > 4):
        c1_list.pop(0)


def Camera2_callback(msg):  # Right Camera
    global c2_list
    c2_list.append(msg)

    if ((len(c2_list)) > 4):
        c2_list.pop(0)


def Camera3_callback(msg):  # Back Camera
    global c3_list
    c3_list.append(msg)

    if ((len(c3_list)) > 4):
        c3_list.pop(0)


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


def save_img(ca0_msg, ca1_msg, ca2_msg, ca3_msg, sensor_file_name):
    global camera_path 

    # Before modifying camera delay
    # if (len(camera0_list) > 0) and (len(camera1_list) > 0) and (len(camera2_list) > 0) and (len(camera3_list) > 0):
    # img0 = camera0_list[len(camera0_list)-1]    # Left
    # img1 = camera1_list[len(camera1_list)-1]    # Front
    # img2 = camera2_list[len(camera2_list)-1]    # Right
    # img3 = camera3_list[len(camera3_list)-1]    # Back

    np_arr0 = np.fromstring(ca0_msg.data, np.uint8)
    img0 = cv2.imdecode(np_arr0, cv2.IMREAD_COLOR)

    np_arr1 = np.fromstring(ca1_msg.data, np.uint8)
    img1 = cv2.imdecode(np_arr1, cv2.IMREAD_COLOR)

    np_arr2 = np.fromstring(ca2_msg.data, np.uint8)
    img2 = cv2.imdecode(np_arr2, cv2.IMREAD_COLOR)

    np_arr3 = np.fromstring(ca3_msg.data, np.uint8)
    img3 = cv2.imdecode(np_arr3, cv2.IMREAD_COLOR)

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



def convert_pcl(data, sensor_file_name):
    
    lidar_str = lidar_path + sensor_file_name + '.pcd'

    # Header
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

    with open(lidar_str, 'wb') as f:

        # PCD Header 
        # f.write( ( header_byte % (data.width * data.height, data.width * data.height)))
        
        outlier_range = 0.3
        outlider_count = 0
        all_point_count = 0
        point_count = 0

        for p in pc2.read_points(data, skip_nans=True):
            all_point_count += 1
            if ((abs(p[0]) <= outlier_range) and (abs(p[1]) <= outlier_range) and (abs(p[2]) <= outlier_range)):
                outlider_count += 1
                continue 

        point_count = all_point_count - outlider_count
        f.write((header_byte % (point_count, point_count)))

        print("outlier count: ", outlider_count)
        print("all point count: ", all_point_count)
        print("all point count - outlier count: ", point_count)

        for p in pc2.read_points(data, skip_nans=True): 

            if ((abs(p[0]) <= outlier_range) and (abs(p[1]) <= outlier_range) and (abs(p[2]) <= outlier_range)):
                outlider_count += 1
                # print("removed: ", p[0], p[1], p[2])
                continue
                
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
    global lidar_list


    # CODE: 0~9 count per 1 sec
    if (last_sec != gps_sec):
        count = 0
    else:
        count = count + 1        

    last_sec = gps_sec

    print("\n-------------------------------------------------------------", count)

    gps_file_name = 'GPS_%02d%02d%02d_%02d%02d%02d_%04d' % (gps_year, gps_month, gps_day, gps_hour, gps_min, gps_sec, count)

    gps_time = '%02d%02d%02d.%d' % (gps_hour, gps_min, gps_sec, count)

    gps_info = gps_time + ',%.8f,%.8f,%.2f,%.2f,%.2f,%.2f,%.2f' % (latitude, longitude, altitude, speed * 3.6, headingangle, roll, pitch)
    
    lidar_list.append(msg)

    if(len(lidar_list)>= 3):

        sensor_file_name = save_gps()
        convert_pcl(msg, sensor_file_name)   # intensity O

        lidar_msg = lidar_list.pop(0)

        lidar_time_stamp = lidar_msg.header.stamp.secs + lidar_msg.header.stamp.nsecs/1000000000.0
        print('>> lidar_time_stamp: ', lidar_time_stamp, '\n')

        min_diff = 100
        min_index0 = -1
        min_index1 = -1
        min_index2 = -1
        min_index3 = -1

        for i in range(0, len(c0_list)):
            c0_time_stamp = (c0_list[i].header.stamp.secs + c0_list[i].header.stamp.nsecs/1000000000.0)
            diff = abs(lidar_time_stamp - c0_time_stamp)
            # print('c0_time_stamp: ', c0_time_stamp, 'diff: ', diff)
            if (diff < min_diff):
                min_index0 = i
                min_diff = diff
        print('>> selected_c0_time_stamp: ', c0_list[min_index0].header.stamp.secs + c0_list[min_index0].header.stamp.nsecs/1000000000.0, ", selcted_index: ", min_index0, ', diff: ', min_diff, '\n')
        
        min_diff = 100
        for i in range(0, len(c1_list)):
            c1_time_stamp = (c1_list[i].header.stamp.secs + c1_list[i].header.stamp.nsecs/1000000000.0) 
            diff = abs(lidar_time_stamp - c1_time_stamp)
            # print('c1_time_stamp: ', c1_time_stamp, 'diff: ', diff)
            if (diff < min_diff):
                min_index1 = i
                min_diff = diff
        print('>> selected_c1_time_stamp: ', c1_list[min_index1].header.stamp.secs + c1_list[min_index1].header.stamp.nsecs/1000000000.0, ", selcted_index: ", min_index1, ', diff: ', min_diff, '\n')

        min_diff = 100
        for i in range(0, len(c2_list)):
            c2_time_stamp = (c2_list[i].header.stamp.secs + c2_list[i].header.stamp.nsecs/1000000000.0) 
            diff = abs(lidar_time_stamp - c2_time_stamp)
            # print('c2_time_stamp: ', c2_time_stamp, 'diff: ', diff)
            if (diff < min_diff):
                min_index2 = i
                min_diff = diff
        print('>> selected_c2_time_stamp: ', c2_list[min_index2].header.stamp.secs + c2_list[min_index2].header.stamp.nsecs/1000000000.0, ", selcted_index: ", min_index2, ', diff: ', min_diff, '\n')

        min_diff = 100
        for i in range(0, len(c3_list)):
            c3_time_stamp = (c3_list[i].header.stamp.secs + c3_list[i].header.stamp.nsecs/1000000000.0) 
            diff = abs(lidar_time_stamp - c3_time_stamp)
            # print('c3_time_stamp: ', c3_time_stamp, 'diff: ', diff)
            if (diff < min_diff):
                min_index3 = i
                min_diff = diff
        print('>> selected_c3_time_stamp: ', c3_list[min_index3].header.stamp.secs + c3_list[min_index3].header.stamp.nsecs/1000000000.0, ", selcted_index: ", min_index3, ', diff: ', min_diff, '\n')

        ca0_msg = c0_list[min_index0]
        ca1_msg = c1_list[min_index1]
        ca2_msg = c2_list[min_index2]
        ca3_msg = c3_list[min_index3]

        save_img(ca0_msg, ca1_msg, ca2_msg, ca3_msg, sensor_file_name)



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

