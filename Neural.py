import tkinter as tk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dictionarie of color

colors = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
          "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}

# Define the trial functions
# Class' Cuamtum oscillator

psi_functions = {
    "psi1": lambda x, alpha: x * sp.exp(-alpha * x**2),
    "psi2": lambda x, alpha: 1 / (alpha * x**2 + 1)**2,
    "psi3": lambda x, alpha: 1 / (x**2 + alpha),
    "psi4": lambda x, alpha: 1 / (x**2 + alpha**2),
    "psi5": lambda x, alpha: 1 / (x**2 + alpha**2)**2,
    "psi6": lambda x, alpha: (x**2) / (x**2 + alpha)**2
    }


class QuantumOscillator:
    def __init__(self, Gui_instance):
        
        self.color = {"black": "#000000", "green": "#488c2e", "purple": "#6a0606", "gray": "#b9b9b9"}
        plt.rcParams["toolbar"] = "none"

        self.x, self.a, self.m, self.w, self.h = sp.symbols("x a m w h", real=True, positive=True)
        self.A = sp.symbols("A", real=True)  # Dejar A como un símbolo separado
        
        self.psi = None

        self.V = (1/2) * self.m * self.w**2 * self.x**2
        self.Gui_instance = Gui_instance
    
    def Psi(self, psi_key):
        self.psi = psi_functions[psi_key](self.x, self.a)

        #if psi_key in psi_functions:
        #    self.psi = psi_functions[psi_key](self.x, self.a)
        #else:
        #    raise ValueError("Psi no es valida")
        #print(psi_key)

    
    def T(self, psi):
        T_hat = -(self.h**2) / (2 * self.m)
        return sp.integrate(psi * T_hat * sp.diff(psi, self.x, 2), (self.x, -sp.oo, sp.oo))

    def U(self, psi):
        return sp.integrate(psi * self.V * psi, (self.x, -sp.oo, sp.oo))

    def N(self, psi):
        return sp.integrate(psi * psi, (self.x, -sp.oo, sp.oo))

    def Normalize(self):
        cons = sp.solve(sp.Eq(sp.integrate(self.A * self.psi * self.A * self.psi, (self.x, -sp.oo, sp.oo)), 1), self.A)
        return cons[0]

    def calculate_energy(self):
        A_value = self.Normalize()
        psi_normalized = A_value * self.psi

        T_normalized = self.T(psi_normalized)
        U_normalized = self.U(psi_normalized)
        N_normalized = self.N(psi_normalized)

        E = T_normalized + U_normalized
        dE = sp.diff(E, self.a)

        return E, dE

    def plot_energy(self, E, dE):
        E_subs = E.subs({self.m: 1, self.w: 1, self.h: 1})
        dE_da = dE.subs({self.m: 1, self.w: 1, self.h: 1})
        dE_da = sp.lambdify(self.a, dE_da, 'numpy')

        E_plot = sp.lambdify(self.a, E_subs, 'numpy')

        a = np.linspace(0.1, 2, 100)
        Energy = E_plot(a)

        E_latex = sp.latex(E)

        # Minimizacion GD
         
        theta = 0.2
        lr = float(self.Gui_instance.get_lr()) 
        iter = int(self.Gui_instance.get_ep())

        for i in range(iter):
            grad = dE_da(theta)
            theta -= lr * grad

        w_val = 1
        m_val = 1
        x_val = np.linspace(-1, 1, 100)
        V_fun = lambda x: 0.5*m_val*w_val**2*x**2
        V_val = V_fun(x_val)
        
        x_sym = sp.Symbol("x")
        alpha_sym = sp.Symbol('alpha')
        alpha_value = theta
        
        sym_func  = self.psi.subs(self.a, alpha_value)
        func_numeric = sp.lambdify(x_sym, sym_func, 'numpy')
        
        x  = np.linspace(-10, 10, 100)
        y  = func_numeric(x) 
        Y  = y*y

        plt.subplot(2, 2, 1)
        plt.plot(x, y, color='#000000', label="f1")
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        
        plt.subplot(2, 2, 2)
        plt.plot(x, Y, color='gray', label="f3")
        plt.fill(x, Y, color=colors["gray"])
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()


        plt.subplot(2, 2, (3, 4))
        plt.plot(a, Energy, color=self.color["black"], label=f"${E_latex}$")
        plt.scatter(theta, E_plot(theta), color=self.color["purple"], label=f"${E_plot(theta):.3f} \\hbar \\omega$")
        plt.axvline(0, color=self.color["gray"])
        plt.axhline(0, color=self.color["gray"])
        plt.legend()
        plt.xlim(0.1, 2)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
    
        #plt.tight_layout()
        plt.subplots_adjust(wspace=0.3)
        plt.subplots_adjust(hspace=0.4)

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
        
        self.window.bind("<Configure>", self.resize_frames)

        # Crear el notebook
        #self.notebook = ttk.Notebook(self.right_half)
        #self.notebook.pack(fill="both", expand=1)

    #def open_new_tab(self):
    #    new_tab = ttk.Frame(self.notebook)
    #    self.notebook.add(new_tab, text="New Tab")
    #    label = tk.Label(new_tab, text="Esta es una nueva pestaña vacía.", bg="#FFFFFF", fg="#000000")
    #    label.pack(pady=20)
    #    self.notebook.select(new_tab)
       
    def create_widgets(self):
        btn_exit = tk.Button(self.left_half, text="Exit", fg="#FFFFFF", command=self.exit)
        btn_exit.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_exit.place(relx=0.25, rely=0.7, anchor="center")

        btn_draw = tk.Button(self.left_half, text="Approach", fg="#FFFFFF", command=self.draw)
        btn_draw.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")  
        btn_draw.place(relx=0.5, rely=0.7, anchor="center")

        btn_graph = tk.Button(self.left_half, text="Graph", fg="#FFFFFF", command=self.graph)
        btn_graph.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph.place(relx=0.75, rely=0.7, anchor="center")

     #   new = tk.Button(self.left_half, text="New", fg="#FFFFFF", command=self.open_new_tab)
     #   new.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
     #   new.place(relx=0.7, rely=0.6, anchor="center")

        btn_clear = tk.Button(self.left_half, text="Clear", fg="#FFFFFF", command=self.clean)
        btn_clear.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_clear.place(relx=0.25, rely=0.8, anchor="center")

        btn_about = tk.Button(self.left_half, text="About", fg="#FFFFFF", command=self.About)
        btn_about.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_about.place(relx=0.5, rely=0.8, anchor="center")

        btn_graph_3D = tk.Button(self.left_half, text="3D", fg="#FFFFFF", command=self.graph_3D)
        btn_graph_3D.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        btn_graph_3D.place(relx=0.75, rely=0.8, anchor="center")

        self.lr = tk.Entry(self.left_half, width=10, bg="#4a6c65",fg="white", bd=1, relief="flat",
                      highlightbackground="white", highlightcolor="white")
        self.lr.place(relx=0.4, rely=0.4, anchor="center")

        lr_label = tk.Label(self.left_half, text="Lr", fg="white")
        lr_label.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        lr_label.place(relx=0.23, rely=0.4, anchor="center")
        
        self.epochs = tk.Entry(self.left_half, width=10, bg="#4a6c65",fg="white", bd=1, relief="flat",
                      highlightbackground="white", highlightcolor="white")
        self.epochs.place(relx=0.4, rely=0.5, anchor="center")

        ep_label = tk.Label(self.left_half, text="Ep", fg="white")
        ep_label.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
        ep_label.place(relx=0.23, rely=0.5, anchor="center")

        menu_boton = tk.Menubutton(self.left_half, text="Cuamtum System", relief=tk.FLAT,
                                bg=colors["dark_green"], fg="white", bd=0)

        menu_boton.menu = tk.Menu(menu_boton, tearoff=0, 
                                bg="white", fg="black", 
                                activebackground=colors["dark_green"], 
                                activeforeground="white", relief=tk.FLAT, bd=0)
        menu_boton["menu"] = menu_boton.menu
        

        menu_boton.menu.add_command(label="Cuamtum oscillator", command=self.update_psi_trial_oscillator)
        menu_boton.menu.add_command(label="Particle in box", command=self.update_psi_trial_particleinbox)
        menu_boton.menu.add_command(label="Potential", command=self.update_potential)
        menu_boton.menu.add_command(label="Anaharmonic oscillator", command=self.update_Anarmonic)
        menu_boton.menu.add_command(label="Hydrogen Atom", command=self.update_Hydrogen)
        menu_boton.menu.add_command(label="Exit", command=self.exit)
        
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

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ₁(x) = x * e^(-α * x²)", command=lambda: Q_O.Psi("psi1"))
        self.psi_trial.menu.add_command(label="ψ₂(x) = 1 / (α * x² + 1)²", command=lambda: Q_O.Psi("psi2"))
        self.psi_trial.menu.add_command(label="ψ₃(x) = 1 / (x² + α)", command=lambda: Q_O.Psi("psi3"))
        self.psi_trial.menu.add_command(label="ψ₄(x) = 1 / (x² + α²)", command=lambda: Q_O.Psi("psi4"))
        self.psi_trial.menu.add_command(label="ψ₅(x) = 1 / (x² + α²)²", command=lambda: Q_O.Psi("psi5"))
        self.psi_trial.menu.add_command(label="ψ₆(x) = (x²) / (x² + α)²", command=lambda: Q_O.Psi("psi6"))

        self.graph_O_A()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    
    def update_psi_trial_particleinbox(self):
        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 1")
        self.psi_trial.menu.add_command(label="ψ(x) = 2")
        self.psi_trial.menu.add_command(label="ψ(x) = 3")
        self.psi_trial.menu.add_command(label="ψ(x) = 4")
        
        self.box()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
    

    
    def update_potential(self):
        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 5")
        self.psi_trial.menu.add_command(label="ψ(x) = 6")
        self.psi_trial.menu.add_command(label="ψ(x) = 7")

        self.potential()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
 

    def update_Anarmonic(self):

        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 8")
        self.psi_trial.menu.add_command(label="ψ(x) = 9")

        self.Anaharmonic()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
 

    def update_Hydrogen(self):
        self.psi_trial.menu.delete(0, tk.END)
        self.psi_trial.menu.add_command(label="ψ(x) = 10", command=self.O_A)
        self.psi_trial.menu.add_command(label="ψ(x) = 11")

        self.hydrogen()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


    def get_lr(self):
        return self.lr.get()

    def get_ep(self):
        return self.epochs.get()

    def O_A(self):
        self.clean()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


    def diagram(self):
        self.clean()
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        f1 = np.sin(x)
        f2 = np.exp(-x**2)
        f22 = np.exp(-10**x**2)
        f222 = np.exp(-3*x**2)
        f3 = np.tan(x)

        plt.subplot(2, 2, 1)
        plt.plot(x, f1, color='#000000', label="f1")
        plt.xlim(-2*np.pi, 2*np.pi)
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        

        plt.subplot(2, 2, 2)
        plt.plot(x, f2, color='#000000', label="f2")
        plt.plot(x, f22, color=colors["olive"], label="f22")
        plt.plot(x, f222, color=colors["dark_green"], label="f222")
        plt.xlim(-2*np.pi, 2*np.pi)
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
    

        plt.subplot(2, 2, (3, 4))
        plt.plot(x, f3, color='gray', label="f3")
        plt.xlim(-2*np.pi, 2*np.pi)
        plt.axhline(0, color='gray', linestyle='-', linewidth=1)
        plt.axvline(0, color='gray', linestyle='-', linewidth=1)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

        #plt.tight_layout()
        plt.subplots_adjust(wspace=0.3)
        plt.subplots_adjust(hspace=0.4)

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

    def resize_frames(self, event):
        global_width = self.window.winfo_width()
        new_global_width = global_width // 3
        self.left_half.configure(width=new_global_width)
        self.right_half.configure(width=2*new_global_width)

    def About(self):
        self.clean()
        

        colors = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
                  "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}
        
        plt.rcParams["toolbar"] = "none"
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
        plt.axis("off")
        
        plt.rcParams["text.usetex"] = True  # Habilitar LaTeX
        plt.rcParams["font.serif"] = ["Times New Roman"]
        
            # xy = punto de destino 
        # xytext = lugar del texto 
        
        font_params = {"fontsize": 16, "fontweight": "bold", "fontstyle": "italic"}
        

        an0 = ax.annotate(r"$\{V(\vec{r}),~ \psi_{test}\}$", xy=(0.15, 0.85), xycoords="data",
                          va="center", ha="center", 
                          bbox=dict(boxstyle="round", fc="w", linestyle="-"),
                          arrowprops=dict(arrowstyle="->"),
                          xytext=(0.15, 0.85), **font_params)
        
        
        an1 = ax.annotate(r"$E[\psi_{test}] = \frac{\langle \psi_{test} | \hat{H} | \psi_{test} \rangle}{\langle \psi_{test} | \psi_{test} \rangle} \geq E_0$",
                          xy=(0.15, 0.65), xycoords="data",
                          va="center", ha="center",
                          bbox=dict(boxstyle="round", fc="w", linestyle="-"),
                          arrowprops=dict(arrowstyle="->"),
                          xytext=(0.15, 0.65), **font_params)
        
        an2 = ax.annotate(r"$E(\theta^{(t)}, \mu^{(t)})$", 
                          xy=(0.15, 0.45), xycoords="data",
                          va="center", ha="center",
                          bbox=dict(boxstyle="round", fc=colors["dark_green"], edgecolor=colors["dark_green"], alpha=0.5),
                          arrowprops=dict(arrowstyle="->", connectionstyle="angle, angleA=90, angleB=180, rad=0"),
                          xytext=(0.15, 0.45), **font_params)
        
        
        an3 = ax.annotate(r"$\theta^{(t+1)} = \theta^{(t)} - \eta_{\theta}\nabla_{\theta} E(\theta, \mu)$" "\n" r"$\mu^{(t+1)} = \mu^{(t)} - \eta_{\mu}\nabla_{\mu} E(\theta, \mu)$",
                          xy=(0.75, 0.2), xycoords="data",
                          va="center", ha="center",
                          bbox=dict(boxstyle="round", fc="w"),
                          arrowprops=dict(arrowstyle="->", connectionstyle="angle, angleA=90, angleB=180, rad=0"),
                          xytext=(0.75, 0.2), **font_params)
        
        an4 = ax.annotate(r"$\eta_{\theta}, Iter$", xy=(0.37, 0.35), xycoords="data",
                          va="center", ha="center", 
                          bbox=dict(boxstyle="round", fc="w", linestyle="--"),
                          arrowprops=dict(arrowstyle="->"),
                          xytext=(0.37, 0.35), **font_params)
        
        an5 = ax.annotate(r"$E_{0}$", xy=(0.75, 0.45), xycoords="data",
                          va="center", ha="center", 
                          bbox=dict(boxstyle="round", fc="w"),
                          arrowprops=dict(arrowstyle="->"),
                          xytext=(0.75, 0.45), **font_params)
        
        an5 = ax.annotate(r"$H_{0}\psi_{test} - E_{0}\Psi_{test}=0$", xy=(0.75, 0.65), xycoords="data",
                  va="center", ha="center", 
                  bbox=dict(boxstyle="round", fc="w"),
                  arrowprops=dict(arrowstyle="->"),
                  xytext=(0.75, 0.65), **font_params)



        plt.rcParams["text.usetex"] = False

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)
        

    def exit(self):
        self.window.quit()

    def draw(self):
        self.clean()
        #self.text_label.config(text="Hello Aliens! How's it going?")
        E_1, dE_1 = Q_O.calculate_energy()
        Q_O.plot_energy(E_1, dE_1)
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
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
    
    def Anaharmonic(self):
        
        self.clean()
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator

        x = np.linspace(-1.79, 1.79, 50)
        y = np.linspace(-1.79, 1.79, 50)
        x, y = np.meshgrid(x, y)
        
        m, w, l = 1, 1, 1
        
        v = (1/2)*m*w*(x**2+y**2) + l*(x**4+y**4)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot_wireframe(x, y, v, color="black", alpha=0.5)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('V(x)')
        ax.set_title(r"$V(x, y) = \frac{1}{2}m\omega (x^{2}+y^{2}) + \lambda (x^{4}+y^{4})$")
        
        ax.view_init(elev=10, azim=135)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor('black')
        ax.yaxis.pane.set_edgecolor('black')
        ax.zaxis.pane.set_edgecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        ax.xaxis.set_major_locator(MultipleLocator(4))
        ax.yaxis.set_major_locator(MultipleLocator(4))
        ax.zaxis.set_major_locator(MultipleLocator(4))
        
        ax.xaxis._axinfo['tick']['inward_factor'] = 0
        ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.yaxis._axinfo['tick']['inward_factor'] = 0
        ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.zaxis._axinfo['tick']['inward_factor'] = 0
        ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
        
    def box(self):
        self.clean()
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator

        points = np.array([
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ])
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Crear una malla de puntos
        r = [-1, 1]
        X, Y = np.meshgrid(r, r)
        
        # Definir Z como una matriz con valores constantes
        Z1 = np.ones_like(X)
        Z2 = -np.ones_like(X)
        
        # Dibujar los wireframes de las paredes
        ax.plot_surface(X, Y, Z1,color='black', alpha=0.2)
        ax.plot_surface(X, Y, Z2,color='black', alpha=0.2)
        ax.plot_surface(X, -1*Y, Z1, color='black', alpha=0.2)
        ax.plot_surface(X, -1*Y, Z2, color='black', alpha=0.2)
        ax.plot_surface(Z1, X, Y, color='black',alpha=0.2)
        ax.plot_surface(Z2, X, Y, color='black', alpha=0.2)
        
        # Graficar los puntos
        ax.scatter3D(points[:, 0], points[:, 1], points[:, 2], color="black", marker=".")
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.set_title('V(x, y, z) = 0 si 0 ≤ x ≤ L_x, 0 ≤ y ≤ L_y, 0 ≤ z ≤ L_z; ∞ en otro caso')
        ax.set_xlim(-0.96, 0.96)
        ax.set_ylim(-0.96, 0.96)
        ax.set_zlim(-0.96, 0.96)
        
        
        ax.view_init(elev=10, azim=135)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor('black')
        ax.yaxis.pane.set_edgecolor('black')
        ax.zaxis.pane.set_edgecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
                 
        ax.xaxis.set_major_locator(MultipleLocator(4))
        ax.yaxis.set_major_locator(MultipleLocator(4))
        ax.zaxis.set_major_locator(MultipleLocator(4))
                 
        ax.xaxis._axinfo['tick']['inward_factor'] = 0
        ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.yaxis._axinfo['tick']['inward_factor'] = 0
        ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.zaxis._axinfo['tick']['inward_factor'] = 0
        ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
 

    def potential(self):
        
        self.clean()
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator

        # Definir los rangos de x y y
        x = np.linspace(-1.79, 1.79, 50)
        y = np.linspace(-1.79, 1.79, 50)
        x, y = np.meshgrid(x, y)
        
        # Definir el potencial
        v = (x**2 - 1)**2 - x**2
        
        # Crear la figura y el gráfico 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Graficar la superficie
        ax.plot_wireframe(x, y, v, color="black", alpha=0.5)
        
        # Etiquetas de los ejes
        ax.set_title(r"$V(x, y) = (x^{2}-1)^{2}-x^{2}$")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('V(x)')
        
        ax.view_init(elev=10, azim=135)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor('black')
        ax.yaxis.pane.set_edgecolor('black')
        ax.zaxis.pane.set_edgecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        ax.xaxis.set_major_locator(MultipleLocator(4))
        ax.yaxis.set_major_locator(MultipleLocator(4))
        ax.zaxis.set_major_locator(MultipleLocator(4))
        
        ax.xaxis._axinfo['tick']['inward_factor'] = 0
        ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.yaxis._axinfo['tick']['inward_factor'] = 0
        ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.zaxis._axinfo['tick']['inward_factor'] = 0
        ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
        


    def graph_O_A(self, m=1, w=1, x_range=(-1, 1), y_range=(-1, 1), grid_points=50):
        
        self.clean()

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator


        def V_O(x):
            return 0.5 * m * w**2 * x**2

        x = np.linspace(x_range[0], x_range[1], grid_points)
        y = np.linspace(y_range[0], y_range[1], grid_points)

        X, Y = np.meshgrid(x, y)
        Z = V_O(X) + V_O(Y)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_wireframe(X, Y, Z, color="black", alpha=0.5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('V(x, y)')
        ax.set_title(r"$V(x, y) = \frac{1}{2}m\omega^{2}(x^{2}+y^{2})$")

        ax.view_init(elev=20, azim=135)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor('black')
        ax.yaxis.pane.set_edgecolor('black')
        ax.zaxis.pane.set_edgecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.zaxis.set_major_locator(MultipleLocator(1))

        ax.xaxis._axinfo['tick']['inward_factor'] = 0
        ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.yaxis._axinfo['tick']['inward_factor'] = 0
        ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.zaxis._axinfo['tick']['inward_factor'] = 0
        ax.zaxis._axinfo['tick']['outward_factor'] = 0.4

        
   
    def graph_3D(self):
        self.clean()

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator

        color = {"black":"#000000", "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}
        plt.rcParams['toolbar'] = 'none'

        alpha = np.linspace(-5, 5, 100)
        beta = np.linspace(-5, 5, 100)
        
        alpha, beta = np.meshgrid(alpha, beta)
        m, w, h = 1.0, 1.0, 1.0
        
        E = 0.25 * alpha * m * w**2 + 0.5 * beta**2 * m * w**2 + h**2 / (4 * alpha * m)
        
        min_E = np.min(E)
        min_indices = np.unravel_index(np.argmin(E, axis=None), E.shape)
        min_alpha = alpha[min_indices]
        min_beta = beta[min_indices]
        
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot_wireframe(alpha, beta, E, color=color["black"], linewidth=0.5, alpha=0.5)
        
        ax.scatter(min_alpha, min_beta, min_E, color=color["purple"], s=50, label='Mínimo')
        ax.contour(alpha, beta, E, zdir='z', offset=ax.get_zlim()[0], colors=color["black"], alpha=0.7)
        
        
        ax.set_xlabel(r'$\alpha$')
        ax.set_ylabel(r'$\beta$')
        ax.set_zlabel(r'$E(\alpha, \beta)$')
        ax.set_title(r'$E = 0.25 \alpha m w^{2} + 0.5 \beta^{2} m w^{2} + \frac{h^{2}}{4 \alpha m}$')
        
        ax.view_init(elev=20, azim=135)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor('black')
        ax.yaxis.pane.set_edgecolor('black')
        ax.zaxis.pane.set_edgecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.zaxis.set_major_locator(MultipleLocator(5))
        
        ax.xaxis._axinfo['tick']['inward_factor'] = 0
        ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.yaxis._axinfo['tick']['inward_factor'] = 0
        ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.zaxis._axinfo['tick']['inward_factor'] = 0
        ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.right_half)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)


    def hydrogen(self):

        self.clean()
        
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import MultipleLocator
        
        e = 1.602e-19  # carga del electrón en Coulombs
        epsilon_0 = 8.854e-12  # permitividad del vacío en Faradios por metro
       
        def potential(x, y, z):
            r = np.sqrt(x**2 + y**2 + z**2)
            return -e**2 / (4 * np.pi * epsilon_0 * r)
        
        x = np.linspace(-1, 1, 50)
        y = np.linspace(-1, 1, 50)
        X, Y = np.meshgrid(x, y)
        
        z_val = 0
        Z = np.full_like(X, z_val)
        
        V = potential(X, Y, Z)
        
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_wireframe(X, Y, V, color="black", alpha=0.5)
        ax.contour(X, Y, V, zdir='z',levels=30,  offset=ax.get_zlim()[0], colors="black", alpha=0.7)
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('$V(x, y)$')
        ax.set_title(r"$V(x, y) = -\frac{e^2}{4 \pi \epsilon_0 \sqrt{x^2 + y^2}}$")
        
        ax.view_init(elev=25, azim=135)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor('black')
        ax.yaxis.pane.set_edgecolor('black')
        ax.zaxis.pane.set_edgecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
                 
        ax.xaxis.set_major_locator(MultipleLocator(4))
        ax.yaxis.set_major_locator(MultipleLocator(4))
        ax.zaxis.set_major_locator(MultipleLocator(4))
                 
        ax.xaxis._axinfo['tick']['inward_factor'] = 0
        ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.yaxis._axinfo['tick']['inward_factor'] = 0
        ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
        ax.zaxis._axinfo['tick']['inward_factor'] = 0
        ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
 

if __name__ == "__main__":


    window = tk.Tk()
    window.config(bg="#FFFFFF")
    window.minsize(1000, 500)
    app = Gui(window=window)
    Q_O = QuantumOscillator(app)
    window.mainloop()
