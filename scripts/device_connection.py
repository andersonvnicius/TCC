"""
serial_object.py

This file is used for the creation of objects associated with connection and data gathering with serial devices.
"""

# import os
# import os.path
import sys
import glob

import serial
from requests import post

from numpy import array, append
from pandas import DataFrame

import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime


def get_serial_ports():
    """
    lists serial port names
    source: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    port_list = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            port_list.append(port)
        except (OSError, serial.SerialException):
            pass
    return port_list


class SerialDevice:
    """
    Creates a serial connection device object
    """
    from serial import Serial

    def __init__(self, port, baudrate, delay_time):
        self.serial_object = self.Serial(port=port, baudrate=baudrate, timeout=1)
        self.delay_time = float(delay_time) * 1e-3

    def read_samples(self, n_of_samples):
        """returns a number of data lines given a sample size"""
        current_sample = 0
        data = []
        while current_sample < n_of_samples:
            data.append(self.read_line())
            current_sample += 1
        return data

    def read_line(self):
        """returns the last line of data sent by the device"""
        self.serial_object.flushInput()
        data = self.serial_object.readline()
        return data

    def plot_data(self, n_of_samples=False, description=(), offset=2550, plot=False):
        """
        read and plot any numerical serial received data as long it is in the following format:
        b'<data_1> <data_2> <data_3> ... <data_n>/r/n'

        TBD:
        - write about:
          -- input variables:
           - n_of_samples
          -- outputs:
           - live plot to the user
        """
        from matplotlib.pyplot import ion, subplots, cla, pause
        from numpy import zeros, append
        from pandas import DataFrame
        from datetime import datetime

        self.serial_object.close()
        self.serial_object.open()
        self.serial_object.flushInput()
        self.serial_object.readline()

        data = self.read_line().decode().rstrip('\r\n').split(' ')
        n_of_plots = len(data)

        # LIVE-PLOT SETUP
        if plot:
            ion()
            fig, axs = subplots(n_of_plots)
            fig.suptitle('Sensor readings')

        # empty variables
        if n_of_plots == 1:
            data = []
        else:
            data = zeros((1, n_of_plots))

        # indexes
        error_qnt = 0
        n_of_iterations = 0
        current_sample = 0

        datetime_start = datetime.now().strftime('%H_%M_%S')

        if n_of_plots == 1:

            while True:
                if plot:
                    cla()

                try:
                    self.serial_object.flushInput()
                    read = int(self.serial_object.readline().decode().rstrip('\r\n').split(' ')[0]) - offset
                    data.append(read)

                    if plot:
                        axs.cla()
                        axs.plot(data[-5:], ('C' + str(0)))
                    else:
                        print(data[-1])

                    pause(self.delay_time)

                    if not n_of_samples:
                        pass

                    else:
                        if current_sample == n_of_samples:
                            break
                        current_sample += 1

                except IndexError:
                    error_qnt += 1

                except ValueError:
                    error_qnt += 1

        else:

            while True:
                cla()
                n_of_iterations += 1
                read_float = []

                try:
                    self.serial_object.flushInput()
                    read = self.serial_object.readline().decode().rstrip('\r\n').split(' ')

                    for value in read:
                        read_float.append(float(value))

                    data = append(data, [read_float], axis=0)

                    for j in range(0, n_of_plots):
                        axs[j].cla()
                        axs[j].plot(data[:, j][-5:], ('C' + str(j)))

                    pause(self.delay_time)

                    if not n_of_samples:
                        pass

                    else:
                        if current_sample == n_of_samples:
                            break
                        current_sample += 1

                except IndexError:
                    error_qnt += 1
                    print('Index Error rate', round(error_qnt / n_of_iterations, 2))

        datetime_end = datetime.now().strftime('%H_%M_%S')
        filename = f'Report_{"_".join(description)}_{datetime_start}_{datetime_end}.csv'
        DataFrame(data).to_csv(f'{filename}')

        return


class WirelessDevice:
    """
    Creates a serial connection device object
    """

    def __init__(self, ip, delay_time):
        self.url = f'http://{ip}/read'
        self.delay_time = delay_time
        self.offset = 0
        self.a = 1
        self.b = 0

    def read_line(self, calibrated=False):
        """returns the last line of data sent by the device"""
        read = int(post(self.url).text) - self.offset
        if calibrated:
            return self.a * read + self.b
        else:
            return read

    def calibrate_offset(self):
        """sets the offset value for the device data gathering"""
        self.offset = 0
        self.offset = round(self.read_samples(n_of_samples=40).mean())

    def calibrate_readings(self, calibration_dict_1: dict, calibration_dict_2: dict):
        """calibrate the device readings"""
        w1 = calibration_dict_1['nominal_value']
        w2 = calibration_dict_2['nominal_value']
        r1 = round(calibration_dict_1['signal'].mean())
        r2 = round(calibration_dict_1['signal'].mean())

        self.b = round(r2 / ((w2 / w1) * (r1 - 1) + 1))
        self.a = round((r1 - self.b) / w1)

    def read_samples(self, n_of_samples: int, plot: bool = False, calibrated: bool = False):
        """returns a number of data lines given a sample size"""

        if not plot:
            value_list = array([])
            while len(value_list) < n_of_samples:
                value_list = append(
                    value_list,
                    int(device.read_line(calibrated=calibrated))
                )
                sleep(self.delay_time)
                # print(f"sample: {len(value_list)}, value: {int(value_list[-1])}")

        else:
            value_list = self.plot_data(n_of_samples=n_of_samples)

        return value_list

    def plot_data(self, n_of_samples):
        """plot the numerical data received"""
        value_list = array([])

        plt.ion()
        fig, axs = plt.subplots(1)
        fig.suptitle('Readings')

        while len(value_list) < n_of_samples:
            try:
                value_list = append(value_list, int(device.read_line()))

                axs.cla()
                axs.plot(value_list[-100:])

                plt.pause(self.delay_time)

            except:
                print("error!")

        plt.close()

        return value_list


if __name__ == '__main__':

    # TESTING wireless device object
    device_ip = '192.168.1.4'
    delay_time = 100e-3

    device = WirelessDevice(
        ip=device_ip,
        delay_time=delay_time
    )

    # device calibration
    device.calibrate_offset()

    from pandas import read_csv
    device.calibrate_readings(
        calibration_dict_1={
            'nominal_value': 16,
            'signal': array(read_csv('../results/read_eraser.csv')[:-100]['read'])
        },
        cal_read_2={
            'nominal_value': 59,
            'signal': array(read_csv('../results/read_airpod.csv')[:-100]['read'])
        }
    )

    # device testing
    read = device.read_samples(n_of_samples=100, plot=True)
    DataFrame(read).to_csv(f'../results/test_{datetime.now()}.csv')
