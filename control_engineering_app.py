import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
# PIL lib for GUI image functionality
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from scipy import signal

import control

# basic definition for s-domain 's' operator
s = control.tf([1,0],1)


LARGE_FONT= ("Verdana", 12)

class ClassicalControlApp(tk.Tk):

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, bg="powder blue")
        label = tk.Label(self, text="Control Engineering Modeller", font=('arial', 30, 'bold'), fg="steel blue", bg="powder blue")
        label.pack(pady=10,padx=10)

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="light goldenrod")
        label = tk.Label(self, text="Classical Control Systems Plotter", font=('arial', 30, 'bold'), bg="light goldenrod")
        label.pack(pady=10,padx=10)

        numerator_label = tk.Label(self, text="Transfer function Numerator (Algebraic form):", font=('arial', 15), bg="light goldenrod")
        numerator_label.pack()
        tf_numerator = tk.Entry(self, bd = 5, bg="powder blue")
        tf_numerator.insert("end", "1")
        tf_numerator.pack(pady=10, padx=10)

        denominator_label = tk.Label(self, text="Transfer function Denumerator (Algebraic form):", font=('arial', 15), bg="light goldenrod")
        denominator_label.pack()
        tf_denominator = tk.Entry(self, bd = 5, bg="cornsilk")
        tf_denominator.insert("end", "s*(s+1)")
        tf_denominator.pack(pady=10, padx=10)

        # button and functionality for bode plot
        bode_button = ttk.Button(self, text="Make Bode Plot", width=25,
                            command= lambda: self.plot_bode(tf_numerator.get(), tf_denominator.get()))
        bode_button.pack(pady=10, padx=10)

        # button and command functionality for Nyquist plot
        nyquist_button = ttk.Button(self, text="Make Nyquist plot", width=25,
                            command= lambda: self.plot_nyquist(tf_numerator.get(), tf_denominator.get()))
        nyquist_button.pack(pady=10, padx=10)

        # button and command functionality for Time domain plots
        step_response_button = ttk.Button(self, text="Plot Step Response", width=25,
                            command= lambda: self.time_domain_step_response(tf_numerator.get(), tf_denominator.get()))
        step_response_button.pack(pady=10, padx=10)

        # button and command functionality for Time domain plots
        ramp = ttk.Button(self, text="Plot Ramp Response", width=25,
                            command= lambda: self.time_domain_ramp_response(tf_numerator.get(), tf_denominator.get()))
        ramp.pack(pady=10, padx=10)

        # return to home button
        home_button = ttk.Button(self, text="Return to Home", width=25,
                            command=lambda: controller.show_frame(StartPage))
        home_button.pack(padx=10, pady=10)

        # create a canvas object and insert front page image
        self.canvas = tk.Canvas(self, width=300, height=300, bg="light goldenrod")
        self.canvas.pack()
        self.img_file = Image.open("transfer_function_system.gif")
        self.display_img = ImageTk.PhotoImage(self.img_file)
        self.canvas.create_image(150, 150, image=self.display_img)

        signature = tk.Label(self, text="Created by B.D. Fraser", font=('arial', 8), fg="steel blue", bg="powder blue")
        signature.pack(side='bottom')


    def plot_bode(self, tf_numerator, tf_denominator):
        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))

        # obtain magnitude, phase and freq range using python control
        mag, phase, omega = control.bode_plot(sys_tf, dB=True)

        plt.figure(1)
        plt.figtext(0.3, 0.93, "Gain and phase response Bode plots", size="large", weight="bold")

        # plot magnitude gain response sub-plot
        plt.subplot(2,1,1)
        plt.semilogx(omega,mag,'k-',linewidth=2, color="b")
        plt.grid(b=True, which='major', color='k', alpha=0.8)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.4)
        plt.ylabel('Gain magnitude (dB)', weight="bold")

        # plot phase response sub-plot
        plt.subplot(2,1,2)
        plt.semilogx(omega,phase,'k-',linewidth=2, color="g")
        plt.grid(b=True, which='major', color='k', alpha=0.8)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.4)
        plt.ylabel('Phase (degrees)', weight="bold")
        plt.xlabel('Frequency (rad/s)', weight="bold")
        plt.show()
        return

    def plot_nyquist(self, tf_numerator, tf_denominator):
        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))
        plt.figure(2)
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

    def time_domain_step_response(self, tf_numerator, tf_denominator):
        """
        """
        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))
        closed_loop_tf = control.feedback(sys_tf, 1)

        # plot step response
        [x,y] = control.step_response(closed_loop_tf)
        plt.figure(3)
        plt.plot(x,y)
        plt.title('Time-domain Unit Step Response')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Response')
        plt.grid(1)
        plt.show()
        return

    def time_domain_ramp_response(self, tf_numerator, tf_denominator):
        """
        """
        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))
        closed_loop_tf = control.feedback(sys_tf, 1)
        plt.figure(4)
        [time, _] = control.step_response(closed_loop_tf)
        [x,y] = control.step_response((closed_loop_tf/s), time)
        plt.plot(x,y)
        plt.plot([0.0, max(x)], [0.0, max(x)], 'r--')
        plt.grid(1)
        plt.title('Time-domain Unit Ramp Response')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Response')
        plt.show()    
        return

