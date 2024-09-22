import tkinter as tk
from tkinter import ttk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from subfolder.oscillator import QuantumOscillator, psi_functions

colors = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
          "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}

# Gui

class Gui:
    def __init__(self, window):
        self.window = window
        self.right_half = tk.Frame(self.window, bg="#FFFFFF")
        self.right_half.pack(side=tk.RIGHT, fill="both", expand=1)
        self.left_half = tk.Frame(self.window, bg=colors["dark_green"])
        self.left_half.pack(side=tk.LEFT, fill="both", expand=1)
        self.text_label = tk.Label(self.left_half, text="", bg="#4a6c65", fg="white", width=30)
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas = None
        self.create_widgets()   

        self.window_counter = 0 

        self.window.bind("<Configure>", self.resize_frames)

        self.style = ttk.Style()
        self.style.configure("TNotebook", background="#FFFFFF", borderwidth=1,
                             highlightthickness=0, relief="flat")  # Configura el fondo del Notebook
        self.style.configure("TNotebook.Tab", background="#FFFFFF", foreground="#000000", padding=[10, 5])
        self.style.map("TNotebook.Tab",
               background=[("selected", "#FFFFFF")],  # Color de la pestaña seleccionada
               foreground=[("selected", "#000000")])  # Color del texto de la pestaña seleccionada
        # Configura el color de fondo y del texto de las pestañas
         
        self.window.bind("<Configure>", self.resize_frames)
    

        self.notebook = ttk.Notebook(self.right_half)
        self.notebook.pack(fill="both", expand=1)
        self.open_new_tab()
        
        new = tk.Button(self.left_half, text="New", fg="#FFFFFF", command=self.open_new_tab)
        new.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        new.place(relx=0.5, rely=0.1, anchor="center")


    def open_new_tab(self):    
        self.window_counter += 1
        new_tab = tk.Frame(self.notebook, bg="#FFFFFF")  # Usa el notebook como contenedor
        self.notebook.add(new_tab, text=f"Ventana {self.window_counter}")
        #label = tk.Label(new_tab, text="Esta es una nueva pestaña vacía", bg="#FFFFFF", fg="#000000")
        #label.pack(pady=40)
        self.notebook.select(new_tab)
    
    def create_widgets(self):
        btn_exit = tk.Button(self.left_half, text="Exit", fg="#FFFFFF", command=self.exit)
        btn_exit.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_exit.place(relx=0.25, rely=0.7, anchor="center")

        approach = tk.Button(self.left_half, text="Approach", fg="#FFFFFF", command=self.Approach)
        approach.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")  
        approach.place(relx=0.5, rely=0.7, anchor="center")

        btn_graph = tk.Button(self.left_half, text="3D", fg="#FFFFFF", command=self.graph_3D)
        btn_graph.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph.place(relx=0.75, rely=0.7, anchor="center")

        btn_clear = tk.Button(self.left_half, text="Clear", fg="#FFFFFF", command=self.clean)
        btn_clear.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_clear.place(relx=0.25, rely=0.8, anchor="center")

        btn_about = tk.Button(self.left_half, text="About", fg="#FFFFFF", command=self.Algorithm)
        btn_about.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_about.place(relx=0.5, rely=0.8, anchor="center")

        btn_graph_3D = tk.Button(self.left_half, text="LOGO", fg="#FFFFFF", command=self.logo)
        btn_graph_3D.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph_3D.place(relx=0.75, rely=0.8, anchor="center")
    

        density = tk.Button(self.left_half, text=r"Density", fg="#FFFFFF", command=self.histograma)
        density.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        density.place(relx=0.5, rely=0.9, anchor="center")
                
        # start points
        self.p1 = tk.Entry(self.left_half, width=6, bg="#4a6c65", fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.p1.place(relx=0.75, rely=0.4, anchor="center")
        p1 = tk.Label(self.left_half, text="P1", fg="white")
        p1.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        p1.place(relx=0.6, rely=0.4, anchor="center")
        

        
        self.p2 = tk.Entry(self.left_half, width=6, bg="#4a6c65", fg="white", bd=1, relief="flat",
                           highlightbackground="white", highlightcolor="white")
        self.p2.place(relx=0.75, rely=0.5, anchor="center")
        p2 = tk.Label(self.left_half, text="P2", fg="white")
        p2.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        p2.place(relx=0.6, rely=0.5, anchor="center")
        
        self.E = tk.Entry(self.left_half, width=6, bg="#4a6c65", fg="white", bd=1, relief="flat",
                          highlightbackground="white", highlightcolor="white")
        self.E.place(relx=0.75, rely=0.6, anchor="center")
        E = tk.Label(self.left_half, text="E", fg="white")
        E.place(relx=0.6, rely=0.6, anchor="center")
        E.config(bg="#4a6c65", borderwidth=0, fg="white")


        # learning rate 
        self.lr = tk.Entry(self.left_half, width=6, bg="#4a6c65",fg="white", bd=1, relief="flat",
                      highlightbackground="white", highlightcolor="white")
        self.lr.place(relx=0.38, rely=0.4, anchor="center")


        lr_label = tk.Label(self.left_half, text="Lr", fg="white")
        lr_label.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        lr_label.place(relx=0.23, rely=0.4, anchor="center")
        
        #Epochs
        self.epochs = tk.Entry(self.left_half, width=6, bg="#4a6c65",fg="white", bd=1, relief="flat",
                      highlightbackground="white", highlightcolor="white")
        self.epochs.place(relx=0.38, rely=0.5, anchor="center")

        ep_label = tk.Label(self.left_half, text="Ep", fg="white")
        ep_label.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        ep_label.place(relx=0.23, rely=0.5, anchor="center")

        menu_boton = tk.Menubutton(self.left_half, text="Quamtum System", relief=tk.FLAT,
                                bg=colors["dark_green"], fg="white", bd=0)

        menu_boton.menu = tk.Menu(menu_boton, tearoff=0, 
                                bg="white", fg="black", 
                                activebackground=colors["dark_green"], 
                                activeforeground="white", relief=tk.FLAT, bd=0)
        menu_boton["menu"] = menu_boton.menu
        
        menu_boton.menu.add_command(label="Quamtum oscillator", command=self.update_psi_trial_oscillator)
        menu_boton.menu.add_command(label="Particle in box", command=self.update_psi_trial_particleinbox)
        menu_boton.menu.add_command(label="Double well", command=self.update_Double_well)
        menu_boton.menu.add_command(label="Anaharmonic oscillator", command=self.update_Anarmonic)
        menu_boton.menu.add_command(label="Hydrogen Atom", command=self.update_Hydrogen)
        menu_boton.menu.add_command(label="Yukawa", command=self.update_yukawa)
        menu_boton.menu.add_command(label="Lennard-Jhones", command=self.update_LJ)
        menu_boton.menu.add_command(label="Histograma", command=self.histograma)
        
        menu_boton.place(relx=0.36, rely=0.2, anchor="center")

        self.psi_trial = tk.Menubutton(self.left_half, text=r"Ψ Trial", relief=tk.FLAT, 
                                  bg=colors["dark_green"], fg="white", bd=0)

        self.psi_trial.menu = tk.Menu(self.psi_trial, tearoff=0, 
                                bg="white", fg="black", 
                                activebackground=colors["dark_green"], 
                                activeforeground="white", relief=tk.FLAT, bd=0)
        
        self.psi_trial["menu"] = self.psi_trial.menu
        self.psi_trial.place(relx=0.75, rely=0.2, anchor="center")

    def update_psi_trial_oscillator(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())
        from subfolder.oscillator import OA

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ₁(x) = x * e^(-α * x²)", command=lambda: Q_O.Psi("psi1"))
        self.psi_trial.menu.add_command(label="ψ₂(x) = 1 / (α * x² + 1)²", command=lambda: Q_O.Psi("psi2"))
        self.psi_trial.menu.add_command(label="ψ₃(x) = 1 / (x² + α)", command=lambda: Q_O.Psi("psi3"))
        self.psi_trial.menu.add_command(label="ψ₄(x) = 1 / (x² + α²)", command=lambda: Q_O.Psi("psi4"))
        self.psi_trial.menu.add_command(label="ψ₅(x) = 1 / (x² + α²)²", command=lambda: Q_O.Psi("psi5"))
        self.psi_trial.menu.add_command(label="ψ₆(x) = (x²) / (x² + α)²", command=lambda: Q_O.Psi("psi6"))
        
        #self.clean()
        OA()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    
    def update_psi_trial_particleinbox(self):
        
        current_tab = self.notebook.nametowidget(self.notebook.select())
        print(current_tab)
        from subfolder.Box import Box

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 1")
        self.psi_trial.menu.add_command(label="ψ(x) = 2")
        self.psi_trial.menu.add_command(label="ψ(x) = 3")
        self.psi_trial.menu.add_command(label="ψ(x) = 4")
        
        self.clean()
        Box()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        
    def update_Double_well(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        from subfolder.double_well import Double_well
        
        for widget in current_tab.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 5")
        self.psi_trial.menu.add_command(label="ψ(x) = 6")
        self.psi_trial.menu.add_command(label="ψ(x) = 7")

        #self.clean()
        Double_well()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
 
    def update_Anarmonic(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        
        from subfolder.Anarmonic import Anarmonic
        
        for widget in current_tab.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 8")
        self.psi_trial.menu.add_command(label="ψ(x) = 9")
        
        #self.clean()
        Anarmonic()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
 
    def update_Hydrogen(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())
        from subfolder.H import H

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 10", command=self.O_A)
        self.psi_trial.menu.add_command(label="ψ(x) = 11")
        
        self.clean()
        H()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def update_yukawa(self):
        
        current_tab = self.notebook.nametowidget(self.notebook.select())

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 12")
        self.psi_trial.menu.add_command(label="ψ(x) = 13")
        
        from subfolder.yukawa import yukawa
        self.clean()
        
        yukawa()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    
    def update_LJ(self):

        current_tab = self.notebook.nametowidget(self.notebook.select())

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 14")
        self.psi_trial.menu.add_command(label="ψ(x) = 15")
               

        from subfolder.Lennar_Jones import LJ
        self.clean()
        
        LJ()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    
    def logo(self):
        
        from logo import logo 
        
        current_tab = self.notebook.nametowidget(self.notebook.select())
        
        logo()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def histograma(self):

        current_tab = self.notebook.index(self.notebook.select())
        
        from subfolder.his import hist

        hist(self.E.get())
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    


    def get_p1(self):
        return self.p1.get()
    
    def get_p2(self):
        return self.p2.get()


    def get_lr(self):
        return self.lr.get()

    def get_ep(self):
        return self.epochs.get()

    def O_A(self):
        self.clean()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def resize_frames(self, event):
        global_width = self.window.winfo_width()
        new_global_width = global_width // 3
        self.left_half.configure(width=new_global_width)
        self.right_half.configure(width=2*new_global_width)

    def Algorithm(self):
        
        current_tab = self.notebook.index(self.notebook.select())
        from subfolder.Algorithm import Algorithm
        self.clean()
        Algorithm()
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def exit(self):
        self.window.quit()

    def Approach(self):
        current_tab = self.notebook.index(self.notebook.select())
        self.clean()
        E_1, dE_1 = Q_O.calculate_energy()
        Q_O.plot_energy(E_1, dE_1)
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=current_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def graph(self):
        self.clean()
        self.diagram()

    def clean(self):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            plt.clf()  # Clear the current figure
            self.canvas = None
    
    def graph_3D(self):
        self.clean()

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator
        from subfolder.E import E 
        
        E()

        #color = {"black":"#000000", "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}
        #plt.rcParams['toolbar'] = 'none'

        #alpha = np.linspace(-5, 5, 30)
        #beta = np.linspace(-5, 5, 30)
        #
        #alpha, beta = np.meshgrid(alpha, beta)
        #m, w, h = 1.0, 1.0, 1.0
        #
        #E = 0.25 * alpha * m * w**2 + 0.5 * beta**2 * m * w**2 + h**2 / (4 * alpha * m)
        #
        #min_E = np.min(E)
        #min_indices = np.unravel_index(np.argmin(E, axis=None), E.shape)
        #min_alpha = alpha[min_indices]
        #min_beta = beta[min_indices]
        #
        #fig = plt.figure(figsize=(10, 8))
        #ax = fig.add_subplot(111, projection='3d')
        #
        #ax.plot_wireframe(alpha, beta, E, color=color["black"], linewidth=0.5, alpha=0.5)
        #
        #ax.scatter(min_alpha, min_beta, min_E, color=color["purple"], s=50, label='Mínimo')
        #ax.contour(alpha, beta, E, zdir='z', offset=ax.get_zlim()[0], colors=color["black"], alpha=0.7)
        #
        #ax.set_xlabel(r'$\alpha$')
        #ax.set_ylabel(r'$\beta$')
        #ax.set_zlabel(r'$E(\alpha, \beta)$')
        #ax.set_title(r'$E = 0.25 \alpha m w^{2} + 0.5 \beta^{2} m w^{2} + \frac{h^{2}}{4 \alpha m}$')
        #
        #ax.view_init(elev=20, azim=135)
        #ax.grid(False)
        #ax.xaxis.pane.set_edgecolor('black')
        #ax.yaxis.pane.set_edgecolor('black')
        #ax.zaxis.pane.set_edgecolor('black')
        #ax.xaxis.pane.fill = False
        #ax.yaxis.pane.fill = False
        #ax.zaxis.pane.fill = False
        #
        #ax.xaxis.set_major_locator(MultipleLocator(5))
        #ax.yaxis.set_major_locator(MultipleLocator(5))
        #ax.zaxis.set_major_locator(MultipleLocator(5))
        #
        #ax.xaxis._axinfo['tick']['inward_factor'] = 0
        #ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        #ax.yaxis._axinfo['tick']['inward_factor'] = 0
        #ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        #ax.zaxis._axinfo['tick']['inward_factor'] = 0
        #ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


if __name__ == "__main__":

    window = tk.Tk()
    window.config(bg="#FFFFFF")
    window.minsize(1000, 500)
    #window.maxsize(1200, 700)
    app = Gui(window=window)
    app.logo()
    Q_O = QuantumOscillator(app)
    window.mainloop()
