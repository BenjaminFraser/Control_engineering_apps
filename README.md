# **CONTROL ENGINEERING ANALYSIS AND SIMULATION APP - README** 

----------

## INTRODUCTION 

The control engineering app is designed to provide quick and convenient analysis of a wide range of control system elements within the field of both classical and modern (digital) control. All plots generated are interactive and can be analysed effectively from a given algebraic s-domain and/or z-domain transfer function.

The application is built using Python, with a tkinter GUI, and operates using python control, matplotlib, scipy and numpy.

![application overview example](example_images/classical_control_example.png?raw=True "Application overview - The many different features available for classical control analysis.")

![application plot examples](example_images/classical_control_example_2.png?raw=True "Application overview - An example of bode plots producable by the application.")

![application time domain examples](example_images/time_response_examples.png?raw=True "Example of plotting a time-domain response to both step and ramp inputs.")

![application discrete time examples](example_images/digital_control_example.png?raw=True "An overview of the modern control system interface within the application.")

![application discrete time domain example](example_images/digital_control_example_2.png?raw=True "An example of the discrete time-domain plot capability.")

----------

## ACCESSING THE APPLICATION/SYSTEM

The application is designed in Python 3.4, but has been tested to work on Python 2.7. To setup the system for use, you'll need to ensure you have installed all the necessary libraries, including numpy, scipy, matplotlib and python-control. The easiest, and most accessible means of operating data science related libraries such as these is to use Anaconda. Conversely, you can manually install and manage using pip install, however I'd recommend at least using a virtual environment.  

----------

## Example use cases and images

![application nyquist plot](example_images/nyquist_example.png?raw=True "Example of using the app to produce a Nyquist plot.")

![application root locus](example_images/root_locus_example.png?raw=True "Root locus plotting example")

----------

## Author 

Benjamin Fraser

--------