class ModernControl(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="wheat")
        label = tk.Label(self, text="Classical Control Systems Plotter", font=('arial', 30, 'bold'), bg="wheat")
        label.pack(pady=10,padx=10)

        numerator_label = tk.Label(self, text="Transfer function Numerator (Algebraic form):", font=('arial', 15), bg="wheat")
        numerator_label.pack()
        tf_numerator = tk.Entry(self, bd = 5, bg="powder blue")
        tf_numerator.insert("end", "1")
        tf_numerator.pack(pady=10, padx=10)

        denominator_label = tk.Label(self, text="Transfer function Denumerator (Algebraic form):", font=('arial', 15), bg="wheat")
        denominator_label.pack()
        tf_denominator = tk.Entry(self, bd = 5, bg="cornsilk")
        tf_denominator.insert("end", "s*(s+1)")
        tf_denominator.pack(pady=10, padx=10)

        # button and functionality for bode plot
        bode_button = ttk.Button(self, text="Make Bode Plot", width=25,
                            command= lambda: self.plot_bode(tf_numerator.get(), tf_denominator.get()))
        bode_button.pack(pady=10, padx=10)

        # button and command functionality for Nyquist plot
        nyquist_button = ttk.Button(self, text="Make Nyquist plot", width=25,
                            command= lambda: self.plot_nyquist(tf_numerator.get(), tf_denominator.get()))
        nyquist_button.pack(pady=10, padx=10)

        # button and command functionality for Time domain plots
        time_response_button = ttk.Button(self, text="Plot Step and Ramp Response", width=25,
                            command= lambda: self.time_domain_response(tf_numerator.get(), tf_denominator.get()))
        time_response_button.pack(pady=10, padx=10)

        # return to home button
        home_button = ttk.Button(self, text="Return to Home", width=25,
                            command=lambda: controller.show_frame(StartPage))
        home_button.pack(padx=10, pady=10)

    def plot_bode(self, tf_numerator, tf_denominator):
        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))

        # obtain magnitude, phase and freq range using python control
        mag, phase, omega = control.bode_plot(sys_tf, dB=True)

        plt.figure(1)
        plt.figtext(0.3, 0.93, "Gain and phase response Bode plots", size="large", weight="bold")

        # plot magnitude gain response sub-plot
        plt.subplot(2,1,1)
        plt.semilogx(omega,mag,'k-',linewidth=2, color="r")
        plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.8)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.4)
        plt.ylabel('Gain magnitude (dB)', weight="bold")

        # plot phase response sub-plot
        plt.subplot(2,1,2)
        plt.semilogx(omega,phase,'k-',linewidth=2, color="g")
        plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.8)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.4)
        plt.ylabel('Phase (degrees)', weight="bold")
        plt.xlabel('Frequency (rad/s)', weight="bold")
        plt.show()
        return

    def plot_nyquist(self, tf_numerator, tf_denominator):
        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))
        plt.figure(2)
        control.nyquist_plot(sys_tf)
        plt.axis([-2,2,-2,2])
        theta = np.linspace(0,6.284,100)
        plt.plot(np.cos(theta),np.sin(theta),'r-')
        phi = np.linspace(0,360,37)/57.3
    
        for j in range(len(phi)):
            plt.plot([0,np.sin(phi[j])],[0,np.cos(phi[j])],'g--')            
        plt.grid(1)
        plt.title('Nyquist Plot')
        plt.xlabel('Real')
        plt.ylabel('Imag')
        plt.show()
        return

    def time_domain_response(self, tf_numerator, tf_denominator, step=True, ramp=True):
        """
        """

        sys_tf = (eval(tf_numerator)/(eval(tf_denominator)))
        closed_loop_tf = control.feedback(sys_tf, 1)
        [x,y] = control.step_response(closed_loop_tf)
        plt.figure(3)
        plt.plot(x,y)
        plt.title('Time-domain Unit Step Response')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Response')
        plt.grid(1)
        plt.show()
        return

class PolesZerosPlots(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Open-Loop Bode plot (with poles, zeroes and gain data)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        poles_label = tk.Label(self, text="Transfer function poles (seperate each by comma (,)):", font=LARGE_FONT)
        poles_label.pack()
        tf_poles = tk.Entry(self, bd = 5)
        tf_poles.insert("end", "")
        tf_poles.pack(pady=10)

        zeros_label = tk.Label(self, text="Transfer function zeros (seperate each by comma (,):", font=LARGE_FONT)
        zeros_label.pack()
        tf_zeros = tk.Entry(self, bd = 5)
        tf_zeros.insert("end", "")
        tf_zeros.pack(pady=10)

        gain_label = tk.Label(self, text="Transfer function gain:", font=LARGE_FONT)
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
        """ takes in the given poles, zeros and gain, and parses them and converts into
            a scipy transfer function, followed by plotting on a bode plot """ 

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

app = ClassicalControlApp()
app.mainloop()