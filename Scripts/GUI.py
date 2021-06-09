"""
script to boot the user interface

TBD:
- !!needs to return an error if wrong baudrate is selected!!
- GUI for live plot
- user inputs for naming the values received and selecting which of them to plot
- additional windows for previous analysis saving and plotting (idk)

"""

from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import serial_object


def ui_start():
    """starts the GUI"""

    def button_test():
        """Disable input fields, tests selected COM port"""
        # disable entries and buttons
        cmb_port.config(state='disabled')
        cmb_baudrate.config(state='disabled')
        txt_connection.config(state='disabled')
        btn_connect.config(state='disable')
        btn_disconnect.config(state='normal')

        SerialDevice = serial_object.SerialDevice(port=cmb_port.get(), baudrate=cmb_baudrate.get())
        check_device_compatibility(SerialDevice)

        return SerialDevice

    def button_stop():
        """enable input fields, stop the serial monitor"""
        cmb_port.config(state='normal')
        cmb_baudrate.config(state='normal')
        txt_connection.config(state='normal')
        btn_connect.config(state='normal')
        btn_disconnect.config(state='disable')
        btn_monitor.config(state='disabled')
        btn_plot.config(state='disabled')

    def check_device_compatibility(Device):
        """gets a sample of data from the serial device"""

        result = Device.read_line().decode()

        if len(result) == 0:
            serial_monitor.config(state='normal')
            serial_monitor.insert(END, 'Incompatible device! \n\n')
            serial_monitor.config(state='disabled')
            serial_monitor.see('end')
            button_stop()

        else:
            serial_monitor.config(state='normal')
            serial_monitor.insert(END, 'Device: ' + cmb_port.get() + '\n')
            serial_monitor.insert(END, 'Entries received: ' + str(result.rstrip('\r\n')) + '\n')
            serial_monitor.insert(END, 'qty of entries: ' + str(len(result.rstrip('\r\n').split(' '))) + '\n\n')
            serial_monitor.see('end')
            serial_monitor.config(state='disabled')
            btn_plot.config(state='normal')
            btn_monitor.config(state='normal')

    port_list = serial_object.get_serial_ports()
    baudrate_list = (9600, 14400, 19200, 38400, 57600, 115200)
    refresh_rate = 10

    root = Tk()
    root.title("Telemetry center (alpha 0.0.1)")

    # CONNECTION SET UP FRAME

    frame_connection = LabelFrame(root, text="Connection setup")
    frame_connection.pack(padx=15, pady=15)

    lbl_port = Label(frame_connection, text="Controller port: ", font=('Arial', 11))
    lbl_port.grid(row=10, column=0)
    cmb_port = Combobox(frame_connection)
    cmb_port['values'] = port_list
    cmb_port.current(0)
    cmb_port.grid(row=11, column=0, columnspan=2)

    lbl_baudrate = Label(frame_connection, text="Baudrate: ", font=('Arial', 11))
    lbl_baudrate.grid(row=20, column=0)
    cmb_baudrate = Combobox(frame_connection)
    cmb_baudrate['values'] = baudrate_list
    cmb_baudrate.current(baudrate_list.index(115200))
    cmb_baudrate.grid(row=21, column=0, columnspan=2)

    lbl_connection = Label(frame_connection, text="Refresh rate [ms]: ", font=('Arial', 11))
    lbl_connection.grid(row=30, column=0, padx=10)
    txt_connection = Entry(frame_connection)
    txt_connection.insert(END, 10)
    txt_connection.grid(row=31, column=0, columnspan=2)

    btn_connect = Button(frame_connection, text='Connect', command=button_test)
    btn_connect.grid(row=41, column=0, pady=10)
    btn_disconnect = Button(frame_connection, text='Disconnect', command=button_stop, state='disabled')
    btn_disconnect.grid(row=41, column=1, padx=20)

    # SERIAL MONITOR FRAME

    frame_monitor = LabelFrame(root, text="Serial monitor")
    frame_monitor.pack(padx=15, pady=15)

    serial_monitor = scrolledtext.ScrolledText(frame_monitor, font=('Arial', 10), width=50, height=10, state='disabled')
    serial_monitor.grid(row=10, column=0, columnspan=2, padx=15, pady=5)

    btn_monitor = Button(frame_monitor, text='monitor', state='disabled')
    btn_monitor.grid(row=20, column=0)
    btn_plot = Button(frame_monitor, text='plot', state='disabled')
    btn_plot.grid(row=20, column=1, pady=5)

    # KILL PROCESS BUTTON

    frame_root = Frame(root)
    frame_root.pack()
    btn_kill = Button(frame_root, text='close!', command=root.destroy)
    btn_kill.grid(row=100, pady=10)

    root.mainloop()


if __name__ == '__main__':
    ui_start()
