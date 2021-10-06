"""used to analyse my results"""

import os
from os.path import isfile, join
from numpy import array
from pandas import read_csv
import matplotlib.pyplot as plt


def data_from_directory_files(directory: str):
    """
    extracts data from files in a directory
    """
    files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
    result_strings = [file.split('Report_')[1].split('.csv')[0] for file in files]  # load, start time, end time
    times = [time_format(time_string[-17:]) for time_string in result_strings]
    loads = [load_string[:-18].split('_')[-1] for load_string in result_strings]
    result = array([loads, times, files]).T

    data_ = []

    for item in result:
        data_.append(
            {
                'weight': item[0],
                'time_start': item[1][0],
                'time_end': item[1][1],
                'dataset': list(read_csv(f'{directory}/{item[2]}').get('0'))
            }
        )

    return data_


def time_format(time_string: str):
    t = time_string.split('_')
    start_time = f"{t[0]}:{t[1]}:{t[2]}"
    end_time = f"{t[3]}:{t[4]}:{t[5]}"
    return start_time, end_time


dir_ = 'Results/sep_24_1'

data = data_from_directory_files(dir_)

plt.figure()


for item