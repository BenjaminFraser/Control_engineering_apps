# import matplotlib graphical libraries
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import math
import numpy as np

# PIL lib for GUI image functionality
from PIL import Image, ImageTk

# import tkinter for app GUI
import tkinter as tk
from tkinter import ttk

from scipy import signal
import control

# basic definition for s-domain 's' operator
s = control.tf([1,0],1)

class ControlSystemApp(tk.Tk):
    """ A tkinter based GUI application for mathematical and graphical analysis of control
        systems. There are two main parts to the app: classical control and modern control.
        Each part has its own dedicated page on the tkinter app, and is represented as a 
        class that inherits from tk.Frame, and is called from this controller class.
    """
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Control Engineering Tool")
        
        container = tk.Frame(self, width=1200, height=800)

        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set default style of buttons for the app
        ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

        self.frames = {}

        for F in (StartPage, ClassicControl, ModernControl, PolesZerosPlots):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    """ Main application welcome page with a selection of buttons linking to
        seperate pages that analyse classical and digital (modern) control
        systems.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, bg="powder blue")
        top = tk.Frame(self, width=1200, height=100, bg="royal blue")
        top.pack(side="top")
        self.title = tk.Label(top, text="Control Engineering Modeller", font=('Helvetica', 30, 'bold'), fg="royal blue", bg="white smoke", bd=5)
        self.title.pack(pady=10,padx=10, fill='both')

        classic_button = ttk.Button(self, text="Classical Control Analysis", width=30,
                            command=lambda: controller.show_frame(ClassicControl))
        classic_button.pack(padx=10, pady=10)

        bode_poleszeros_button = ttk.Button(self, text="Bode plotter - using poles, zeros and gain", width=30,
                            command=lambda: controller.show_frame(PolesZerosPlots))
        bode_poleszeros_button.pack(padx=10, pady=10)

        modern_control_button = ttk.Button(self, text="Modern Control Systems Analysis", width=30,
                            command=lambda: controller.show_frame(ModernControl))
        modern_control_button.pack(padx=10, pady=10)

        # create a canvas object and insert front page image
        self.canvas = tk.Canvas(self, width=300, height=300, bg="powder blue")
        self.canvas.pack()
        self.img_file = Image.open("Control_Engineering_Icon.gif")
        self.display_img = ImageTk.PhotoImage(self.img_file)
        self.canvas.create_image(150, 150, image=self.display_img)

        signature = tk.Label(self, text="Created by B.D. Fraser", font=('arial', 8), fg="steel blue", bg="powder blue")
        signature.pack(side='bottom')


class ClassicControl(tk.Frame):
    """ Interactive page for analysis and visualisation of classical control systems.
        This focuses on systems operating on analogue models, that are analysed using
        Laplace transforms in the frequency domain.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="light goldenrod")
        top = tk.Frame(self, width=1200, height=100, bg="grey")
        top.pack(side="top")
        self.label = tk.Label(top, text="Classical Control System Plotter", font=('Helvetica', 30, 'bold'), bg="grey", bd=5)
        self.label.pack(pady=10,padx=10)

        self.data_area = tk.Frame(self, width=500, height=600, bg="light goldenrod")
        self.data_area.pack(side='left', padx=10)

        self.oltf_label = tk.Label(self.data_area, text="G(s) - Plant Transfer Function (Algebraic form):", font=('Helvetica', 15, 'bold'), bg="light goldenrod")
        self.oltf_label.pack()
        self.oltf = tk.Entry(self.data_area, bd = 5, bg="powder blue")
        self.oltf.insert("end", "1/(s*(s+1))")
        self.oltf.pack(pady=10, padx=10)

        self.compensator_label = tk.Label(self.data_area, text="F(s) - Compensator Transfer Function (Algebraic form):", font=('Helvetica', 15, 'bold'), bg="light goldenrod")
        self.compensator_label.pack()
        self.tf_compensator = tk.Entry(self.data_area, bd = 5, bg="cornsilk")
        self.tf_compensator.insert("end", "1")
        self.tf_compensator.pack(pady=10, padx=10)

        # button and functionality for bode plot
        self.bode_button = ttk.Button(self.data_area, text="Plot Open-loop Bode", width=25,
                            command= lambda: self.plot_bode(self.oltf.get(), self.tf_compensator.get()))
        self.bode_button.pack(pady=5, padx=10)

        # button and functionality for bode plot
        self.cltf_bode_button = ttk.Button(self.data_area, text="Plot Closed-loop Bode", width=25,
                            command= lambda: self.plot_bode(self.oltf.get(), self.tf_compensator.get(), closed_loop=True))
        self.cltf_bode_button.pack(pady=5, padx=10)

        # button and command functionality for Nyquist plot
        self.nyquist_button = ttk.Button(self.data_area, text="Make Nyquist plot", width=25,
                            command= lambda: self.plot_nyquist(self.oltf.get(), self.tf_compensator.get()))
        self.nyquist_button.pack(pady=5, padx=10)

        # button and command functionality for Time domain plots
        self.step_response_button = ttk.Button(self.data_area, text="Plot Step Response", width=25,
                            command= lambda: self.time_domain_response(self.oltf.get(), self.tf_compensator.get()))
        self.step_response_button.pack(pady=5, padx=10)

        # button and command functionality for Time domain plots
        self.ramp = ttk.Button(self.data_area, text="Plot Ramp Response", width=25,
                            command= lambda: self.time_domain_response(self.oltf.get(), self.tf_compensator.get(), ramp=True))
        self.ramp.pack(pady=5, padx=10)

        # button and command functionality for Root Locus plots
        self.root_locus = ttk.Button(self.data_area, text="Plot Root Locus", width=25,
                            command= lambda: self.root_locus_plot(self.oltf.get(), self.tf_compensator.get()))
        self.root_locus.pack(pady=5, padx=10)

        # return to home button
        self.home_button = ttk.Button(self.data_area, text="Return to Home", width=25,
                            command=lambda: controller.show_frame(StartPage))
        self.home_button.pack(padx=5, pady=10)

        self.diagram_area = tk.Frame(self, width=700, height=600, bg="light goldenrod")
        self.diagram_area.pack(side='right')

        # create a canvas object and insert front page image
        self.canvas = tk.Canvas(self.diagram_area, width=700, height=300, bg="light goldenrod")
        self.canvas.pack()
        self.img_file = Image.open("transfer_function_system.gif")
        self.display_img = ImageTk.PhotoImage(self.img_file)
        self.canvas.create_image(330, 150, image=self.display_img)

        # results area for displaying current gain and phase margin
        self.results_area = tk.Frame(self.diagram_area, width=700, height=200, bg="light goldenrod")
        self.results_area.pack()
        self.margin_label = tk.Label(self.results_area, text="System stability margins:", font=('Helvetica', 20, 'bold'), bg="light goldenrod")
        self.margin_label.pack(pady=20)
        self.current_margins = tk.StringVar()
        self.margin_text = tk.Label(self.results_area, textvariable=self.current_margins, height=4, width=50, font=('Helvetica', 15, 'bold'), bg="light goldenrod")
        self.margin_text.pack(pady=5)
        self.current_margins.set("Input a function to display gain and phase margins")

        # lower sig block
        self.signature = tk.Label(self, text="Created by B.D. Fraser", font=('arial', 8), fg="steel blue", bg="light goldenrod")
        self.signature.pack(side='bottom')

    def output_margins(self, sys_tf):
        """ Outputs the system stability margins based on the passed transfer
            function argument. Analysed parameters include the gain margin (dB),
            phase margin (deg), gain crossover freq (rad/s) and phase crossover
            freq (rad/s)
        """
        # gather open-loop gain and phase margins, and crossover freqs
        gain_m, pm, wg, wp = control.margin(sys_tf)

        # convert gain margin to dB
        gm = 20*math.log10(gain_m) if gain_m else 0

        # update gain and phase margin indication on GUI
        self.current_margins.set("Gain margin: {0} dB\nPhase margin: {1} degrees\n"
                                    "Gain crossover freq: {2} rad/s\n"
                                    "Phase crossover freq: {3} rad/s".format(gm, pm, wg, wp))
        return

    def plot_bode(self, oltf, tf_compensator, closed_loop=False):
        """ Plot either the open-loop or closed loop gain, dependent on closed_loop arg. 
            and phase response for the given transfer function. The closed-loop transfer function
            used is simply the unity gain negative feedback model of the given
            open-loop transfer function.
        """
        sys_tf = (eval(oltf)*(eval(tf_compensator)))

        self.output_margins(sys_tf)

        # if closed loop - determine cltf
        if closed_loop:
            sys_tf = control.feedback(sys_tf, 1)
            plt.figure(2)
        else:
            plt.figure(1)

        # obtain magnitude, phase and freq range using python control
        mag, phase, omega = control.bode_plot(sys_tf, dB=True)

        plt.figtext(0.3, 0.93, "Gain and Phase Response Bode Plots", size="large", weight="bold")

        # plot magnitude gain response sub-plot
        plt.subplot(2,1,1)
        plt.semilogx(omega,mag,'k-',linewidth=1, color="b")
        plt.grid(b=True, which='major', color='k', alpha=0.8)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.4)
        plt.ylabel('Gain magnitude (dB)', weight="bold")

        # plot phase response sub-plot
        plt.subplot(2,1,2)
        plt.semilogx(omega,phase,'k-',linewidth=1, color="g")
        plt.grid(b=True, which='major', color='k', alpha=0.8)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.4)
        plt.ylabel('Phase (degrees)', weight="bold")
        plt.xlabel('Frequency (rad/s)', weight="bold")
        plt.show()
        return

    def plot_nyquist(self, oltf, tf_compensator):
        """ Form a Nyquist plot for the given transfer function. Includes phase angle
            lines for ease of reference.
        """
        sys_tf = (eval(oltf)*(eval(tf_compensator)))
        plt.figure(3)
        control.nyquist_plot(sys_tf)
        plt.axis([-2,2,-2,2])
        theta = np.linspace(0,6.284,100)
        plt.plot(np.cos(theta),np.sin(theta),'r-')
        phi = np.linspace(0,360,37)/57.3
    
        for j in range(len(phi)):
            plt.plot([0,np.sin(phi[j])],[0,np.cos(phi[j])],'g--')            
        plt.grid(1)
        plt.title('System Nyquist Plot')
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.show()
        return

    def time_domain_response(self, oltf, tf_compensator, ramp=False):
        """ Plot the time-domain step response of the given transfer function.
            The closed-loop form of the transfer function must be used for this.
        """
        sys_tf = (eval(oltf)*(eval(tf_compensator)))
        closed_loop_tf = control.feedback(sys_tf, 1)

        # if ramp selected, convert to ramp response, otherwise do step
        if ramp:
            title_txt = "Ramp"
            plt.figure(5)
            [time, _] = control.step_response(closed_loop_tf)
            [x,y] = control.step_response((closed_loop_tf/s), time)
            plt.plot([0.0, max(x)], [0.0, max(x)], 'r--', linewidth=1)
        else:
            [x,y] = control.step_response(closed_loop_tf)
            plt.figure(4)
            title_txt = "Step"
        plt.plot(x,y, linewidth=1, alpha=1)
        plt.title("Time-domain Unit {0} Response".format(title_txt))
        plt.xlabel('Time (seconds)')
        plt.ylabel('Response')
        plt.grid(1)
        plt.show()
        return

    def root_locus_plot(self, oltf, tf_compensator):
        """ Plot the closed-loop root locus plot for the system based on the open
            loop transfer function poles and zeros.  
        """
        sys_tf = eval(oltf)*eval(tf_compensator)
        control.rlocus(sys_tf)
        plt.grid()
        plt.title('S-Domain Root Locus Plot')
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.show()
        return

