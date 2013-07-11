#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sajnikanth  (http://sajnikanth.com)

import fnmatch
import os
import lib.EXIF as EXIF

class bcolors:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'

location = raw_input(bcolors.BLUE + "Enter the location of your photos (full path with no ~ or trailing /): " + bcolors.ENDC)
if location == "":
    print bcolors.YELLOW + "using default location /Users/sajnikanth/Dropbox/Photos 0001-0097/..." + bcolors.ENDC
    location = "/Users/sajnikanth/Dropbox/Photos 0001-0097/"

# Look for JPG images in that location
jpg_files = []
for root, dirnames, filenames in os.walk(location):
    for filename in fnmatch.filter(filenames, '*.jpg'):
        jpg_files.append(os.path.join(root, filename))

# If there are JPG images in that location
if len(jpg_files) > 0:

    # Get EXIF from all images in that location
    raw_data_from_jpg_files = {}
    fail_counter = 0
    for i in range(0, len(jpg_files)):
        raw_data_from_jpg_files[jpg_files[i]] = EXIF.process_file(open(jpg_files[i]))  # raw_data_from_jpg_files now has {filename1_with_path:{exif_info1:exif_value1, exif_info2:exif_value2}, filename2_with_path....}
        filename = jpg_files[i].split("/")[(len(jpg_files[i].split("/"))-1)]
        parent_directory = jpg_files[i].split("/")[(len(jpg_files[i].split("/"))-2)]
        # Check if there's a Date field in EXIF
        if any("Date" in s for s in raw_data_from_jpg_files.get(jpg_files[i]).keys()):
            pass
        else:
            open("failures.log", "a").write(parent_directory + "/" + filename + "\n")
            fail_counter +=1

    # Get Dates for all images and dump them in results.csv
    pass_counter = 0
    open("results.csv", "a").write("File Name,Date,Time\n")
    for file_name in raw_data_from_jpg_files:
        jpg_exif_info = raw_data_from_jpg_files[file_name].keys()  # create a list of exif_info
        for i in range(0, len(jpg_exif_info)):
                if "DateTimeOriginal" in jpg_exif_info[i]:
                    jpg_image_date = str(raw_data_from_jpg_files[file_name][jpg_exif_info[i]].values).split(" ")[0]
                    jpg_image_time = str(raw_data_from_jpg_files[file_name][jpg_exif_info[i]].values).split(" ")[1]
                    open("results.csv", "a").write(file_name + "," + jpg_image_date + "," + jpg_image_time + "\n")
                    pass_counter +=1

    # Print Stats at the end
    print bcolors.BLUE + str(len(jpg_files)) + bcolors.ENDC + " photos found"
    print bcolors.GREEN + str(pass_counter) + bcolors.ENDC + " photos had Date and Time information. Check results.csv"
    if fail_counter > 0:
        print bcolors.RED + str(fail_counter) + bcolors.ENDC + " photos didn't have date info. Check failures.log"

else:
    print bcolors.RED + "There were no photos in that location" + bcolors.ENDC
