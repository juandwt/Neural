import tkinter as tk    
import matplotlib.pyplot as plt


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


window = tk.Tk()
window.config(bg="#FFFFFF")
window.minsize(600, 400)
window_height = 500 #window.winfo_screenwidth()  
window_width  = 500
#window_height = 500

width_half = window_height // 3

window.bind("<Configure>", resize_frames)


left_half = tk.Frame(window, bg="#4a6c65", width=width_half, height=window_height)
left_half.pack(side="left", expand=True, fill="both")

right_half = tk.Frame(window, bg="#FFFFFF", width=width_half, height=window_width)
right_half.pack(side="right", expand=True, fill="both")

Exit = tk.Button(left_half, text="EXIT", fg="#FFFFFF", command=Exit)
Exit.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
Exit.place(relx=0.6, rely=0.6, anchor="center")  # Centrar el botón en la mitad derecha

Draw = tk.Button(left_half, text="Draw", fg="#FFFFFF", command=Draw)
Draw.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")  
Draw.place(relx=0.4, rely=0.6, anchor="center")

Graph = tk.Button(left_half, text="Graph", fg="#FFFFFF")
Graph.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief="flat")
Graph.place(relx=0.5, rely=0.7, anchor="center")

text_label = tk.Label(left_half, text="", bg="#4a6c65", fg="white", width=30)
text_label.pack(expand=True)
text_label.place(relx=0.5, rely=0.5, anchor="center")


window.mainloop()
