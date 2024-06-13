import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

productos = []


def cargar_datos():
    try:
        with open("productos.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_datos(data):
    with open("productos.json", "w") as file:
        json.dump(data, file, indent=4)


def registrar_movimiento(tipo, producto, cantidad_anterior=0):
    movimiento = {
        "tipo": tipo,
        "producto": producto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cantidad_anterior": cantidad_anterior
    }
    try:
        with open("movimientos.json", "r") as file:
            movimientos = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        movimientos = []

    movimientos.append(movimiento)
    with open("movimientos.json", "w") as file:
        json.dump(movimientos, file, indent=4)


def gestion_corta(vent_madre):
    vent_madre.withdraw()

    def cargar_datos_treeview(treeview):
        for item in treeview.get_children():
            treeview.delete(item)
        for producto in productos:
            treeview.insert("", tk.END, values=(producto["Codigo"], producto["Descripcion"], producto["Precio"], producto["Cantidad"]))

    def dar_alta_producto():
        ventana_alta_producto = tk.Toplevel()
        ventana_alta_producto.title("Alta Producto")
        ventana_alta_producto.geometry("600x300")
        ventana_alta_producto.config(bg="#F794A4")
        ventana_alta_producto.resizable(0, 0)

        etiquetas = ["Descripcion", "Precio", "Cantidad"]
        entries = []

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(ventana_alta_producto, text=f"{etiqueta}: ", font="Arial 12", bg="#F794A4").grid(
                row=i, column=0)
            entry = tk.Entry(ventana_alta_producto, width=70) if etiqueta == "Descripcion" else tk.Entry(
                ventana_alta_producto, width=30)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def guardar_producto():
            datos = [entry.get().strip() for entry in entries]

            if datos[0] == "":
                messagebox.showerror(
                    "Advertencia", "Por favor, ingrese una descripción.")
                return

            if "" in datos[1:]:
                messagebox.showerror(
                    "Advertencia", "Por favor, ingrese valores válidos.")
                return

            try:
                precio = float(datos[1])
                cantidad = int(datos[2])
            except ValueError:
                messagebox.showerror(
                    "Advertencia", "El precio y la cantidad deben ser valores numéricos.")
                return

            ultimo_codigo = productos[-1]["Codigo"] if productos else 0
            nuevo_producto = {
                "Descripcion": datos[0].upper(),
                "Codigo": ultimo_codigo + 1,
                "Precio": precio,
                "Cantidad": cantidad
            }
            productos.append(nuevo_producto)
            guardar_datos(productos)
            registrar_movimiento("alta", nuevo_producto)
            cargar_datos_treeview(treeview)
            ventana_alta_producto.destroy()

        tk.Button(ventana_alta_producto, text="CONFIRMAR", font="Arial 12",
                  bg="light green", command=guardar_producto).grid(row=3, column=1)
        tk.Button(ventana_alta_producto, text="CANCELAR", font="Arial 12",
                  bg="dark red", command=ventana_alta_producto.destroy).grid(row=4, column=1)

    def modificar_producto():
        seleccion = treeview.selection()
        if seleccion:
            item = treeview.item(seleccion[0])
            producto_seleccionado = next(
                (prod for prod in productos if prod["Codigo"] == item["values"][0]), None)
            cantidad_anterior = producto_seleccionado["Cantidad"]

            def guardar_cambios():
                nueva_descripcion = entry_descripcion.get().strip()
                if nueva_descripcion == "":
                    messagebox.showerror(
                        "Error", "La descripción no puede estar en blanco.")
                    return

                producto_seleccionado["Descripcion"] = nueva_descripcion.upper(
                )
                producto_seleccionado["Precio"] = float(entry_precio.get())
                producto_seleccionado["Cantidad"] = int(entry_cantidad.get())
                guardar_datos(productos)
                registrar_movimiento(
                    "modificacion", producto_seleccionado, cantidad_anterior)
                cargar_datos_treeview(treeview)
                ventana_modificar_producto.destroy()

            ventana_modificar_producto = tk.Toplevel()
            ventana_modificar_producto.title("Modificar Producto")
            ventana_modificar_producto.geometry("600x300")
            ventana_modificar_producto.config(bg="#F794A4")
            ventana_modificar_producto.resizable(False, False)

            tk.Label(ventana_modificar_producto, text="Descripcion: ",
                     font="Arial 12", bg="#F794A4").grid(row=0, column=0)
            tk.Label(ventana_modificar_producto, text="Precio: ",
                     font="Arial 12", bg="#F794A4").grid(row=1, column=0)
            tk.Label(ventana_modificar_producto, text="Cantidad: ",
                     font="Arial 12", bg="#F794A4").grid(row=2, column=0)

            entry_descripcion = tk.Entry(ventana_modificar_producto, width=70)
            entry_descripcion.grid(row=0, column=1)
            entry_descripcion.insert(0, producto_seleccionado["Descripcion"])

            entry_precio = tk.Entry(ventana_modificar_producto, width=30)
            entry_precio.grid(row=1, column=1)
            entry_precio.insert(0, producto_seleccionado["Precio"])

            entry_cantidad = tk.Entry(ventana_modificar_producto, width=30)
            entry_cantidad.grid(row=2, column=1)
            entry_cantidad.insert(0, producto_seleccionado["Cantidad"])

            tk.Button(ventana_modificar_producto, text="Guardar Cambios",
                      bg="#A2626D", command=guardar_cambios).grid(row=3, column=1)
        else:
            messagebox.showerror(
                "Error", "Por favor, seleccione un producto primero.")

    def eliminar_producto():
        seleccion = treeview.selection()
        if seleccion:
            item = treeview.item(seleccion[0])
            producto_eliminado = next(
                (prod for prod in productos if prod["Codigo"] == item["values"][0]), None)
            cantidad_anterior = producto_eliminado["Cantidad"]
            productos.remove(producto_eliminado)
            guardar_datos(productos)
            registrar_movimiento("baja", producto_eliminado, cantidad_anterior)
            cargar_datos_treeview(treeview)
            messagebox.showinfo(
                "Eliminado", "Producto eliminado correctamente.")
        else:
            messagebox.showerror(
                "Error", "Por favor, seleccione un producto primero.")

    def salir_gestion_producto():
        ventana_producto.destroy()
        vent_madre.deiconify()

    # Crear la ventana principal
    ventana_producto = tk.Toplevel()
    ventana_producto.title("Gestión de Productos")
    ventana_producto.geometry("1200x600")
    ventana_producto.resizable(0, 0)
    ventana_producto.configure(bg="#F794A4")

    # Crear y configurar el Treeview
    columns = ("ID", "Descripcion", "Precio", "Cantidad")
    treeview = ttk.Treeview(
        ventana_producto, columns=columns, show="headings", height=25)
    treeview.heading("ID", text="ID")
    treeview.heading("Descripcion", text="Descripcion")
    treeview.heading("Precio", text="Precio")
    treeview.heading("Cantidad", text="Cantidad")
    treeview.grid(row=1, column=0, columnspan=4, sticky="nsew")

    # Ajustar el tamaño de las columnas
    for col in columns:
        treeview.column(col, width=300)

    # Cargar datos al iniciar la aplicación
    productos = cargar_datos()
    cargar_datos_treeview(treeview)

    # Crear y configurar los botones
    tk.Button(ventana_producto, text="Ingresar Producto", command=dar_alta_producto, bg="#A2626D", height=3, width=20).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(ventana_producto, text="Modificar Producto", command=modificar_producto,
              bg="#A2626D", height=3, width=20).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(ventana_producto, text="Eliminar Producto", command=eliminar_producto,
              bg="#A2626D", height=3, width=20).grid(row=2, column=2, padx=5, pady=5)
    tk.Button(ventana_producto, text="Salir", command=salir_gestion_producto,
              bg="#A2626D", height=3, width=20).grid(row=2, column=3, padx=5, pady=5)

    ventana_producto.mainloop()
