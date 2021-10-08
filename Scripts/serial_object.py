"""
object for using with serial devices
"""


def get_serial_ports():
    """
    lists serial port names
    source: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    import sys
    import glob
    import serial

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

    def read_line(self):
        """returns the last line of data sent by the device"""
        self.serial_object.flushInput()
        data = self.serial_object.readline()
        return data

    def read_samples(self, n_of_samples):
        """returns a number of data lines given a sample size"""
        from time import sleep
        current_sample = 0
        data = []
        while current_sample < n_of_samples:
            data.append(self.read_line())
            current_sample += 1
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


if __name__ == '__main__':
    esp = SerialDevice(get_serial_ports()[0], 115200, 10)
    esp.plot_data(n_of_samples=10, description=('DEBUG', 'REPORT'))
