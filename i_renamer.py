#!/usr/bin/env python3
# the script that rename folders after iPhoto export
# "Place, 24 April 2020" -> "2020-04-24 Place"
# or
# "24 April 2020" -> "2020-04-24"
# to use run script and provide folder path  ~/Downloads/temp/ with last "/" definitely
import sys
import re
import calendar
from pathlib import Path
from os import listdir
from os.path import isdir, join


def get_date_with_place(dir_name):
    day = re.search('[a-zA-Z0-9_ ]*,\s(\d{1,2}).*', dir_name).group(1)
    if len(str(day)) == 1:
        day = "0" + str(day)
    month_letter = re.search('January|February|March|April|May|June|July|August|September|October|November|December',
                             dir_name).group(0)
    month_digit = list(calendar.month_abbr).index(month_letter[:3])
    if len(str(month_digit)) == 1:
        month_digit = "0" + str(month_digit)

    year = re.search('\d{4}$', dir_name).group(0)
    date = str(year) + '-' + str(month_digit) + '-' + str(day)
    location_raw = re.search('^.+?(?=,)', dir_name).group(0)
    location = re.sub('Home', 'Lelystad', location_raw)
    dir_name_new = str(date) + ' ' + str(location)
    return dir_name_new


def get_date_no_place(dir_name):
    day = re.search('^\d{1,2}', dir_name).group(0)
    if len(str(day)) == 1:
        day = "0" + str(day)
    month_letter = re.search(
        '^\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}$',
        dir_name).group(1)
    month_digit = list(calendar.month_abbr).index(month_letter[:3])
    if len(str(month_digit)) == 1:
        month_digit = "0" + str(month_digit)

    year = re.search('\d{4}$', dir_name).group(0)
    date = str(year) + '-' + str(month_digit) + '-' + str(day)
    dir_name_new = str(date)
    return dir_name_new


def rename_with_place(dir_name):
    data_file = Path(folder_path + dir_name)
    data_file.rename(folder_path + str(get_date_with_place(dir_name)))


def rename_no_place(dir_name):
    data_file = Path(folder_path + dir_name)
    data_file.rename(folder_path + str(get_date_no_place(dir_name)))


# check is the path to directory defined
# if defined get it
if len(sys.argv) < 2:
    print('Not all variables defined')
    exit(1)
else:
    folder_path = sys.argv[1]

# get all directories name before rename
onlydir = [f for f in listdir(folder_path) if isdir(join(folder_path, f))]
print(onlydir)

# iterate over directories and check
for i in onlydir:
    pattern_with_place = re.compile(
        '^.*,\s\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}$')
    pattern_no_place = re.compile(
        '^\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}$')
    if pattern_with_place.match(i):
        rename_with_place(str(i))
    elif pattern_no_place.match(i):
        rename_no_place(str(i))
    else:
        print('Dirrectory ' + i + ' is not in a iPhoto format')

# print separater
print('==== result ====')

# get all directories name after rename
onlydir = [f for f in listdir(folder_path) if isdir(join(folder_path, f))]
print(onlydir)
