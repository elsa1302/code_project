"""
   Description:
   The purpose of the GUI is to visualize the comparison and categorization of protocols.
   The main functions of GUI are as below:
   Displays the available COM PORTS.
   User can connect to the port .
   User can select the available protocols to establish connectivity between two STM32 boards.
   User can also execute performance analysis through various tests:

  """
import threading
from tkinter import *
import tkinter as tk
import serial.tools.list_ports
import serial
import glob
import sys

serial_data = ''
filter_data = ' '
serial_object = None
serial_write = ''
comPort = 'None'
root = tk.Tk()
root.title("Protocol Analysis")


def serial_ports():
    """ Lists serial port names

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

    result = []
    for port1 in ports:
        try:
            s = serial.Serial(port1)
            result.append(port1)
        except (OSError, serial.SerialException):
            pass
    return result


def get_ports():
    """Function get_ports() returns the list of devices connected through serial port"""
    ports = serial.tools.list_ports.comports()

    return ports


def find_STM(portsFound):
    """ The function returns only the ports where boards are connected and which can be used to establish connection
    for serial communication """
    numConnection = len(portsFound)

    for i in range(0, numConnection):
        Port = foundPorts[i]
        strPort = str(Port)

        if 'STLink' in strPort:
            splitPort = strPort.split(' ')
            comPort = (splitPort[0])
            print(comPort)
    return comPort


def connect():
    """The function initiates connection to UART device with the port fed through the GUI interface and displays the
    same """
    global serial_object
    global serial_data
    global serial_write
    P = port_entry.get()

    try:
        data.insert(END, '\nConnected to \t')
        data.insert(END, str(P))
        t1 = threading.Thread(target=get_data)
        t1.d = True
        t1.start()

    except ValueError:
        print("Enter Port")
        return
    t1 = threading.Thread(target=get_data)
    t1.d = True
    t1.start()


def get_data():
    """This function serves the purpose of collecting data from the serial object and storing
    the filtered data into a global variable.
    The function has been put into a thread since the serial event is a blocking function.
    """
    global serial_object
    global filter_data
    global serial_data
    global serial_write
    try:
        serial_data = serial_object.readline()
        filter_data = serial_data
        print(serial_data.decode())
        serial_write = serial_object.write('E\n'.encode())
    except:
        pass


def update_gui():
    global filter_data
    global update_period
    p1 = protocol_string_var.get()
    t1 = perf_tests_var.get()
    if filter_data:
        if p1 == "Protocol 1" and t1 == "Memory Usage":
            data.insert(END, "The mem is\n")

        elif p1 == "Protocol 1" and t1 == "Execution Time":
            try:
                data.insert(END, "\n")
                data.insert(END, filter_data)
                data.insert(END, "\n")
            except:
                pass

        elif p1 == "Protocol 1" and t1 == "Power Consumption":
            data.insert(END, "The power consumption is\n")
        else:
            pass


def clear():
    """Implements Button Reset functionality. The function clears the changes in GUI and sets the selection to
        default value """
    protocol_string_var.set("NONE")
    perf_tests_var.set("NONE")
    data.delete('1.0', END)


def disconnect():
    """
    This function is for disconnecting from the serial port .

    """
    try:
        data.insert(END, "\nDisconnected from \t")
        data.insert(END, connectPort)
        port_entry.delete(0, END)
        serial_object.close()

    except AttributeError:
        print("Closed without Using it -_-")


if __name__ == "__main__":
    """The main function contains frames which divides the GUI into various frames, each having a feature.
    The main loop consists of all the GUI objects and its placement.
    The Main loop handles all the widget placements.
    
    A label frame for each category generates an object, which is passed over to the respective functions."""

    protocol_label_frame = tk.LabelFrame(root, text="STM 32 Protocols", width=340, height=80)
    protocol_label_frame.grid(row=0, column=0, padx='20', pady='10', sticky='W')

    perf_test_label_frame = tk.LabelFrame(root, text="Performance Test", width=340, height=80)
    perf_test_label_frame.grid(row=1, column=0, padx='20', pady='10', sticky='W')

    dis_label_frame = tk.LabelFrame(root, text="Display ", width=340, height=80)
    dis_label_frame.grid(row=2, column=0, padx='20', pady='0', sticky='W')

    connect_label_frame = tk.LabelFrame(root, text="Connect", width=340, height=80)
    connect_label_frame.grid(row=3, column=0, padx='20', pady='0', sticky='W')

    button_label_frame = tk.LabelFrame(root, text="Execute test", width=340, height=80)
    button_label_frame.grid(row=4, column=0, padx='20', pady='0', sticky='W')

    """Buttons for various functionality : RUN RESET CONNECT DISCONNECT"""

    run = Button(master=button_label_frame, command=update_gui, text="RUN", width=5)
    run.grid(row=3, column=0, padx='20', pady='10', sticky='W')

    reset = Button(master=button_label_frame, command=clear, text="RESET", width=5)
    reset.grid(row=3, column=4, padx='20', pady='10', sticky='W')

    connect = Button(master=connect_label_frame, text="CONNECT", command=connect, width=8)
    connect.grid(row=3, column=1, padx='20', pady='10', sticky='W')

    connect = Button(master=connect_label_frame, text="DISCONNECT", command=disconnect, width=10)
    connect.grid(row=3, column=6, padx='20', pady='10', sticky='W')

    """The entry field allows the user to enter the serial port and to establish connection"""

    port = Label(master=connect_label_frame, text="PORT")
    port.grid(row=3, column=3)
    port_entry = Entry(master=connect_label_frame, width=7)
    port_entry.grid(row=3, column=5)

    """A text widget is included with a scrollbar to display the execution and also to display chosen functionality"""
    scrollbar = Scrollbar(dis_label_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    data = tk.Text(master=dis_label_frame, width='39', height='6')
    data.pack()
    data.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=data.yview)

    """ Option menu for protocols"""

    protocol_string_var = tk.StringVar(protocol_label_frame)  # variable pointing
    protocol_string_var.set("NONE")  # default
    protocol_drop_down = tk.OptionMenu(protocol_label_frame, protocol_string_var,
                                       "Protocol 1", "Protocol 2", "Protocol 3")
    protocol_drop_down.config(width=25)
    protocol_drop_down.place(x=20, y=20)

    """ Option menu for Tests """
    perf_tests_var = tk.StringVar(perf_test_label_frame)
    perf_tests_var.set("NONE")
    perf_tests_drop_down = tk.OptionMenu(perf_test_label_frame, perf_tests_var, "Execution Time", "Memory Usage",
                                         "Power Consumption"
                                         )
    perf_tests_drop_down.pack()
    perf_tests_drop_down.config(width=23)
    perf_tests_drop_down.place(x=20, y=20)

    t2 = threading.Thread(target=update_gui)
    t2.d = True
    t2.start()

    foundPorts = get_ports()
    connectPort = find_STM(foundPorts)

    data.insert(END, "THE AVAILABLE PORTS:\t")
    data.insert(END, serial_ports())

    '''for i in connectPort:
        print(connectPort)'''

    """Window size"""

    width = "500"
    height = "520"
    root.geometry(width + "x" + height)
    root.resizable(0, 0)
    """Title of the GUI"""
    root.title("Protocol Analysis")
    root.title()

    """Position the GUI in the center of the window screen. The height and width is hard coded in main function
       # Gets both half the screen width/height and window width/height
       # Positions the window in the center of the page."""
    position_right = int(root.winfo_screenwidth() / 2 - int(width) / 2)
    position_down = int(root.winfo_screenheight() / 2 - int(height) / 2)
    root.geometry("+{}+{}".format(position_right, position_down))

    if port_entry.get() == '3':
        serial_object = serial.Serial(port='COM3', baudrate=9600, timeout=None)
        serial_object.isOpen()
    else:
        serial_object = serial.Serial(port='COM4', baudrate=9600, timeout=None)
        serial_object.isOpen()

    root.mainloop()
