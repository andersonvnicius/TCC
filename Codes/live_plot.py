"""
read and plot any numerical serial received data as long it is in the following format:
b'<data_1> <data_2> <data_3> ... <data_n>/r/n'

TBD:
- write about:
  - input variables:
   - n_of_samples
   - name_of_values_received
   - name_of_values_to_plot
   - microcontroller port
   - microcontroller baudrate
   - microcontroller refresh_rate (maybe get automatically from the arduino!??)
  - outputs:
   - pandas df with read values @ end of the analysis
   - live plot to the user
"""

import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

# User inputs and settings
n_of_samples = False  # set to false for a non end analysis
values_to_plot = ('Load', 'Ax', 'Gx')  # any order will work as long as the values contains in variable values_received
values_received = ('Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz', 'Load')

arduino_port = '/dev/ttyUSB0'
arduino_baudrate = 115200
arduino_delay_time = 10E-3

output_file_path = '/home/and1/TCC/Reports'

# Save start time
datetime_start = datetime.now().strftime('%Y_%m_%d_%H:%M:%S')

# arduino port
Arduino = serial.Serial(port=arduino_port, baudrate=arduino_baudrate)
Arduino.close()
Arduino.open()
Arduino.flushInput()
Arduino.readline()

# plot setup
plt.ion()
values_to_plot_index = [values_received.index(item) for item in values_to_plot]
n_of_plots = len(values_to_plot_index)
fig, axs = plt.subplots(n_of_plots)
fig.suptitle('Sensor readings')

# empty variables
data = np.zeros((1, n_of_plots))

# indexes
error_qnt = 0
current_sample = 0
n_of_iterations = 0


try:
    while True:
        plt.cla()
        read_float = []
        n_of_iterations += 1

        try:
            Arduino.flushInput()
            read = Arduino.readline().decode().rstrip('\r\n').split(' ')

            for index in values_to_plot_index:
                read_float.append(float(read[index]))

            data = np.append(data, [read_float], axis=0)

            for j in range(0, n_of_plots):
                axs[j].cla()
                axs[j].plot(data[:, j][-5:], ('C' + str(j)))

            plt.pause(arduino_delay_time)

            if isinstance(n_of_samples, bool):
                pass

            else:
                if current_sample > n_of_samples:
                    break
                current_sample += 1

        except IndexError:
            error_qnt += 1
            print('Index Error ', round(error_qnt / n_of_iterations, 2))
            # print(read_0)

except KeyboardInterrupt:
    print('keyboard interrupt!')
    data = data[:-1]


data[0, 0] = error_qnt / n_of_iterations
datetime_end = datetime.now().strftime('%H:%M:%S')
dataframe = pd.DataFrame(data, columns=values_to_plot)
dataframe.to_csv(('Reports/results_' + datetime_start + '_' + datetime_end + '.csv'))

print('save done!')
