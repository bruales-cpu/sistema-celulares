import tkinter as tk
from tkinter import messagebox

inventario = []

# ------------------ COLORES ------------------
COLOR_FONDO = "#1e1e2f"
COLOR_TEXTO = "#ffffff"
COLOR_INPUT = "#2a2a40"
COLOR_BOTON = "#4CAF50"
COLOR_BOTON2 = "#2196F3"

# ------------------ FUNCIONES ------------------

def agregar_celular():
    try:
        if entry_nombre.get() == "" or entry_marca.get() == "":
            messagebox.showerror("Error", "Campos vacíos")
            return

        cel = {
            "nombre": entry_nombre.get(),
            "marca": entry_marca.get(),
            "procesador": int(entry_procesador.get()),
            "memoria": int(entry_memoria.get()),
            "camara": int(entry_camara.get()),
            "almacenamiento": int(entry_almacenamiento.get()),
            "precio": int(entry_precio.get()),
            "cantidad": int(entry_cantidad.get())
        }

        inventario.append(cel)
        messagebox.showinfo("Éxito", "Celular agregado")
        limpiar_campos()

    except ValueError:
        messagebox.showerror("Error", "Datos inválidos")


def limpiar_campos():
    for entry in [entry_nombre, entry_marca, entry_procesador,
                  entry_memoria, entry_camara, entry_almacenamiento,
                  entry_precio, entry_cantidad]:
        entry.delete(0, tk.END)


def mostrar_inventario():
    texto.delete("1.0", tk.END)
    for cel in inventario:
        texto.insert(tk.END,
            f"{cel['nombre']} - {cel['marca']} | "
            f"Proc: {cel['procesador']} | RAM: {cel['memoria']}GB | "
            f"Cam: {cel['camara']}MP | Alm: {cel['almacenamiento']}GB | "
            f"Precio: {cel['precio']} | Cantidad: {cel['cantidad']}\n"
        )


def vender_celular():
    nombre = entry_buscar.get()

    for i, cel in enumerate(inventario):
        if cel["nombre"].lower() == nombre.lower():
            inventario[i]["cantidad"] -= 1

            if inventario[i]["cantidad"] <= 0:
                inventario.pop(i)

            messagebox.showinfo("Venta", "Venta realizada")
            mostrar_inventario()
            return

    messagebox.showerror("Error", "Celular no encontrado")


# 🔥 RECOMENDACIÓN (UNA SOLA OPCIÓN)
def recomendar():
    texto.delete("1.0", tk.END)

    if not inventario:
        texto.insert(tk.END, "No hay celulares registrados\n")
        return

    lista = inventario.copy()
    seleccion = opcion.get()

    if seleccion == "precio":
        lista.sort(key=lambda x: x["precio"])
        for i, cel in enumerate(lista[:3], start=1):
            texto.insert(tk.END,
                f"{i}. {cel['nombre']} ({cel['marca']}) | Precio: {cel['precio']}\n"
            )

    elif seleccion == "camara":
        lista.sort(key=lambda x: x["camara"], reverse=True)
        for i, cel in enumerate(lista[:3], start=1):
            texto.insert(tk.END,
                f"{i}. {cel['nombre']} ({cel['marca']}) | Cámara: {cel['camara']}MP\n"
            )

    elif seleccion == "procesador":
        lista.sort(key=lambda x: x["procesador"], reverse=True)
        for i, cel in enumerate(lista[:3], start=1):
            texto.insert(tk.END,
                f"{i}. {cel['nombre']} ({cel['marca']}) | Procesador: {cel['procesador']}\n"
            )

    elif seleccion == "ram":
        lista.sort(key=lambda x: x["memoria"], reverse=True)
        for i, cel in enumerate(lista[:3], start=1):
            texto.insert(tk.END,
                f"{i}. {cel['nombre']} ({cel['marca']}) | RAM: {cel['memoria']}GB\n"
            )

    elif seleccion == "almacenamiento":
        lista.sort(key=lambda x: x["almacenamiento"], reverse=True)
        for i, cel in enumerate(lista[:3], start=1):
            texto.insert(tk.END,
                f"{i}. {cel['nombre']} ({cel['marca']}) | Almacenamiento: {cel['almacenamiento']}GB\n"
            )

    else:
        texto.insert(tk.END, "Seleccione una opción\n")


# ------------------ INTERFAZ ------------------

ventana = tk.Tk()
ventana.title("Sistema de Celulares")
ventana.geometry("900x600")
ventana.configure(bg=COLOR_FONDO)

# -------- CONTENEDORES --------
frame_izq = tk.Frame(ventana, bg=COLOR_FONDO)
frame_izq.pack(side="left", fill="y", padx=10, pady=10)

frame_der = tk.Frame(ventana, bg=COLOR_FONDO)
frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# -------- INVENTARIO --------
tk.Label(frame_izq, text="INVENTARIO",
         font=("Arial", 14, "bold"),
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

def crear_entry(label):
    tk.Label(frame_izq, text=label,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    e = tk.Entry(frame_izq, bg=COLOR_INPUT, fg="white", insertbackground="white")
    e.pack(pady=2)
    return e

entry_nombre = crear_entry("Nombre")
entry_marca = crear_entry("Marca")
entry_procesador = crear_entry("Procesador 1-10")
entry_memoria = crear_entry("RAM")
entry_camara = crear_entry("Cámara")
entry_almacenamiento = crear_entry("Almacenamiento")
entry_precio = crear_entry("Precio")
entry_cantidad = crear_entry("Cantidad")

tk.Button(frame_izq, text="Agregar", bg=COLOR_BOTON, fg="white",
          command=agregar_celular).pack(pady=5)

tk.Button(frame_izq, text="Mostrar", bg=COLOR_BOTON2, fg="white",
          command=mostrar_inventario).pack(pady=5)

# -------- VENTA --------
tk.Label(frame_izq, text="VENTA",
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)

entry_buscar = tk.Entry(frame_izq, bg=COLOR_INPUT, fg="white", insertbackground="white")
entry_buscar.pack()

tk.Button(frame_izq, text="Vender", bg="#ff9800", fg="white",
          command=vender_celular).pack(pady=5)

# -------- RECOMENDACIÓN --------
tk.Label(frame_izq, text="RECOMENDACIÓN",
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)

opcion = tk.StringVar()

tk.Radiobutton(frame_izq, text="Mejor Cámara", value="camara", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor="#333").pack(anchor="w")

tk.Radiobutton(frame_izq, text="Mejor Procesador", value="procesador", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor="#333").pack(anchor="w")

tk.Radiobutton(frame_izq, text="Más RAM", value="ram", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor="#333").pack(anchor="w")

tk.Radiobutton(frame_izq, text="Más Almacenamiento", value="almacenamiento", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor="#333").pack(anchor="w")

tk.Radiobutton(frame_izq, text="Más Económico", value="precio", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor="#333").pack(anchor="w")

tk.Button(frame_izq, text="Recomendar TOP 3", bg="#9c27b0", fg="white",
          command=recomendar).pack(pady=10)

# -------- RESULTADOS --------
tk.Label(frame_der, text="RESULTADOS",
         font=("Arial", 14, "bold"),
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

texto = tk.Text(frame_der, bg="#121212", fg="white")
texto.pack(fill="both", expand=True)

ventana.mainloop()