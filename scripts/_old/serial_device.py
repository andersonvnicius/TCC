"""
functions for using with serial devices

TBD:
- create an object for the serial device and wanted functions
  - plot for number of samples needed
  - plot for sample time needed
  - live plot
"""

import sys
import glob
import serial


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


def device_test(port, baudrate):
    """
    returns the data output of an serial device object,
    if no data is received after 0.5 seconds, returns None
    """
    Device = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)
    Device.flushInput()
    response = Device.readline().decode().rstrip('\r\n').split(' ')
    if len(response) == 1 and len(response[0]) == 0:
        return None
    else:
        return response
