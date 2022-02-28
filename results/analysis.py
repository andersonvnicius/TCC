"""used to analyse my results"""

import os
from os.path import isfile, join
from numpy import array, average, linspace
from scipy.stats import linregress
from pandas import read_csv, DataFrame
from datetime import datetime
import matplotlib.pyplot as plt


def data_from_directory_files(directory, delete_plots=False):
    """
    extracts data from files in a directory
    """
    files = [f for f in os.listdir(directory) if isfile(join(directory, f)) and '.csv' in f]
    result_strings = [file.split('Report_')[1].split('.csv')[0] for file in files]  # load, start time, end time
    times = [time_format(time_string[-17:]) for time_string in result_strings]
    loads = [load_string[:-18].split('_')[-1] for load_string in result_strings]
    result = array([loads, times, files]).T

    if delete_plots:
        files_to_delete = [f for f in os.listdir(directory) if isfile(join(directory, f)) and '.png' in f]
        if files_to_delete:
            print(f'{files_to_delete} removed')

    data_ = []

    for item in result:
        df = list(read_csv(f'{directory}/{item[2]}').get('0'))
        weight_value = get_weight_value(item[0])
        data_.append(
            {
                'weight_class': item[0],
                'weight_value': weight_value,
                'strain_value': get_strain_value(weight_value) * 1e6,
                'file_name': item[2],
                'time_start': item[1][0],
                'time_end': item[1][1],
                'read_offset': round(average(df[:100])),
                'read_load': round(average(df[1000:3000])),
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
        '0': 0,
        'fuse_and_nut': weights_kg['fuse'] + weights_kg['nut'],
        'only_fuse': weights_kg['fuse'],
        '1': weights_kg['weight_1'] + weights_kg['fuse'] + weights_kg['nut'],
        '2': weights_kg['weight_2'] + weights_kg['fuse'] + weights_kg['nut'],
        '3': weights_kg['weight_3'] + weights_kg['fuse'] + weights_kg['nut'],
        'a': weights_kg['weight_a'] + weights_kg['fuse'] + weights_kg['nut'],
        'b': weights_kg['weight_b'] + weights_kg['fuse'] + weights_kg['nut']
    }

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

    colors = {
        '1': 'red',
        '2': 'green',
        '3': 'blue',
        'a': 'yellow',
        'b': 'cyan',
        '0': 'black',
    }

    if adjust:
        load_axis = read_adjust(plot_item)
        load_hline = plot_item['weight_value']
        load_unit = 'kg'
        plt.ylabel('load value [kg]')
        filecomp = ''
    else:
        load_axis = plot_item['read_full']
        load_hline = plot_item['read_load']
        load_unit = ''
        plt.ylabel('load value [ADC units]')
        filecomp = '_ADCunits'

    plt.plot(time_axis, load_axis, color=colors[plot_item['weight_class']])
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


# diretorio dos arquivos pra analise
dir_ = 'sep_24_1'

# obtendo dados dos arquivos de resultados
data = data_from_directory_files(dir_, delete_plots=True)

# plot de cada analise
# plot_all_files(save=True, directory=dir_, adjust=True)

# obtendo dados de cada leitura
df = DataFrame(data).sort_values('read_load').drop(['file_name', 'read_full'], axis=1)

# regressoes entre peso e valor obtido pelo ADC
plt.figure()
plot_regression(
    regression_list=[
        regression_weight_read(  # regressão com 2 pontos
            adj_points=['1', '3'],
            data_=data
        ),
        regression_weight_read(  # regressão com 3 pontos
            adj_points=['1', 'a', '3'],
            data_=data
        ),
        regression_weight_read(  # regressão com todos os pontos
            adj_points=['0', '1', '2', 'a', 'b', '3'],
            data_=data
        )
    ],
    x_points=array(df['weight_value']),
    y_points=array(df['read_load']),
    color_int=1
)
plt.title('Regressão entre peso e valor no ADC')
plt.xlabel('Massa aplicada [kg]')
plt.ylabel('Leitura do amplificador analógico digital')
plt.legend()
plt.show()
plt.savefig(f'{dir_}_weight.png')
plt.close()

# regressoes entre valor do ADC e deformacao
regression_list = [
    regression_read_strain(  # regressão com 2 pontos
        adj_points=['1', '3'],
        data_=data
    ),
    regression_read_strain(  # regressão com 3 pontos
        adj_points=['1', 'a', '3'],
        data_=data
    ),
    regression_read_strain(  # regressão com todos os pontos
        adj_points=['0', '1', '2', 'a', 'b', '3'],
        data_=data
    )
]

i = 1
for regression in regression_list:
    df[f'linreg_{i}'] = regression.slope * df['read_load'] + regression.intercept
    i += 1

# df.to_csv('Results/sep_24_1_results.csv', index=None)

plt.figure()
plot_regression(
    regression_list=regression_list,
    x_points=array(df['read_load']),
    y_points=array(df['strain_value']),
    color_int=1
)
plt.title('Regressão entre valor obtido e deformação')
plt.xlabel('Valor obtido pelo amplificador analógico digital')
plt.ylabel('Deformação no strain gauge [um]')
plt.legend()
plt.show()
# plt.savefig(f'{dir_}_deformation.png')
plt.close()
