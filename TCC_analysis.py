"""used to analyse my results"""

import os
from os.path import isfile, join
from numpy import array, average
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
        df = list(read_csv(f'{directory}/{item[2]}').get('0'))
        data_.append(
            {
                'weight': item[0],
                'time_start': item[1][0],
                'time_end': item[1][1],
                'read_offset': round(average(df[:100])),
                'read_load': round(average(df[1000:3000])),
                'read_full': df,
            }
        )

    return data_


def time_format(time_string: str):
    t = time_string.split('_')
    start_time = f"{t[0]}:{t[1]}:{t[2]}"
    end_time = f"{t[3]}:{t[4]}:{t[5]}"
    return start_time, end_time


def adjust_weights(load: int, offset: int):

    # offset = -(-735)

    weights_kg = {
        'nut': 3.06E-3,
        'fuse': 48.63E-3,
        'weight_1': 86.73E-3,
        'weight_2': 198.38E-3,
        'weight_3': 997.13E-3,
        'weight_a': 497.66E-3,
        'weight_b': 495.24E-3
    }

    loads = {
        'nothing': 0,
        'fuse_and_nut': weights_kg['fuse'] + weights_kg['nut'],
        'only_fuse': weights_kg['fuse'],
        'weight_1': weights_kg['weight_1'] + weights_kg['fuse'] + weights_kg['nut'],
        'weight_2': weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        'weight_3': weights_kg['weight_3'] + weights_kg['fuse'] + weights_kg['nut'],
        'weight_a': weights_kg['weight_a'] + weights_kg['fuse'] + weights_kg['nut'],
        'weight_b': weights_kg['weight_b'] + weights_kg['fuse'] + weights_kg['nut']
    }

    factors = {
        loads['only_fuse']: -711 + offset,
        loads['fuse_and_nut']: -708 + offset,
        loads['weight_1']: -680 + offset,
        loads['weight_2']: -622 + offset,
        loads['weight_3']: -274.82 + offset,
        loads['weight_a']: -500.53 + offset,
        loads['weight_b']: -496.19 + offset
    }

    # # plot factor distribution
    # import matplotlib.pyplot as plt
    # plt.plot(list(factors.values()), list(factors.keys()), 'o')

    adjusted_value = offset + factors[load]

    return adjusted_value


dir_ = 'Results/sep_24_1'

data = data_from_directory_files(dir_)


# plt.figure()

# legend = []
# for item in data[:-3]:
#     plt.plot(item['dataset'][0:100])
#     legend.append(item['weight'])
#
# plt.legend(legend)
# plt.show()
#
# plt.figure()
#
# legend = []
# for item in data[:-3]:
#     plt.plot(item['dataset'][1000:3000])
#     legend.append(item['weight'])
#
# plt.legend(legend)
# plt.show()
