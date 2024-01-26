"""
@file lab0example.py

Authors: Conor Schott, Fermin Moreno, Berent Baysal

Run real or simulated dynamic response tests and plot the results. This program
demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
old-fashioned and useful GUI library included in Python by default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@date   2023-12-24 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import math
import time
import tkinter
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Make an example plot to demonstrate embedding a plot into a GUI.

    Parameters:
        - plot_axes: Matplotlib plot axes.
        - plot_canvas: Matplotlib plot canvas.
        - xlabel: Label for the plot's horizontal axis.
        - ylabel: Label for the plot's vertical axis.

    Description:
        - Simulates data (times and volts) as if collected from a diving board motion.
        - Reads real test data through the USB-serial port and processes it to create two lists (`times` and `volts`).
        - Generates theoretical data (`theory_times` and `theory_volts`).
        - Plots both actual and theoretical data on the given axes.
    """
    # Here we create some fake data. It is put into an X-axis list (times) and
    # a Y-axis list (boing). Real test data will be read through the USB-serial
    # port and processed to make two lists like these
    # Specify the serial port and baud rate
    serial_port = 'COM9'  
    baud_rate = 115200
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    ser.write(b'\x04')
        
    times = []
    volts = []
        
    stop_condition = 0

    while stop_condition <= 1990:
        try:
            # Read data from the microcontroller
            data = ser.readline().decode('utf-8').strip()
            print(data)
            
            times_str, volts_str = data.split(',')
            times_flt = float(times_str)
            volts_flt = float(volts_str)
        
            times.append(times_flt)
            volts.append(volts_flt)
            stop_condition += 10
            
        except ValueError:
            print('Data collection in process')
      
    print(times)
    print(volts)
    
    VMAX = 3.094  # Replace with your actual VMAX value
    R = 90.4e3  # 90.3 K ohms
    C = 3.3e-6  # 3.3 microfarads

    # Generate theory data
    theory_times = list(range(2000))
    theory_volts = [VMAX * (1 - math.exp(-t / (R * C * 1000))) for t in theory_times]
    plot_axes.plot(theory_times, theory_volts, label='Data Points')
    
    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(times, volts, 'o', label='Data Points')
    
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    # plot_axes.legend()  # Show legend for the label
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.

    Parameters:
        - plot_function: The function that, when executed, creates a plot on the specified axes and canvas.
        - xlabel: Label for the plot's horizontal axis.
        - ylabel: Label for the plot's vertical axis.
        - title: A title for the plot; it shows up in the window title bar.

    Description:
        - Initializes the main Tkinter window.
        - Creates Matplotlib figure and axes.
        - Sets up drawing canvas and toolbar for navigation.
        - Adds buttons for quitting, clearing the plot, and running the test.
        - Arranges components in a grid.
        - Executes the Tkinter main loop, keeping the program running until the user closes the window.
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Voltage vs. Time")
