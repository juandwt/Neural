import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


color_1 = "#4a6c65"
color_2 = "#7B904B"

def sine(window): 
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = np.sin(x)
    Y = np.gradient(y, x)

    plt.subplot(2, 1, 1)
    plt.plot(x, y, color='#000000')
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.axhline(0, color='gray', linestyle='-', linewidth=1)  # Línea horizontal en y=0
    plt.axvline(0, color='gray', linestyle='-', linewidth=1)  # Línea vertical en x=0


    plt.subplot(2, 1, 2)
    plt.plot(x, Y, color='gray')
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.axhline(0, color='gray', linestyle='-', linewidth=1)  # Línea horizontal en y=0
    plt.axvline(0, color='gray', linestyle='-', linewidth=1)  # Línea vertical en x=0




    #plt.plot(x, y, color='#000000', ls='--')
    #plt.plot(x, Y, color='gray')
    #plt.xlim(0, 2*np.pi)
    
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill="both", expand=1)

def resize_frames(event):
    global_width = window.winfo_width()
    new_global_width = global_width // 3
    left_half.configure(width=new_global_width)
    right_half.configure(width=2*new_global_width)

# Funciones de los botones
def Exit():
    window.quit()

def Draw():
    text_label.config(text="Hello Aliens! How's it going?")

def Graph():
    sine(right_half)

window = tk.Tk()
window.config(bg="#FFFFFF")
window.minsize(600, 400)
window_height = 500 #window.winfo_screenwidth()  
window_width  = 500
#window_height = 500

width_half = window_height // 3

window.bind("<Configure>", resize_frames)

left_half = tk.Frame(window, bg=color_1, width=width_half, height=window_height)
left_half.pack(side="left", expand=True, fill="both")

right_half = tk.Frame(window, bg="#FFFFFF", width=width_half, height=window_width)
right_half.pack(side="right", expand=True, fill="both")

Exit = tk.Button(left_half, text="EXIT", fg="#FFFFFF", command=Exit)
Exit.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
Exit.place(relx=0.6, rely=0.6, anchor="center")  # Centrar el botón en la mitad derecha

Draw = tk.Button(left_half, text="Draw", fg="#FFFFFF", command=Draw)
Draw.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")  
Draw.place(relx=0.4, rely=0.6, anchor="center")

Graph = tk.Button(left_half, text="Graph", fg="#FFFFFF", command=Graph)
Graph.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
Graph.place(relx=0.5, rely=0.7, anchor="center")

text_label = tk.Label(left_half, text="", bg="#4a6c65", fg="white", width=30)
text_label.pack(expand=True)
text_label.place(relx=0.5, rely=0.5, anchor="center")


window.mainloop()
