
# Import the necessary packages and modules
import GUI as gs
import matplotlib.pyplot as plt
import numpy as np


class Execute:
    def __init__(self, graph_var, perf_tests_string_var, protocol_string_var, data_var):
        self.graph_var = graph_var
        self.data_var = data_var
        self.perf_tests_string_var = perf_tests_string_var
        self.protocol_string_var = protocol_string_var

    def stm_execute(self):
        self.draw_graph()
        self.connect()

    def draw_graph(self):
        # print("helloooo ", self.graph_var)
        if self.graph_var.get():
            # print("Graph clicked")
            # Prepare the data
            x = np.linspace(0, 10, 100)

            # Plot the data
            plt.plot(x, x, label='xx')

            # Add a legend
            plt.legend()

            # Show the plot
            plt.show()
        else:
            print("Graph unclicked")

    def connect(self):
        if self.data_var.get():
            print('tt')
        else:
            print('nop')