class ModernControl(tk.Frame):
    """ Interactive page for analysis and visualisation of classical control systems.
        This focuses on systems operating on analogue models, that are analysed using
        Laplace transforms in the frequency domain.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="wheat")
        top = tk.Frame(self, width=1200, height=100, bg="grey")
        top.pack(side="top")
        self.label = tk.Label(top, text="Classical Control System Plotter", font=('Helvetica', 30, 'bold'), bg="grey", bd=5)
        self.label.pack(pady=10,padx=10)

        self.data_area = tk.Frame(self, width=500, height=600, bg="wheat")
        self.data_area.pack(side='left', padx=10)

        self.oltf_label = tk.Label(self.data_area, text="G(s) - Plant Transfer Function (Algebraic form):", font=('Helvetica', 15, 'bold'), bg="wheat")
        self.oltf_label.pack()
        self.oltf = tk.Entry(self.data_area, bd = 5, bg="powder blue")
        self.oltf.insert("end", "1/(s*(s+1))")
        self.oltf.pack(pady=10, padx=10)

        self.compensator_label = tk.Label(self.data_area, text="F(s) - Compensator Transfer Function (Algebraic form):", font=('Helvetica', 15, 'bold'), bg="wheat")
        self.compensator_label.pack()
        self.tf_compensator = tk.Entry(self.data_area, bd = 5, bg="cornsilk")
        self.tf_compensator.insert("end", "1")
        self.tf_compensator.pack(pady=10, padx=10)

        self.sampling_label = tk.Label(self.data_area, text="System Sampling Time period (seconds):", font=('arial', 15), bg="wheat")
        self.sampling_label.pack()
        self.sampling_time = tk.Entry(self.data_area, bd = 5, bg="cornsilk")
        self.sampling_time.insert("end", "0.1")
        self.sampling_time.pack(pady=5, padx=10)

        # button and functionality for bode plot
        self.bode_button = ttk.Button(self.data_area, text="Plot Open-loop Bode", width=25,
                            command= lambda: self.plot_bode(self.oltf.get(), self.tf_compensator.get(), self.sampling_time.get()))
        self.bode_button.pack(pady=5, padx=10)

        # button and functionality for bode plot
        self.cltf_bode_button = ttk.Button(self.data_area, text="Plot Closed-loop Bode", width=25,
                            command= lambda: self.plot_bode(self.oltf.get(), self.tf_compensator.get(), self.sampling_time.get(), closed_loop=True))
        self.cltf_bode_button.pack(pady=5, padx=10)

        # button and command functionality for Nyquist plot
        self.nyquist_button = ttk.Button(self.data_area, text="Make Nyquist plot", width=25,
                            command= lambda: self.plot_nyquist(self.oltf.get(), self.tf_compensator.get(), self.sampling_time.get()))
        self.nyquist_button.pack(pady=5, padx=10)

        # button and command functionality for Time domain plots
        self.step_response_button = ttk.Button(self.data_area, text="Plot Discrete Step Response", width=25,
                            command= lambda: self.time_domain_response(self.oltf.get(), self.tf_compensator.get(), self.sampling_time.get()))
        self.step_response_button.pack(pady=5, padx=10)

        # button and command functionality for Time domain plots
        self.ramp = ttk.Button(self.data_area, text="Plot Discrete Ramp Response", width=25,
                            command= lambda: self.time_domain_response(self.oltf.get(), self.tf_compensator.get(), self.sampling_time.get(), ramp=True))
        self.ramp.pack(pady=5, padx=10)

        # button and command functionality for Root Locus plots
        self.root_locus = ttk.Button(self.data_area, text="Plot Z-Domain Root Locus", width=25,
                            command= lambda: self.root_locus_plot(self.oltf.get(), self.tf_compensator.get(), self.sampling_time.get()))
        self.root_locus.pack(pady=5, padx=10)

        # return to home button
        self.home_button = ttk.Button(self.data_area, text="Return to Home", width=25,
                            command=lambda: controller.show_frame(StartPage))
        self.home_button.pack(padx=5, pady=10)

        self.diagram_area = tk.Frame(self, width=700, height=600, bg="wheat")
        self.diagram_area.pack(side='right')

        # create a canvas object and insert front page image
        self.canvas = tk.Canvas(self.diagram_area, width=700, height=300, bg="wheat")
        self.canvas.pack()
        self.img_file = Image.open("digital_control_system.gif")
        self.display_img = ImageTk.PhotoImage(self.img_file)
        self.canvas.create_image(330, 150, image=self.display_img)

        # results area for displaying current gain and phase margin
        self.results_area = tk.Frame(self.diagram_area, width=700, height=200, bg="wheat")
        self.results_area.pack()
        self.margin_label = tk.Label(self.results_area, text="System stability margins:", font=('Helvetica', 20, 'bold'), bg="wheat")
        self.margin_label.pack(pady=20)
        self.current_margins = tk.StringVar()
        self.margin_text = tk.Label(self.results_area, textvariable=self.current_margins, height=4, width=50, font=('Helvetica', 15, 'bold'), bg="wheat")
        self.margin_text.pack(pady=5)
        self.current_margins.set("Input a function to display gain and phase margins")

        # lower sig block
        self.signature = tk.Label(self, text="Created by B.D. Fraser", font=('arial', 8), fg="steel blue", bg="wheat")
        self.signature.pack(side='bottom')

    def output_margins(self, sys_tf):
        """ Outputs the system stability margins based on the passed transfer
            function argument. Analysed parameters include the gain margin (dB),
            phase margin (deg), gain crossover freq (rad/s) and phase crossover
            freq (rad/s)
        """
        # gather open-loop gain and phase margins, and crossover freqs
        gain_m, pm, wg, wp = control.margin(sys_tf)

        # convert gain margin to dB
        gm = 20*math.log10(gain_m) if gain_m else 0

        # update gain and phase margin indication on GUI
        self.current_margins.set("Gain margin: {0} dB\nPhase margin: {1} degrees\n"
                                    "Gain crossover freq: {2} rad/s\n"
                                    "Phase crossover freq: {3} rad/s".format(gm, pm, wg, wp))
        return

    def plot_bode(self, oltf, dig_compensator, sampling_time, closed_loop=False):
        """ Plot either the open-loop or closed loop gain, dependent on closed_loop arg. 
            and phase response for the given transfer function. The closed-loop transfer function
            used is simply the unity gain negative feedback model of the given
            open-loop transfer function.
        """
        sys_tf = eval(oltf)

        # basic definition for z-domain 'z' operator for digital freq analysis
        z = control.tf([1,0],1,float(sampling_time))

        discrete_sys_tf = control.sample_system(sys_tf, float(sampling_time), method='zoh')*eval(dig_compensator)

        self.output_margins(sys_tf)

        # if closed loop - determine cltf
        if closed_loop:
            tf_cl = control.tf(discrete_sys_tf)
            discrete_sys_tf = control.feedback(tf_cl, 1)
            plt.figure(2)
        else:
            plt.figure(1)

        freq_vector=np.linspace(0, np.pi/float(sampling_time), 500)
        control.bode_plot(discrete_sys_tf, omega=freq_vector, dB=True)
        plt.show()
        return

    def plot_nyquist(self, oltf, dig_compensator, sampling_time):
        """ Form a Nyquist plot for the given transfer function. Includes phase angle
            lines for ease of reference.
        """
        sys_tf = eval(oltf)
        z = control.tf([1,0],1,float(sampling_time))
        discrete_sys_tf = control.sample_system(sys_tf, float(sampling_time), method='zoh')*eval(dig_compensator)

        plt.figure(3)
        control.nyquist_plot(discrete_sys_tf)
        plt.axis([-2,2,-2,2])
        plt.grid(1)
        plt.title('Digital System Nyquist Plot')
        plt.xlabel('Real')
        plt.ylabel('Imaginary')

        # plot the unit circle for reference
        theta = np.linspace(0, np.pi*2, 100)
        plt.plot(np.cos(theta),np.sin(theta),'g--') 

        plt.show()
        return

    def time_domain_response(self, oltf, dig_compensator, sampling_time, ramp=False):
        """ Plot the time-domain step response of the given transfer function.
            The closed-loop form of the transfer function must be used for this.
        """
        sys_tf = eval(oltf)

        # basic definition for z-domain 'z' operator for digital freq analysis
        z = control.tf([1,0],1,float(sampling_time))

        discrete_sys_tf = control.sample_system(sys_tf, float(sampling_time), method='zoh')*eval(dig_compensator)
        closed_loop_tf = control.feedback(discrete_sys_tf, 1)

        # if ramp selected, convert to ramp response, otherwise do step
        if ramp:
            title_txt = "Ramp"
            plt.figure(5)
            [time, _] = control.step_response(closed_loop_tf)
            [x,y] = control.step_response((closed_loop_tf/s), time)
            print(closed_loop_tf)
            #plt.plot([0.0, max(x)], [0.0, max(x)], 'r--')
        else:
            [x,y] = control.step_response(closed_loop_tf)
            fig = plt.figure(4)
            title_txt = "Step"
        plt.stem(y)
        plt.title("Discrete Time Response to {0} input".format(title_txt))
        plt.xlabel("Sample number (sample period of {0})".format(sampling_time))
        plt.ylabel('Response')
        plt.grid(1)
        plt.show()
        return

    def root_locus_plot(self, oltf, dig_compensator, sampling_time):
        """ Plot the closed-loop root locus plot for the system based on the open
            loop transfer function poles and zeros.  
        """
        sys_tf = eval(oltf)
        z = control.tf([1,0],1,float(sampling_time))
        discrete_sys_tf = control.sample_system(sys_tf, float(sampling_time), method='zoh')*eval(dig_compensator)

        control.rlocus(discrete_sys_tf)
        theta=np.linspace(0, 2*np.pi, 100)
        plt.plot(np.cos(theta),np.sin(theta),'m--')
        damping=0.7
        rtz=np.sqrt(1-damping**2)
        plt.plot(np.real(np.exp(-theta*damping+1.0j*theta*rtz)),np.imag(np.exp(-theta*damping+1.0j*theta*rtz)),'g--')
        plt.plot(np.real(np.exp(-theta*damping-1.0j*theta*rtz)),np.imag(np.exp(-theta*damping-1.0j*theta*rtz)),'g--')
        plt.grid(1)
        plt.title('Z-Domain Root-Locus Plot')
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.show()
        return

class PolesZerosPlots(tk.Frame):
    """ A basic page to plot gain and phase bode plots from a set of system poles, zeros and gain """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Open-Loop Bode plot (with poles, zeroes and gain data)", font=('Helvetica', 30, 'bold'))
        label.pack(pady=10,padx=10)

        poles_label = tk.Label(self, text="Transfer function poles (seperate each by comma (,)):", font=('Helvetica', 30, 'bold'))
        poles_label.pack()
        tf_poles = tk.Entry(self, bd = 5)
        tf_poles.insert("end", "")
        tf_poles.pack(pady=10)

        zeros_label = tk.Label(self, text="Transfer function zeros (seperate each by comma (,):", font=('Helvetica', 30, 'bold'))
        zeros_label.pack()
        tf_zeros = tk.Entry(self, bd = 5)
        tf_zeros.insert("end", "")
        tf_zeros.pack(pady=10)

        gain_label = tk.Label(self, text="Transfer function gain:", font=('Helvetica', 30, 'bold'))
        gain_label.pack()
        tf_gain = tk.Entry(self, bd = 5)
        tf_gain.insert("end", "1")
        tf_gain.pack(pady=10)

        plot_button = ttk.Button(self, text="Make plot",
                            command= lambda: self.plot_bode(tf_poles.get(), tf_zeros.get(), tf_gain.get()))
        plot_button.pack()

        home_button = ttk.Button(self, text="Return to Home",
                            command=lambda: controller.show_frame(StartPage))
        home_button.pack()

    def plot_bode(self, poles, zeros, gain):
        """ takes in given system poles, zeros and gain, and then parses and converts into
            a scipy transfer function. The data gain and phase response data is then plotted """ 

        pole_strings, zero_strings = poles.split(","), zeros.split(",")

        if not poles:
            formatted_poles = []
        else:
            formatted_poles = list(map(float, pole_strings))

        if not zeros:
            formatted_zeros = []
        else:
            formatted_zeros = list(map(float, zero_strings))
        formatted_gain = float(gain)

        print("The poles, zeros and gain are: {0}, {1}, {2}".format(formatted_zeros, formatted_poles, formatted_gain))

        zerosPolesGain = signal.ZerosPolesGain(formatted_zeros, formatted_poles, formatted_gain)
        sys_tf = signal.TransferFunction(zerosPolesGain)
        plt.figure(6)

        print("The transfer function is: {0}".format(sys_tf))
        
        w,mag,phase = signal.bode(sys_tf)
        plt.figtext(0.3, 0.93, "Open-loop system response", size="large", weight="bold")

        # plot magnitude gain response sub-plot
        plt.subplot(2,1,1)
        plt.semilogx(w,mag,'k-',linewidth=2, color="r")
        plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.4)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.6)
        plt.ylabel('Gain magnitude (dB)', weight="bold")

        # plot phase response sub-plot
        plt.subplot(2,1,2)
        plt.semilogx(w,phase,'k-',linewidth=2, color="g")
        plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.4)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.6)
        plt.ylabel('Phase (degrees)', weight="bold")
        plt.xlabel('Frequency (rad/s)', weight="bold")
        plt.show()
        return

app = ControlSystemApp()
app.mainloop()