import sys
import os
import time
import rospy
# import rosbag
import subprocess
import yaml
# from tkinter import filedialog
# from tkinter import *
import datetime
from time import strftime
from time import gmtime

# def openFolder():
#     root = tkinter.Tk()
#     root.withdraw()
#     folder_name = filedialog.askdirectory(parent=root,initialdir=".",title='Please select a directory')
#     print("Selected Folder : ", folder_name)
#     os.chdir(folder_name)


def main():
    # openFolder()

    if len(sys.argv) != 2:
        print("Enter folder name")
        sys.exit()
    
    else:
        folder_name = sys.argv[1]
        print("Selected folder: ", folder_name)

    os.chdir(folder_name)

    os.getcwd()

    files = os.listdir()

    total_duration = 0.0
    count = 0

    for file in files:
        if not (file.endswith('.bag')):
            continue
        info_dict = yaml.load(subprocess.Popen(['rosbag', 'info', '--yaml', file], stdout=subprocess.PIPE).communicate()[0])
        duration = info_dict['duration']
        total_duration += duration
        count += 1
        print('[%3d] ' % (count), 'Bag file: ', file, ', Duration: %12f' % (duration), 'sec')

    hhmmss = str(datetime.timedelta(seconds=total_duration))
    print('------------------------------')
    print('Folder: ', folder_name)
    print('Count: ', count)
    print('Total Duration: %12f' % (total_duration), 'sec', '(%2dh %2dm %2ds)' % (int(hhmmss.split(':')[0]), int(hhmmss.split(':')[1]), int((hhmmss.split(':')[2]).split('.')[0])))
    print('')
    

if __name__ == "__main__":
	main()
