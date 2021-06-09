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
        self.delay_time = float(delay_time)*1e-3

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

    def plot_data(self, n_of_samples=False):
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
        import matplotlib.pyplot as plt
        import numpy as np

        self.serial_object.close()
        self.serial_object.open()
        self.serial_object.flushInput()
        self.serial_object.readline()

        data = self.read_line().decode().rstrip('\r\n').split(' ')

        # LIVE-PLOT SETUP
        plt.ion()
        n_of_plots = len(data)
        fig, axs = plt.subplots(n_of_plots)
        fig.suptitle('Sensor readings')

        # empty variables
        data = np.zeros((1, n_of_plots))

        # indexes
        error_qnt = 0
        n_of_iterations = 0
        current_sample = 0

        while True:
            plt.cla()
            read_float = []
            n_of_iterations += 1
            print(current_sample)

            try:
                self.serial_object.flushInput()
                read = self.serial_object.readline().decode().rstrip('\r\n').split(' ')

                for value in read:
                    read_float.append(float(value))

                data = np.append(data, [read_float], axis=0)

                for j in range(0, n_of_plots):
                    axs[j].cla()
                    axs[j].plot(data[:, j][-5:], ('C' + str(j)))

                plt.pause(self.delay_time)

                if isinstance(n_of_samples, bool):
                    pass

                else:
                    if current_sample > n_of_samples - 2:
                        break
                    current_sample += 1

            except IndexError:
                error_qnt += 1
                print('Index Error rate', round(error_qnt / n_of_iterations, 2))
