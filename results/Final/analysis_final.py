"""used to analyse my results"""

import os
from os.path import isfile, join
from numpy import array, average, linspace
from scipy.stats import linregress
from pandas import read_csv, DataFrame
from datetime import datetime
import matplotlib.pyplot as plt

# AMP_FACTOR = 1 / 123

_ANALYSIS = 'x14h'

dir_ = f'{_ANALYSIS}'

weights_kg = {
    'nut': 3.06E-3,
    'fuse': 48.63E-3,
    'weight_1': 86.73E-3,
    'weight_2': 198.38E-3,
    'weight_3': 997.13E-3,
    'weight_a': 497.66E-3,
    'weight_b': 495.24E-3
}

if _ANALYSIS == 'x14h':

    loads = {
        '0': 0,  #
        '1': weights_kg['weight_1'] + weights_kg['fuse'] + weights_kg['nut'],
        '2': weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        '1_2': weights_kg['weight_1'] + weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        '3_a': weights_kg['weight_a'] + weights_kg['fuse'] + weights_kg['nut'],
        '3_a_p_1': weights_kg['weight_a'] + weights_kg['weight_1'] + weights_kg['fuse'] + weights_kg['nut'],
        '3_a_p_2': weights_kg['weight_a'] + weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        '3_a_p_2_p_1': weights_kg['weight_a'] + weights_kg['weight_1'] + weights_kg['weight_2'] + weights_kg['fuse'] +
                       weights_kg['nut'],
        '4': weights_kg['weight_3'] + weights_kg['fuse'] + weights_kg['nut'],
        '4_p_1': weights_kg['weight_3'] + weights_kg['weight_1'] + weights_kg['fuse'] + weights_kg['nut'],
        '4_p_2': weights_kg['weight_3'] + weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        '4_p_2_p_1': weights_kg['weight_3'] + weights_kg['weight_1'] + weights_kg['weight_2'] + weights_kg['fuse'] +
                     weights_kg['nut'],
    }

    colors = {
        '0': 'black',
        '1': 'black',
        '2': 'black',
        '1_2': 'black',
        '3_a': 'black',
        '3_a_p_1': 'black',
        '3_a_p_2': 'black',
        '3_a_p_2_p_1': 'black',
        '4': 'black',
        '4_p_1': 'black',
        '4_p_2': 'black',
        '4_p_2_p_1': 'black',
    }

else:
    loads = {
        '0': 0,
        'fuse_and_nut': weights_kg['fuse'] + weights_kg['nut'],
        'only_fuse': weights_kg['fuse'],
        '1': weights_kg['weight_1'] + weights_kg['fuse'] + weights_kg['nut'],
        '2': weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        '3': weights_kg['weight_3'] + weights_kg['fuse'] + weights_kg['nut'],
        'a': weights_kg['weight_a'] + weights_kg['fuse'] + weights_kg['nut'],
        'b': weights_kg['weight_b'] + weights_kg['fuse'] + weights_kg['nut'],

    }

    colors = {
        '1': 'red',
        '2': 'green',
        '3': 'blue',
        'a': 'yellow',
        'b': 'cyan',
        '0': 'black',
    }


def data_from_directory_files(directory, delete_plots=False):
    """
    extracts data from files in a directory
    """

    files = [f for f in os.listdir(directory) if isfile(join(directory, f)) and '.csv' in f]
    result_strings = [file.split('Report_')[1].split('.csv')[0] for file in files]  # load, start time, end time
    times = [time_format(time_string[-17:]) for time_string in result_strings]

    if _ANALYSIS == 'x14h':
        loads_list = [load_string[:-18] for load_string in result_strings]
    else:
        loads_list = [load_string[:-18].split('_')[-1] for load_string in result_strings]

    result = array([loads_list, times, files]).T

    if delete_plots:
        files_to_delete = [f for f in os.listdir(directory) if isfile(join(directory, f)) and '.png' in f]
        if files_to_delete:
            print(f'{files_to_delete} removed')

    data_ = []

    for item in result:
        df = list(read_csv(f'{directory}/{item[2]}').get('0'))
        weight_value = get_weight_value(item[0])
        read_offset = round(average(df[:100]))
        read_load = round(average(df[-100:]))
        if read_offset > read_load:
            read_load = read_offset
            read_offset = round(average(df[-100:]))
        data_.append(
            {
                'weight_class': item[0],
                'weight_value': weight_value,
                'strain_value': get_strain_value(weight_value) * 1e6,
                'file_name': item[2],
                'time_start': item[1][0],
                'time_end': item[1][1],
                'read_offset': read_offset,
                'read_load': read_load,
                'read_full': df,
            }
        )

    return data_


