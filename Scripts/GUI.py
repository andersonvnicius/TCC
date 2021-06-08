"""
script to boot the user interface

TBD:
- GUI for live plot
- user inputs for naming the values received and selecting which of them to plot
- additional windows for previous analysis saving and plotting (idk)
"""


from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import time
import serial_device


def ui_start():
    """starts the GUI"""
    def button_test():
        """Disable input fields, tests selected COM port"""
        # disable entries and buttons
        combo_11.config(state='disabled')
        combo_21.config(state='disabled')
        text_31.config(state='disabled')
        button_0_41.config(state='disable')
        button_1_41.config(state='normal')

        get_data()


    def button_stop():
        """enable input fields, stop the serial monitor"""
        combo_11.config(state='normal')
        combo_21.config(state='normal')
        text_31.config(state='normal')
        button_0_41.config(state='normal')
        button_1_41.config(state='disable')

    def get_data():
        """gets a sample of data from the serial device"""
        result = serial_device.device_test(port=combo_11.get(), baudrate=combo_21.get())

        if result is None:
            text_box_60.config(state='normal')
            text_box_60.insert(END, 'Incompatible device! \n')
            text_box_60.config(state='disabled')
            text_box_60.see('end')
            button_stop()

        else:
            text_box_60.config(state='normal')
            text_box_60.insert(END, 'Entries received: ')
            text_box_60.insert(END, result)
            text_box_60.insert(END, '\n')
            text_box_60.insert(END, 'qty of entries: ')
            text_box_60.insert(END, len(result))
            text_box_60.insert(END, '\n')
            text_box_60.see('end')
            text_box_60.config(state='disabled')

    port_list = serial_device.get_serial_ports()
    baudrate_list = (9600, 14400, 19200, 38400, 57600, 115200)
    refresh_rate = 10

    window = Tk()
    window.title("Serial monitor!")

    label_0 = Label(window, text=" ", font=('Arial', 12))
    label_0.grid(row=0, columnspan=2)

    label_10 = Label(window, text="Controller port: ", font=('Arial', 11))
    label_10.grid(row=10, column=0)

    combo_11 = Combobox(window)
    combo_11['values'] = port_list
    combo_11.current(0)
    combo_11.grid(row=11, column=0, columnspan=2)

    selected_port = combo_11.current()

    label_20 = Label(window, text="Baudrate: ", font=('Arial', 11))
    label_20.grid(row=20, column=0)

    combo_21 = Combobox(window)
    combo_21['values'] = baudrate_list
    combo_21.current(baudrate_list.index(115200))
    combo_21.grid(row=21, column=0, columnspan=2)

    label_30 = Label(window, text="Refresh rate [ms]: ", font=('Arial', 11))
    label_30.grid(row=30, column=0)

    text_31 = Entry(window)
    text_31.insert(END, 10)
    text_31.grid(row=31, column=0, columnspan=2)

    # find another way to add space!
    label_40 = Label(window, text=" ", font=('Arial', 5))
    label_40.grid(row=40, column=0)

    button_0_41 = Button(window, text='lock', command=button_test)
    button_0_41.grid(row=41, column=0)

    button_1_41 = Button(window, text='unlock', command=button_stop, state='disabled')
    button_1_41.grid(row=41, column=1)

    label_50 = Label(window, text="Serial monitor", font=('Arial', 10))
    label_50.grid(row=50, columnspan=2)

    text_box_60 = scrolledtext.ScrolledText(window, font=('Arial', 10), width=50, height=10, state='disabled')
    text_box_60.grid(row=60, column=0, columnspan=2)

    button_70 = Button(window, text='close!', command=window.destroy)
    button_70.grid(row=70, columnspan=2)

    window.mainloop()


if __name__ == '__main__':
    ui_start()
