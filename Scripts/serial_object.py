"""
object for using with serial devices
"""


class Device():
    """
    Creates a serial connection device object
    """
    from serial import Serial

    def __init__(self, port, baudrate):
        self.serial_object = self.Serial(port=port, baudrate=baudrate, timeout=1)

    def read_line(self):
        """returns the last line of data sent by the device"""
        self.serial_object.flushInput()
        data = self.serial_object.readline().decode().rstrip('\r\n').split(' ')
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
