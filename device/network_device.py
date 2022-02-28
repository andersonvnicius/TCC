from datetime import datetime
from time import sleep

from matplotlib import pyplot as plt
from numpy import array, append
from requests import post


class NetworkDevice:
    """
    Creates a local network connection device object
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

        self.b = w2 / ((r2 / r1) * (w1 - 1) + 1)
        self.a = (w1 - self.b) / r1

    def read_samples(self, n_of_samples: int, plot: bool = False, calibrated: bool = False):
        """returns a number of data lines given a sample size"""

        if not plot:
            value_list = array([])
            while len(value_list) < n_of_samples:
                value_list = append(
                    value_list,
                    int(self.read_line(calibrated=calibrated))
                )
                sleep(self.delay_time)
                # print(f"sample: {len(value_list)}, value: {int(value_list[-1])}")

        else:
            value_list = self.plot_data(n_of_samples=n_of_samples, calibrated=calibrated)

        return value_list

    def plot_data(self, n_of_samples, calibrated: bool = False):
        """plot the numerical data received"""
        value_list = array([])

        plt.ion()
        fig, axs = plt.subplots(1)
        fig.suptitle('Readings')

        while len(value_list) < n_of_samples:
            try:
                value_list = append(value_list, int(self.read_line(calibrated=calibrated)))

                axs.cla()
                axs.plot(value_list[-25:])

                plt.pause(self.delay_time)

            except:
                print("error!")

        plt.close()

        return value_list


if __name__ == '__main__':
    # TESTING wireless device object
    device_ip = '192.168.1.4'
    read_rate = 100e-3

    device = NetworkDevice(
        ip=device_ip,
        delay_time=read_rate
    )

    # device calibration
    device.calibrate_offset()

    from pandas import read_csv, DataFrame

    device.calibrate_readings(
        {'nominal_value': 16, 'signal': array(read_csv('../results/read_1.csv')[:-100]['read'])},
        {'nominal_value': 59, 'signal': array(read_csv('../results/read_2.csv')[:-100]['read'])}
    )

    # device testing
    read = device.read_samples(n_of_samples=300, plot=True, calibrated=True)
    DataFrame(read, columns=['read']).to_csv(f'../results/test_{datetime.now()}.csv')
