from tkinter import *
import tkinter as tk
import serial

import Execution_stm as gfe


class GuiWindow:
    """The Class GUIWindow includes all the front end features of the GUI """

    def __init__(self, root, width, height, stm_protocols, perf_tests, title):
        self.root = root
        self.width = width
        self.height = height
        self.stm_protocols = stm_protocols
        self.perf_tests = perf_tests
        self.title = title
        self.protocol_string_var = ""
        self.graph_var = 0
        self.data_var = 1
        self.perf_tests_string_var = ""

    def gui_features(self):
        """Entry point to the class: GUIWindow(). All functions are invoked from here."""
        self.root.geometry(self.width + "x" + self.height)
        self.root.resizable(0, 0)
        self.root.title(self.title)
        self.gui_win_position()
        self.gui_label_frame()

    def gui_win_position(self):
        """Position the GUI in the center of the window screen. The height and width is hard coded in main function"""
        # Gets both half the screen width/height and window width/height
        position_right = int(self.root.winfo_screenwidth() / 2 - int(self.width) / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - int(self.height) / 2)
        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(position_right, position_down))

    def gui_protocol_dropdown(self, protocol_label_frame):
        self.protocol_string_var = tk.StringVar(protocol_label_frame)  # variable pointing
        self.protocol_string_var.set("none")  # default
        protocol_drop_down = tk.OptionMenu(protocol_label_frame, self.protocol_string_var,
                                           *self.stm_protocols)
        protocol_drop_down.config(width=25)
        protocol_drop_down.place(x=20, y=20)

    def gui_perf_test_dropdown(self, perf_test_label_frame):
        self.perf_tests_string_var = tk.StringVar(perf_test_label_frame)
        self.perf_tests_string_var.set("none")
        perf_tests_drop_down = tk.OptionMenu(perf_test_label_frame, self.perf_tests_string_var,
                                             *self.perf_tests)
        perf_tests_drop_down.config(width=23)
        perf_tests_drop_down.place(x=20, y=20)

    def gui_graph_checkbox(self, graph_label_frame):
        """The function creates a checkbox on GUI and calls function checkbox_graph to implement visualization using
        graphs """
        "graph_var variable  points to the checkbox object"
        self.graph_var = tk.IntVar(value=0)
        """data_var variable  points to the text object"""

        graph_cb = tk.Checkbutton(graph_label_frame, text='Generate graph', variable=self.graph_var,
                                  command=lambda: self.checkbox_graph(self.graph_var))
        graph_cb.place(x=20, y=22)

    def gui_dis_textbox(self, dis_label_frame):

        self.data_var = tk.IntVar(value=1)
        data = tk.Text(master=dis_label_frame, width='41', height='6')
        data.pack()
        if self.data_var.get():
            ser = serial.Serial(port='COM3', baudrate=9600, timeout=None)
            ser.isOpen()
            data.insert(END, "\n")
            serial_data = ser.readline().decode()
            data.insert(END, ser.readline())
            ser.close()

    def checkbox_graph(self, graph_var):
        """Fetches the value in checkbox to generate graph. Invokes function in Class: Execution_stm"""
        print(graph_var)
        if self.graph_var.get():
            print("Graph clicked")
        else:
            print("Graph unclicked")

    def gui_exec_button(self,button_label_frame):
        """The function gui_exec_button displays two buttons: Run and Reset on the GUI.
        Button *Run*: calls the functions in class Execution_stm to execute tests based on protocol and
                    test user selects.
        Button *Reset*: Function clear is invoked. The function clears the changes in GUI and sets the selection
                    to default value.
                    :param self: """
        test_result_button = tk.Button(master=button_label_frame, text="Run ", width='17',
                                       command=gfe.Execute(self.graph_var, self.perf_tests_string_var,
                                                           self.data_var).stm_execute)
        test_result_button.grid(row=0, column=0, padx='20', pady='10', sticky='W')

        reset_button = tk.Button(master=button_label_frame, text="Reset to default", width='17', command=self.clear)
        reset_button.grid(row=0, column=1, padx='20', pady='10', sticky='W')

    def clear(self):
        """Implements Button Reset functionality. The function clears the changes in GUI and sets the selection to
        default value """
        self.protocol_string_var.set("Protocol 1")
        self.perf_tests_string_var.set("Execution Time")
        self.graph_var.set(0)
        self.data_var.set(0)

    def gui_label_frame(self):
        """The function gui_label_frame divides the GUI into various frames, each having a feature.
        A label frame for each category generates an object, which is passed over to the respective functions."""
        protocol_label_frame = tk.LabelFrame(self.root, text="STM 32 Protocols", width=340, height=80)
        protocol_label_frame.grid(row=0, column=0, padx='20', pady='10', sticky='W')

        perf_test_label_frame = tk.LabelFrame(self.root, text="Performance Test", width=340, height=80)
        perf_test_label_frame.grid(row=1, column=0, padx='20', pady='10', sticky='W')

        graph_label_frame = tk.LabelFrame(self.root, width=340, height=80)
        graph_label_frame.grid(row=2, column=0, padx='20', pady='0', sticky='W')

        dis_label_frame = tk.LabelFrame(self.root, text="Display Output", width=340, height=80)
        dis_label_frame.grid(row=3, column=0, padx='20', pady='0', sticky='W')

        button_label_frame = tk.LabelFrame(self.root, text="Execute test", width=340, height=80)
        button_label_frame.grid(row=4, column=0, padx='20', pady='0', sticky='W')

        '''Functions to display each feature. Label frame object passed as parameter'''
        self.gui_protocol_dropdown(protocol_label_frame)
        self.gui_perf_test_dropdown(perf_test_label_frame)
        self.gui_graph_checkbox(graph_label_frame)
        self.gui_dis_textbox(dis_label_frame)
        self.gui_exec_button(button_label_frame)
