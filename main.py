import tkinter as tk
from tkinter import messagebox

# ------------------ ESTRUCTURAS ------------------

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    def __init__(self):
        self.inicio = None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            temp = self.inicio
            while temp.siguiente:
                temp = temp.siguiente
            temp.siguiente = nuevo
            nuevo.anterior = temp

    def recorrer(self):
        lista = []
        temp = self.inicio
        while temp:
            lista.append(temp.dato)
            temp = temp.siguiente
        return lista


inventario = ListaDoble()
pila_ventas = []

# ------------------ COLORES ------------------
COLOR_FONDO = "#1e1e2f"
COLOR_TEXTO = "#ffffff"
COLOR_INPUT = "#2a2a40"

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

        inventario.agregar(cel)
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
    temp = inventario.inicio

    while temp:
        cel = temp.dato
        texto.insert(tk.END,
            f"{cel['nombre']} - {cel['marca']} | "
            f"Precio: {cel['precio']} | RAM: {cel['memoria']}GB | "
            f"Cámara: {cel['camara']}MP | Procesador: {cel['procesador']} | "
            f"Almacenamiento: {cel['almacenamiento']}GB | "
            f"Cantidad: {cel['cantidad']}\n"
        )
        temp = temp.siguiente


def vender_celular():
    nombre = entry_buscar.get()
    temp = inventario.inicio

    while temp:
        cel = temp.dato
        if cel["nombre"].lower() == nombre.lower():
            cel["cantidad"] -= 1

            # Pila (LIFO)
            pila_ventas.append(cel.copy())

            if cel["cantidad"] <= 0:
                if temp.anterior:
                    temp.anterior.siguiente = temp.siguiente
                if temp.siguiente:
                    temp.siguiente.anterior = temp.anterior
                if temp == inventario.inicio:
                    inventario.inicio = temp.siguiente

            messagebox.showinfo("Venta", "Venta realizada")
            mostrar_inventario()
            return

        temp = temp.siguiente

    messagebox.showerror("Error", "Celular no encontrado")


def mostrar_pila():
    texto.delete("1.0", tk.END)

    if not pila_ventas:
        texto.insert(tk.END, "No hay ventas\n")
        return

    texto.insert(tk.END, "Historial (último vendido primero):\n\n")

    for cel in reversed(pila_ventas):
        texto.insert(tk.END,
            f"{cel['nombre']} - {cel['marca']} | Precio: {cel['precio']}\n"
        )


#  RECOMENDACIÓN
def recomendar():
    texto.delete("1.0", tk.END)

    lista = inventario.recorrer()

    if not lista:
        texto.insert(tk.END, "No hay celulares\n")
        return

    seleccion = opcion.get()

    if seleccion == "precio":
        lista.sort(key=lambda x: x["precio"], reverse=True)
        for cel in lista:
            texto.insert(tk.END,
                f"{cel['nombre']} - Precio: {cel['precio']}\n"
            )

    elif seleccion == "camara":
        lista.sort(key=lambda x: x["camara"], reverse=True)
        for cel in lista:
            texto.insert(tk.END,
                f"{cel['nombre']} - Cámara: {cel['camara']}MP\n"
            )

    elif seleccion == "procesador":
        lista.sort(key=lambda x: x["procesador"], reverse=True)
        for cel in lista:
            texto.insert(tk.END,
                f"{cel['nombre']} - Procesador: {cel['procesador']}\n"
            )

    elif seleccion == "ram":
        lista.sort(key=lambda x: x["memoria"], reverse=True)
        for cel in lista:
            texto.insert(tk.END,
                f"{cel['nombre']} - RAM: {cel['memoria']}GB\n"
            )

    elif seleccion == "almacenamiento":
        lista.sort(key=lambda x: x["almacenamiento"], reverse=True)
        for cel in lista:
            texto.insert(tk.END,
                f"{cel['nombre']} - Almacenamiento: {cel['almacenamiento']}GB\n"
            )

    else:
        texto.insert(tk.END, "Seleccione una opción\n")


# ------------------ INTERFAZ ------------------

ventana = tk.Tk()
ventana.title("Sistema de Celulares")
ventana.geometry("900x600")
ventana.configure(bg=COLOR_FONDO)

frame_izq = tk.Frame(ventana, bg=COLOR_FONDO)
frame_izq.pack(side="left", fill="y", padx=10, pady=10)

frame_der = tk.Frame(ventana, bg=COLOR_FONDO)
frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(frame_izq, text="INVENTARIO",
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

def crear_entry(label):
    tk.Label(frame_izq, text=label,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    e = tk.Entry(frame_izq, bg=COLOR_INPUT, fg="white")
    e.pack()
    return e

entry_nombre = crear_entry("Nombre")
entry_marca = crear_entry("Marca")
entry_procesador = crear_entry("Procesador 1-10 CALIFICACION")
entry_memoria = crear_entry("RAM")
entry_camara = crear_entry("Cámara")
entry_almacenamiento = crear_entry("Almacenamiento")
entry_precio = crear_entry("Precio")
entry_cantidad = crear_entry("Cantidad")

tk.Button(frame_izq, text="Agregar", command=agregar_celular).pack(pady=5)
tk.Button(frame_izq, text="Mostrar", command=mostrar_inventario).pack(pady=5)

tk.Label(frame_izq, text="VENTA",
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

entry_buscar = tk.Entry(frame_izq)
entry_buscar.pack()

tk.Button(frame_izq, text="Vender", command=vender_celular).pack(pady=5)

tk.Button(frame_izq, text="Ver Ventas", command=mostrar_pila).pack(pady=5)

tk.Label(frame_izq, text="RECOMENDACIÓN",
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

opcion = tk.StringVar()

tk.Radiobutton(frame_izq, text="Precio", value="precio", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")

tk.Radiobutton(frame_izq, text="Cámara", value="camara", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")

tk.Radiobutton(frame_izq, text="Procesador", value="procesador", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")

tk.Radiobutton(frame_izq, text="RAM", value="ram", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")

tk.Radiobutton(frame_izq, text="Almacenamiento", value="almacenamiento", variable=opcion,
               bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")

tk.Button(frame_izq, text="Recomendar", command=recomendar).pack(pady=10)

tk.Label(frame_der, text="RESULTADOS",
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

texto = tk.Text(frame_der)
texto.pack(fill="both", expand=True)

ventana.mainloop()
