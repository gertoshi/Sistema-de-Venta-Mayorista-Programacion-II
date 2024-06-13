import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

contador_ventas = 1
productos_mostrados = False


def moduloVenta(vent_madre):
    vent_madre.withdraw()

    def buscar_producto():
        entrada = entryBuscador.get().strip()
        if entrada.isdigit():
            buscar_por_id(int(entrada))
        else:
            buscar_por_nombre(entrada)

    def buscar_por_id(id_busqueda):
        for item in listaProductos.get_children():
            listaProductos.delete(item)
        with open("productos.json", "r") as file:
            productos = json.load(file)
            for producto in productos:
                if producto["Codigo"] == id_busqueda:
                    listaProductos.insert("", "end", values=(
                        producto['Codigo'], producto['Descripcion'], producto['Precio'], producto['Cantidad']))
                    break
            else:
                listaProductos.insert("", "end", values=(
                    "No se encontró ningún producto con ese ID.", "", "", ""))

    def buscar_por_nombre(nombre_busqueda):
        for item in listaProductos.get_children():
            listaProductos.delete(item)
        with open("productos.json", "r") as file:
            productos = json.load(file)
            for producto in productos:
                if nombre_busqueda.lower() in producto["Descripcion"].lower():
                    listaProductos.insert("", "end", values=(
                        producto['Codigo'], producto['Descripcion'], producto['Precio'], producto['Cantidad']))
            if not listaProductos.get_children():
                listaProductos.insert("", "end", values=(
                    "No se encontró ningún producto con ese nombre.", "", "", ""))

    def traer_productos():
        with open("productos.json", "r") as file:
            productos = json.load(file)
        return productos

    def mostrar_productos():
        for item in listaProductos.get_children():
            listaProductos.delete(item)
        global productos_mostrados
        productos = traer_productos()
        if productos:
            for producto in productos:
                listaProductos.insert("", "end", values=(
                    producto['Codigo'], producto['Descripcion'], producto['Precio'], producto['Cantidad']))
            productos_mostrados = True

    def mover_a_carrito():
        cantidad_seleccionada = entryCantidad.get()
        if not cantidad_seleccionada:
            messagebox.showerror(
                "Error", "Por favor, ingresa la cantidad a comprar.")
            return
        cantidad_seleccionada = int(cantidad_seleccionada)

        seleccion = listaProductos.selection()
        if seleccion:
            item = listaProductos.item(seleccion[0])
            codigo, descripcion, precio, stock = item['values']
            stock = int(stock)
            if cantidad_seleccionada > 0 and cantidad_seleccionada <= stock:
                carritoProductos.insert("", "end", values=(
                    codigo, descripcion, precio, cantidad_seleccionada))
                listaProductos.delete(seleccion[0])
                actualizar_stock(codigo, cantidad_seleccionada)
                actualizar_total()
            elif cantidad_seleccionada <= 0:
                messagebox.showerror(
                    "Error", "La cantidad a comprar debe ser mayor que cero.")
            else:
                messagebox.showerror(
                    "Error", "La cantidad a comprar es mayor que la cantidad disponible en stock")
            entryCantidad.delete(0, tk.END)

    def actualizar_total():
        total = 0
        for item in carritoProductos.get_children():
            producto = carritoProductos.item(item)['values']
            cantidad_comprada = int(producto[3])
            precio_producto = float(producto[2])
            total += cantidad_comprada * precio_producto
        totalProducto.config(text=f"${total}")

    def actualizar_stock(codigo, cantidad):
        with open("productos.json", "r+") as file:
            productos = json.load(file)
            for producto in productos:
                if producto["Codigo"] == int(codigo):
                    producto["Cantidad"] -= cantidad
                    file.seek(0)
                    json.dump(productos, file, indent=4)
                    file.truncate()
                    break

    def eliminar_de_carrito():
        seleccion = carritoProductos.selection()
        if seleccion:
            item = carritoProductos.item(seleccion[0])
            codigo, descripcion, precio, cantidad = item['values']
            with open("productos.json", "r+") as file:
                productos = json.load(file)
                for producto in productos:
                    if producto["Codigo"] == int(codigo):
                        producto["Cantidad"] += int(cantidad)
                        file.seek(0)
                        json.dump(productos, file, indent=4)
                        file.truncate()
                        break
            carritoProductos.delete(seleccion[0])
            listaProductos.insert("", "end", values=(
                codigo, descripcion, precio, producto["Cantidad"]))
            actualizar_total()

    def obtener_ultimo_id_venta():
        try:
            with open("venta.json", "r") as file:
                data = json.load(file)
                ventas = data.get("ventas", [])
                if ventas:
                    ultimo_id = ventas[-1]["id_venta"]
                    return ultimo_id + 1
        except FileNotFoundError:
            pass
        return 0

    def actualizar_json(elementos_carrito):
        id_venta = obtener_ultimo_id_venta()
        nueva_venta = {
            "id_venta": id_venta,
            "elementos_carrito": [],
            "venta_total": 0
        }
        total_venta = 0
        try:
            with open("venta.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if 'ventas' not in data:
            data['ventas'] = []

        for item in elementos_carrito:
            codigo, descripcion, precio, cantidad_comprada = item
            precio_total = float(precio) * int(cantidad_comprada)
            venta_producto = {
                "Codigo": int(codigo),
                "Descripcion": descripcion,
                "Cantidad": int(cantidad_comprada),
                "Precio_Unitario": float(precio),
                "Precio_Total": precio_total
            }
            nueva_venta["elementos_carrito"].append(venta_producto)
            total_venta += precio_total

        nueva_venta["venta_total"] = total_venta

        data["ventas"].append(nueva_venta)

        with open("venta.json", "w") as file:
            json.dump(data, file, indent=4)

    def guardar_ventas():
        total = 0
        elementos_carrito = []
        for item in carritoProductos.get_children():
            producto = carritoProductos.item(item)['values']
            codigo = int(producto[0])
            descripcion = producto[1]
            precio = float(producto[2])
            cantidad_comprada = int(producto[3])

            elementos_carrito.append(
                (codigo, descripcion, precio, cantidad_comprada))

        actualizar_json(elementos_carrito)
        carritoProductos.delete(*carritoProductos.get_children())
        totalProducto.config(text="$0")
        messagebox.showinfo("Venta realizada",
                            "La venta se ha realizado correctamente.")

    def salirModuloVenta():
        ventanaPrincipal.destroy()
        vent_madre.deiconify()

    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.title("Venta de Productos")
    ventanaPrincipal.geometry("1200x600")
    ventanaPrincipal.configure(bg="#F794A4")

    ventanaPrincipal.resizable(0, 0)

    botonBuscar = Button(ventanaPrincipal, text="Traer todos los Productos", height=1, width=24,
                         bg="#A2626D", fg="black", font=("Comic Sans", 10, "bold"), command=mostrar_productos)
    botonBuscar.place(x=90, y=55)

    labelBuscador = tk.Label(
        ventanaPrincipal, text="Buscar por ID o por producto:", font=("Comic Sans", 10))
    labelBuscador.place(x=108, y=120)

    entryBuscador = tk.Entry(ventanaPrincipal)
    entryBuscador.place(x=130, y=150)

    botonBuscarProducto = Button(ventanaPrincipal, text="BUSCAR", height=2, width=10,
                                 bg="white", fg="black", font=("Comic Sans", 10, "bold"), command=buscar_producto)
    botonBuscarProducto.place(x=145, y=180)

    botonSalir = Button(ventanaPrincipal, text="SALIR", height=2, width=10,
                        bg="white", fg="black", font=("Comic Sans", 10, "bold"), command=salirModuloVenta)
    botonSalir.place(x=145, y=250)

    columns = ("ID", "Descripcion", "Precio", "Cantidad")
    listaProductos = ttk.Treeview(
        ventanaPrincipal, columns=columns, show="headings")
    for col in columns:
        listaProductos.heading(col, text=col)
        listaProductos.column(col, width=1)
    listaProductos.place(x=400, y=10, width=650, height=250)

    carritoProductos = ttk.Treeview(
        ventanaPrincipal, columns=columns, show="headings")
    for col in columns:
        carritoProductos.heading(col, text=col)
        carritoProductos.column(col, width=1)
    carritoProductos.place(x=400, y=280, width=650, height=250)

    botonEliminar = Button(ventanaPrincipal, text="ELIMINAR", height=2, width=10, bg="red",
                           fg="white", font=("Comic Sans", 10, "bold"), command=eliminar_de_carrito)
    botonEliminar.place(x=50, y=350)

    botonAgregar = Button(ventanaPrincipal, text="AGREGAR", height=2, width=10,
                          bg="blue", fg="white", font=("Comic Sans", 10, "bold"), command=mover_a_carrito)
    botonAgregar.place(x=200, y=350)

    botonCobro = Button(ventanaPrincipal, text="$ COBRAR", height=3, width=10,
                        bg="green", fg="white", font=("Comic Sans", 10, "bold"), command=guardar_ventas)
    botonCobro.place(x=130, y=450)

    etiquetaTotal = tk.Label(ventanaPrincipal, text="TOTAL: ", font=(
        "Comic Sans", 24, "bold"), bg="#F794A4")
    etiquetaTotal.place(x=500, y=550)

    totalProducto = tk.Label(ventanaPrincipal, text=f"$", font=(
        "Comic Sans", 28, "bold"), bg="#F794A4")
    totalProducto.place(x=650, y=545)

    etiquetaCantidad = tk.Label(
        ventanaPrincipal, text="Cantidad:", font=("Comic Sans", 10, "bold"))
    etiquetaCantidad.place(x=1080, y=60)
    entryCantidad = tk.Entry(ventanaPrincipal, width=10)
    entryCantidad.place(x=1080, y=90)

    ventanaPrincipal.mainloop()