def time_format(time_string):
    t = time_string.split('_')
    start_time = f"{t[0]}:{t[1]}:{t[2]}"
    end_time = f"{t[3]}:{t[4]}:{t[5]}"

    return start_time, end_time


def get_weight_value(weight_class):
    if _ANALYSIS == 'x14h':
        if 'r' in weight_class:
            weight_class = weight_class[6:]
        else:
            weight_class = weight_class[4:]

    return loads[weight_class]


def get_strain_value(weight):
    P = weight * 9.81
    E = 85186548337.0813
    L = 155E-3
    b = 20E-3
    t = 2E-3
    return (6 * P * L) / (E * b * t ** 2)


def read_adjust(data_):
    read_array = array(data_['read_full']) - data_['read_offset']
    transfer_constant = data_['weight_value'] / (data_['read_load'] - data_['read_offset'])

    return read_array * transfer_constant


def transform_to_strain(_series):
    a = 2.888090284
    b = -363.431054
    return a * _series + b


def plot_read(plot_item, adjust=True, savefig=False, savefig_dir=''):
    plt.close()
    plt.figure()

    time_start = datetime.strptime(plot_item['time_start'], '%H:%M:%S')
    time_end = datetime.strptime(plot_item['time_end'], '%H:%M:%S')
    delta_t = time_end - time_start
    time_axis = linspace(
        0,
        delta_t.seconds,
        len(plot_item['read_full'])
    )

    if adjust:
        load_axis = read_adjust(plot_item)
        load_hline = round(plot_item['weight_value'], 2)
        load_unit = 'kg'
        plt.ylabel('load value [kg]')
        filecomp = ''
    else:
        load_axis = plot_item['read_full']
        if plot_item['read_load'] >= plot_item['read_offset']:
            load_hline = plot_item['read_load']
        else:
            load_hline = plot_item['read_offset']
        load_unit = ''
        plt.ylabel('load value [ADC units]')
        filecomp = '_ADCunits'

    plt.plot(time_axis, load_axis, color=colors[plot_item['weight_class'].split('c_')[-1].split('r_')[-1]])
    plt.axhline(load_hline, color='orange', linestyle='--')
    plt.xlabel('Elapsed time [s]')

    plt.legend(
        [
            f'weight class {plot_item["weight_class"]}',
            f'{load_hline} {load_unit}'
        ]
    )

    if savefig:

        if savefig_dir:
            filename = f'{savefig_dir}/{plot_item["file_name"].rstrip(".csv")}{filecomp}.png'
        else:
            filename = f'{plot_item["file_name"].rstrip(".csv")}{filecomp}.png'

        plt.savefig(filename)
        plt.close()

    plt.show()


