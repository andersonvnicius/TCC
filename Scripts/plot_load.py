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
import pandas as pd
from time import time


time_analysis = 5
load_offset = 22
analysis_delay_time = 10E-3

arduino_port = '/dev/ttyUSB0'
arduino_baudrate = 115200
Arduino = serial.Serial(port=arduino_port, baudrate=arduino_baudrate)
Arduino.close()
Arduino.open()
Arduino.flushInput()
Arduino.readline()

plt.ion()
fig, axs = plt.subplots()
fig.suptitle('Sensor readings')

data = []
error_qnt = 0

start = time()
print('analysis start')

try:
    while True:
        plt.cla()

        try:
            Arduino.flushInput()
            read = int(Arduino.readline().decode().rstrip('\r\n').split(' ')[0])
            data.append(read - load_offset)

            axs.cla()
            axs.plot(data[-25:], ('C' + str(0)))

            plt.pause(analysis_delay_time)
            end = time()
            if end-start > time_analysis:
                print('analysis end')
                break

        except IndexError:
            error_qnt += 1

        except ValueError:
            error_qnt += 1

except KeyboardInterrupt:
    print('keyboard interrupt!')
    data = data[:-1]

dataframe = pd.DataFrame(data)
