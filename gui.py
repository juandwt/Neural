import tkinter as tk

def resize_frames(event):
    # Obtener el ancho actual de la ventana
    ancho_actual = ventana.winfo_width()

    # Calcular el nuevo ancho de la mitad izquierda
    nuevo_ancho_izquierda = ancho_actual // 3

    # Configurar el nuevo ancho de la mitad izquierda
    mitad_izquierda.configure(width=nuevo_ancho_izquierda)

ventana = tk.Tk()
ventana.config(bg="#FFFFFF")

# Configurar tamaño mínimo de la ventana
ventana.minsize(600, 400)

# Calcular las dimensiones de los marcos
ancho_ventana = ventana.winfo_screenwidth()
alto_ventana = 500

ancho_mitad = ancho_ventana // 2

mitad_izquierda = tk.Frame(ventana, bg="#FFFFFF", width=ancho_mitad, height=alto_ventana)
mitad_izquierda.pack(side="left", expand=True, fill="both")

mitad_derecha = tk.Frame(ventana, bg="#4a6c65", width=ancho_mitad, height=alto_ventana)
mitad_derecha.pack(side="right", expand=True, fill="both")

boton = tk.Button(mitad_derecha, text="Presionar", fg="#FFFFFF")
boton.config(bg="#4a6c65", borderwidth=0, highlightthickness=0, relief='flat')
boton.place(relx=0.5, rely=0.5, anchor="center")  # Centrar el botón en la mitad derecha

# Asociar la función resize_frames al evento de cambio de tamaño de la ventana
ventana.bind("<Configure>", resize_frames)

ventana.mainloop()
