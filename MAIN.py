import tkinter as tk
import GUI as g


def main():
    """
    Description:
    The purpose of the GUI is to visualize the comparison and categorization of protocols.
    The main functions of GUI are as below:
    User can select the available protocols to establish connectivity between two STM32 boards.
    User can also execute performance analysis through various tests:
    a. Execution Time
    b. Power Consumption
    c. Memory Usage
    User can opt to plot and generate graphs along with execution.

    Files Used:

    Function: Calls GUI_stm.py python file to execute GUI
    :return GUI
    """
    """GUI title"""
    title = "Protocol Performance Analysis"
    """Window size"""
    width = "450"
    height = "520"
    """Drop down for Protocols to be executed"""
    stm_protocols = sorted({"Protocol 1", "Protocol 2", "Protocol 3"})
    """Drop down for Performance Test to be executed"""
    perf_tests = sorted({"Execution Time", "Memory Usage", "Power Consumption"})

    root = tk.Tk()
    g.GuiWindow(root, width, height, stm_protocols, perf_tests, title).gui_features()
    root.mainloop()


if __name__ == "__main__":
    main()