def plot_strain(plot_item, adjust=True, savefig=False, savefig_dir='', time_x2=True):
    plt.close()
    plt.figure(dpi=800)

    time_start = datetime.strptime(plot_item['time_start'], '%H:%M:%S')
    time_end = datetime.strptime(plot_item['time_end'], '%H:%M:%S')
    delta_t = time_end - time_start

    if time_x2:
        time_end = time_start + 2 * delta_t

    time_axis = linspace(
        0,
        delta_t.seconds,
        len(plot_item['read_full'])
    )

    plot_item['strain_read'] = transform_to_strain(array(plot_item['read_full']))

    if adjust:
        load_axis = plot_item['strain_read']
        load_hline = round(transform_to_strain(plot_item['read_load']), 4)
        load_unit = ''
        plt.ylabel('Deformação [$\mu$m]')
        filecomp = ''
    else:
        load_axis = plot_item['read_full']
        if plot_item['read_load'] >= plot_item['read_offset']:
            load_hline = plot_item['read_load']
        else:
            load_hline = plot_item['read_offset']
        load_unit = ''
        plt.ylabel('load value [ADC units]')
        filecomp = '_ADCunits'

    if adjust:
        plt.plot(time_axis, load_axis, color=colors[plot_item['weight_class'].split('c_')[-1].split('r_')[-1]])

    else:
        plt.plot(time_axis, load_axis, color=colors[plot_item['weight_class'].split('c_')[-1].split('r_')[-1]])

    plt.axhline(load_hline, color='orange', linestyle='--')
    plt.xlabel('Tempo [s]')

    plt.legend(
        [
            f'Sinal obtido',
            f'Valor médio: {load_hline} {load_unit}'
        ]
    )

    if savefig:

        if savefig_dir:
            filename = f'{savefig_dir}/{plot_item["file_name"].rstrip(".csv")}{filecomp}.png'
        else:
            try:
                filename = f'{plot_item["file_name"].rstrip(".csv")}{filecomp}.png'
            except:
                filename = f'{plot_item["weight_value"]}_{plot_item["strain_value"]}_{plot_item["time_start"]}{filecomp}.png'
                filename_df = f'{plot_item["weight_value"]}_{plot_item["strain_value"]}_{plot_item["time_start"]}{filecomp}.csv'

        plot_item['strain_read'] = transform_to_strain(array(plot_item['read_full']))
        plt.savefig(filename)
        DataFrame(plot_item['read_full']).to_csv(filename_df)
        plt.close()

    plt.show()


def plot_all_files(save=True, directory='', adjust=False):
    [plot_read(item, adjust=adjust, savefig=save, savefig_dir=directory) for item in data]


def regression_weight_read(adj_points, data_):
    x_values = array([data['weight_value'] for data in data_ if data['weight_class'] in adj_points])
    y_values = array([data['read_load'] for data in data_ if data['weight_class'] in adj_points])
    return linregress(x=x_values, y=y_values)


def regression_read_strain(adj_points, data_):
    x_values = array([data['read_load'] for data in data_ if data['weight_class'] in adj_points])
    y_values = array([data['strain_value'] for data in data_ if data['weight_class'] in adj_points])
    return linregress(x=x_values, y=y_values)


def plot_regression(regression_list, x_points, y_points, color_int=1):
    # plotando os valores
    plt.plot(
        x_points,
        y_points,
        'o',
        label='Pontos originais'
    )
    color_int = color_int
    for regression in regression_list:
        plt.plot(
            x_points,
            regression.intercept + regression.slope * x_points,
            f'C{color_int ** 2}',
            label=f'f(x) = {round(regression.slope, 4)} x + {round(regression.intercept, 4)}'
        )
        color_int += 1


# calibration signals

# plt.figure()
# cal_signal_1 = read_csv('calibration/calibration_weight1.csv')
# plt.ylabel('Valor obtido [bits]')
# plt.plot(cal_signal_1, color='black')
#
# plt.figure()
# cal_signal_2 = read_csv('calibration/calibration_weight4.csv')
# plt.ylabel('Valor obtido [bits]')
# plt.plot(cal_signal_1, color='black')

# cal_nominal_value_1 = round(array(cal_signal_1[300:800]).mean())
# cal_nominal_value_2 = round(array(cal_signal_2[400:900]).mean())

# obtendo dados dos arquivos de resultados
data = data_from_directory_files(dir_, delete_plots=True)

# obtendo dados de cada leitura
df = DataFrame(data).sort_values('read_load').drop(['file_name', 'read_full'], axis=1)

df2 = DataFrame(data).sort_values('read_load').drop(['file_name'], axis=1).sort_values('time_start')

for i in range(0, len(df2), 2):
    data = [
        *df2.iloc[i]['read_full'],
        *df2.iloc[i + 1]['read_full']
    ]
    df = df2.iloc[i]
    df['read_full'] = data

    # DataFrame(df['read_full'])

    plot_strain(df, adjust=True, savefig=True)
