import os
import sys
import shutil
from pathlib import Path 

def main():

    first_file = 1
    first_file_after_cropped = 1
    file_count= 0
    remove_file_count = 0
    modified_dir_count = 0
    file_check_first = ['' for i in range(6)]
    file_check_last = ['' for i in range(6)]

    print(os.getcwd())

    if len(sys.argv) != 2:
        print("Insufficient arguments")
        sys.exit()

    elif (len((sys.argv[1]).split('_')) != 3): 
        print("Re-enter directory name")
        sys.exit()
    else:
        dirname = sys.argv[1] # '220817_062414_S'
    
    path = './data/' + dirname.split('_')[0] + '/' + dirname

    # Change directory to '220817_062414_S'
    os.chdir(path)
    print(os.getcwd())

    dirs = []
    for dir in os.listdir():
        if os.path.isdir(dir):
            dirs.append(dir)
    
    dirs.sort()
    print(dirs)

    for dir in dirs:
        first_file = 1
        first_file_after_cropped = 1
        file_count= 0
        remove_file_count = 0

        os.chdir(dir)
        print(os.getcwd())

        files = os.listdir()
        init_file_num = len(files)
        print("Before cropping, file num: ", init_file_num)

        files.sort()

        if (len(files) != 200):
            for file in files:
                filename = file
                sec = ''

                if (dir == 'gps'):
                    sec = (filename.split('_')[2])[4:]
                else:
                    sec = (filename.split('_')[1])[4:]

                if (first_file == 1):
                    first_sec = sec
                    first_file = 0
                
                if (sec == first_sec):
                    os.remove(file)
                    remove_file_count += 1
                    print('Removing file: ', remove_file_count, ' / ', file)
                    continue
                
                else:
                    if (first_file_after_cropped == 1):
                        if (dir == 'gps'):
                            first_file_after_sec = (filename.split('_')[2])
                        else:
                            sec = (filename.split('_')[1])
                        first_file_after_cropped = 0

                    file_count += 1
        
                if (file_count <= 200):
                    if (((((filename.split('.')[0])[-2:]) == '10')) or (((filename.split('_')[2]))[-2:] == '10') and ((filename.split('_')[0] == '2'))):
                        os.remove(file)
                        remove_file_count += 1
                        file_count -= 1
                        print('Removing file: %2d' % (remove_file_count), '10th file: ', file)
                    continue
                else:
                    os.remove(file)
                    remove_file_count += 1
                    print('Removing file: %2d' % (remove_file_count), ' / ', file)

            files = os.listdir()
            files.sort()

            # print('modified_file_num: ', modified_file_num)
            modified_file_num = len(files)
            print('init_file_num: ', init_file_num)
            print('modified_file_num: ', modified_file_num)
            print('remove_file_count: ', remove_file_count)

            if (((init_file_num - modified_file_num) == remove_file_count) and (modified_file_num == 200)):
                modified_dir_count += 1
                print(remove_file_count, ' files deleted')
                print("After cropping, file num: ", init_file_num, ' -> ', modified_file_num)

            file_check_first.append(files[0])
            file_check_last.append(files[-1])


            os.chdir('..')

    os.chdir('..')

    if (modified_dir_count == 6):
        print("All 6 directories modified")
        
        for i in range(0, len(file_check_first)):
            # print(file_check_first[i], ' ', file_check_last[i])   # first, last file
            print('%26s %26s' % (file_check_first[i], file_check_last[i]))


    # '220817_062414_S'
    dir_rename = dirname.split('_')[0] + '_' + first_file_after_sec + '_S'

    shutil.copytree('./' + dirname, './' + dir_rename)
    shutil.rmtree('./' + dirname)

    print("Original directory deleted: ", dirname)
    print("Directory name changed: ", dirname, ' -> ', dir_rename, '\n')


if __name__ == "__main__":
	main()