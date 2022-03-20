"""
script to boot the user interface

TBD:
- !!needs to return an error if wrong baudrate is selected!!
- GUI for live plot
- user inputs for naming the values received and selecting which of them to plot
- additional windows for previous analysis saving and plotting (idk)

"""

from datetime import datetime
from time import sleep

from tkinter import *  # sudo apt-get install python3-tk
from tkinter import scrolledtext
from tkinter.ttk import *

from pandas import DataFrame

from device.network_device import NetworkDevice


def gui_start():
    """starts the GUI"""

    def button_connect():
        """connects device in the selected ip address"""
        txt_address.config(state='disabled')
        txt_read_delay.config(state='disabled')
        btn_connect.config(state='disable')
        btn_disconnect.config(state='normal')

        nonlocal wireless_device
        wireless_device = NetworkDevice(
            ip=txt_address.get(),
            delay_time=int(txt_read_delay.get())*1E-3
        )
        check_device_compatibility(wireless_device)

    def button_stop():
        """close connection with device"""
        txt_address.config(state='normal')
        txt_read_delay.config(state='normal')
        btn_connect.config(state='normal')
        btn_disconnect.config(state='disable')
        btn_run.config(state='disabled')

    def button_calibration_lock():
        """calibrates the device"""
        from numpy import array
        btn_calibrate_lock.config(state='disable')
        txt_r2.config(state='disabled')
        txt_r1.config(state='disabled')
        txt_v1.config(state='disabled')
        txt_v2.config(state='disabled')
        wireless_device.calibrate_readings(
            {'nominal_value': int(txt_v1.get()), 'signal': array([int(txt_r1.get())])},
            {'nominal_value': int(txt_v2.get()), 'signal': array([int(txt_r2.get())])}
        )
        serial_monitor.config(state='normal')
        serial_monitor.insert(END, f'device calibrated!! \n')
        serial_monitor.insert(END, f'factor a: {wireless_device.a} \n')
        serial_monitor.insert(END, f'factor b: {wireless_device.b} \n')
        serial_monitor.config(state='disabled')
        txt_v1.config(state='disabled')
        txt_v2.config(state='disabled')
        txt_r1.config(state='disabled')
        txt_r2.config(state='disabled')
        btn_calibrate_unlock.config(state='normal')

    def button_calibration_unlock():
        """resets device calibration"""
        wireless_device.a = 0
        wireless_device.b = 0
        btn_calibrate_lock.config(state='normal')
        txt_v1.config(state='normal')
        txt_v2.config(state='normal')
        txt_r1.config(state='normal')
        txt_r2.config(state='normal')
        btn_calibrate_unlock.config(state='disabled')

    def check_device_compatibility(Device):
        """gets a sample of data from the ip address"""

        serial_monitor.config(state='normal')
        serial_monitor.insert(END, f'connecting to device in address:\n{device_ip}...')

        try:
            result = Device.read_line()
            serial_monitor.insert(END, f'success!! \n')
            serial_monitor.insert(END, f'value: {result} \n')
            serial_monitor.insert(END, f'calibrating offset...')
            wireless_device.calibrate_offset()
            serial_monitor.insert(END, f'done!\n')
            serial_monitor.see('end')
            serial_monitor.config(state='disabled')
            btn_run.config(state='normal')
            btn_calibrate_lock.config(state='normal')
            txt_v1.config(state='normal')
            txt_v2.config(state='normal')
            txt_r1.config(state='normal')
            txt_r2.config(state='normal')

        except:
            serial_monitor.config(state='normal')
            serial_monitor.insert(END, 'Incompatible device! \n\n')
            serial_monitor.config(state='disabled')
            serial_monitor.see('end')
            button_stop()

    def run_experiment():
        """plots stuff"""

        n_of_samples = int(txt_n_samples.get()) * int(txt_read_delay.get())*1e-3

        DataFrame(
            wireless_device.read_samples(
                n_of_samples=n_of_samples,
                plot=True,
                calibrated=True
            )
        ).to_csv(f"results/{datetime.now()}_{txt_report_name.get()}")

    wireless_device = None

    # initial device port and read rate data
    device_ip = '192.168.1.4'
    read_delay = 100

    # initial device calibration
    v1 = 16         # nominal value of the first data point
    v2 = 59         # nominal value of the second data point
    r1 = 24464      # read value of the first data point
    r2 = 96689      # read value of the first data point

    # starting the gui object
    root = Tk()
    root.title("Telemetry center (alpha 0.1.0)")

    # connection setup frame
    frame_connection = LabelFrame(root, text="Connection setup")
    frame_connection.pack(padx=10, pady=5)

    lbl_address = Label(frame_connection, text="Device address: ", font=('Arial', 11))
    lbl_address.grid(row=10, column=0)
    txt_address = Entry(frame_connection)
    txt_address.insert(END, device_ip)
    txt_address.grid(row=11, column=0, columnspan=2)

    lbl_read_delay = Label(frame_connection, text="Sampling rate[ms]: ", font=('Arial', 11))
    lbl_read_delay.grid(row=30, column=0, padx=10)
    txt_read_delay = Entry(frame_connection)
    txt_read_delay.insert(END, read_delay)
    txt_read_delay.grid(row=31, column=0, columnspan=2)

    btn_connect = Button(frame_connection, text='Connect', command=button_connect)
    btn_connect.grid(row=41, column=0, pady=10)
    btn_disconnect = Button(frame_connection, text='Disconnect', command=button_stop, state='disabled')
    btn_disconnect.grid(row=41, column=1, padx=20)

    # calibration setup frame
    frame_calibration = LabelFrame(root, text="Device Calibration")
    frame_calibration.pack(padx=10, pady=5)


    lbl_v1 = Label(frame_calibration, text="Nominal value 1: ", font=('Arial', 11))
    lbl_v1.grid(row=50, column=0)
    txt_v1 = Entry(frame_calibration)
    txt_v1.insert(END, v1)
    txt_v1.config(state='disabled')
    txt_v1.grid(row=51, column=0, columnspan=1)

    lbl_v2 = Label(frame_calibration, text="Nominal value 2: ", font=('Arial', 11))
    lbl_v2.grid(row=60, column=0, padx=10)
    txt_v2 = Entry(frame_calibration)
    txt_v2.insert(END, v2)
    txt_v2.config(state='disabled')
    txt_v2.grid(row=61, column=0, columnspan=1)

    lbl_r1 = Label(frame_calibration, text="Read average 1: ", font=('Arial', 11))
    lbl_r1.grid(row=50, column=1)
    txt_r1 = Entry(frame_calibration)
    txt_r1.insert(END, r1)
    txt_r1.config(state='disabled')
    txt_r1.grid(row=51, column=1, columnspan=1)

    lbl_r2 = Label(frame_calibration, text="Read average 2: ", font=('Arial', 11))
    lbl_r2.grid(row=60, column=1)
    txt_r2 = Entry(frame_calibration)
    txt_r2.insert(END, r2)
    txt_r2.config(state='disabled')
    txt_r2.grid(row=61, column=1, columnspan=1)

    btn_calibrate_lock = Button(frame_calibration, text='Calibrate', command=button_calibration_lock, state='disabled')
    btn_calibrate_lock.grid(row=71, column=0, pady=10)

    btn_calibrate_unlock = Button(frame_calibration, text='Reset', command=button_calibration_unlock, state='disabled')
    btn_calibrate_unlock.grid(row=71, column=1, pady=10)

    # experiment frame
    frame_monitor = LabelFrame(root, text="Serial monitor")
    frame_monitor.pack(padx=10, pady=5)

    serial_monitor = scrolledtext.ScrolledText(frame_monitor, font=('Arial', 10), width=32, height=10, state='disabled')
    serial_monitor.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

    lbl_report_name = Label(frame_monitor, text="Report name: ", font=('Arial', 11))
    lbl_report_name.grid(row=20, column=0, padx=0)
    txt_report_name = Entry(frame_monitor)
    txt_report_name.insert(END, '')
    txt_report_name.grid(row=21, column=0, columnspan=2)

    lbl_n_samples = Label(frame_monitor, text="Experiment duration [s]: ", font=('Arial', 11))
    lbl_n_samples.grid(row=30, column=0, padx=0)
    txt_n_samples = Entry(frame_monitor)
    txt_n_samples.insert(END, 30)
    txt_n_samples.grid(row=31, column=0, columnspan=2)

    btn_run = Button(frame_monitor, text='run', command=run_experiment, state='disabled')
    btn_run.grid(row=31, column=1, pady=10)

    # kill process button
    frame_root = Frame(root)
    frame_root.pack()
    btn_kill = Button(frame_root, text='Exit', command=root.destroy)
    btn_kill.grid(row=100, pady=5)

    # keep gui running in loop
    root.mainloop()


if __name__ == '__main__':
    gui_start()
