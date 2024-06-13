import tkinter as tk
import json
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
from time import strftime


def cargar_usuarios():
    try:
        with open('usuarios.json', "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}


def guardar_usuarios(usuarios):
    with open('usuarios.json', "w") as archivo:
        json.dump(usuarios, archivo, indent=4)


def actualizar_treeview(treeview, usuarios):
    for usuario in treeview.get_children():
        treeview.delete(usuario)
    for usuario, info in usuarios.items():
        treeview.insert("", "end", values=(
            info["nombre"], info["apellido"], info["dni"], usuario, info["cargo"], info["alta"]))


def modulo_usuario(vent_madre):
    vent_madre.withdraw()

    def confirmacion():

        nombre = usuario_nombre_input.get()
        apellido = usuario_apellido_input.get()
        dni = usuario_dni_input.get()
        nombre_empleado = usuario_nombre_empleado_input.get()
        contrasena_empleado = usuario_contraseña_input.get()
        cargo = tipo_usuario.get()
        usuarios = cargar_usuarios()
        if not nombre.isalpha():
            messagebox.showerror(
                "Error", "El Nombre solo puede contener letras.")
            return
        if not apellido.isalpha():
            messagebox.showerror(
                "Error", "El Apellido solo puede contener letras.")
            return
        if not dni.isdigit():
            messagebox.showerror(
                "Error", "El DNI solo puede contener números.")
            return
        if len(dni) != 8:
            messagebox.showerror("Error", "El DNI debe contener 8 números.")
            return
        if len(nombre) >= 1 and len(apellido) >= 1 and len(dni) >= 1:
            if len(nombre_empleado) >= 1:
                if len(contrasena_empleado) >= 6 and len(cargo) > 1:
                    if nombre_empleado not in usuarios:
                        fecha = strftime(" %d/%m/%y")
                        nuevo_usuario = {
                            "nombre": nombre,
                            "apellido": apellido,
                            "dni": dni,
                            "cargo": cargo,
                            "usuario": nombre_empleado,
                            "contrasena": contrasena_empleado,
                            "alta": fecha
                        }
                        # Agregar el nuevo usuario al diccionario existente
                        usuarios[nombre_empleado] = nuevo_usuario
                        # Guardar todos los usuarios (incluyendo el nuevo) en el archivo JSON
                        guardar_usuarios(usuarios)
                        actualizar_treeview(treeview, usuarios)

                        mensaje_.config(
                            text=f"Usuario '{nombre_empleado}' agregado con éxito.", foreground="blue")
                        usuario_apellido_input.delete(0, tk.END)
                        usuario_dni_input.delete(0, tk.END)
                        usuario_nombre_empleado_input.delete(0, tk.END)
                        usuario_contraseña_input.delete(0, tk.END)
                        tipo_usuario.set("")

                    else:
                        mensaje_.config(
                            text=f"El usuario '{nombre_empleado}' ya existe.", foreground="red")
                        messagebox.showerror(
                            "Error: ", f"El usuario '{nombre_empleado}' ya existe.")
                else:
                    messagebox.showerror(
                        "Error: ", "La contraseña debe tener al menos 6 caracteres.")
            else:
                messagebox.showerror(
                    "Error: ", "Ingrese un usuario y contraseña.")
        else:
            messagebox.showerror(
                "Error: ", "Ingrese todos los datos del usuario.")

    def eliminar_usuario():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror(
                "Error", "Seleccione un usuario para eliminar.")
            return
        usuario = treeview.item(selected_item, "values")[3]
        respuesta = messagebox.askyesno(
            "Confirmación", f"¿Está seguro de que desea eliminar el usuario '{usuario}'?")
        if respuesta:
            usuarios = cargar_usuarios()
            if usuario in usuarios:
                del usuarios[usuario]
                guardar_usuarios(usuarios)
                actualizar_treeview(treeview, usuarios)
                messagebox.showinfo(
                    "Información", f"Usuario '{usuario}' eliminado con éxito.")
            else:
                messagebox.showerror(
                    "Error", f"El usuario '{usuario}' no se encontró.")

    def modificar_usuario():

        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror(
                "Error", "Seleccione un usuario para modificar.")
            return
        usuario = treeview.item(selected_item, "values")[3]
        usuarios = cargar_usuarios()

        def modificado():
            nombre = usuario_nombre_input.get()
            apellido = usuario_apellido_input.get()
            dni = usuario_dni_input.get()
            nombre_empleado = usuario_nombre_empleado_input.get()
            contrasena_empleado = usuario_contraseña_input.get()
            cargo = tipo_usuario.get()
            usuarios = cargar_usuarios()
            if not nombre.isalpha():
                messagebox.showerror(
                    "Error", "El Nombre solo puede contener letras.")
                return
            if not apellido.isalpha():
                messagebox.showerror(
                    "Error", "El Apellido solo puede contener letras.")
                return
            if not dni.isdigit():
                messagebox.showerror(
                    "Error", "El DNI solo puede contener números.")
                return
            if len(dni) != 8:
                messagebox.showerror(
                    "Error", "El DNI debe contener 8 números.")
                return
            if len(nombre) >= 1 and len(apellido) >= 1 and len(dni) >= 1:
                if len(nombre_empleado) >= 1:
                    if len(contrasena_empleado) >= 6 and len(cargo) > 1:
                        if nombre_empleado in usuarios:
                            nuevo_usuario = {
                                "nombre": nombre,
                                "apellido": apellido,
                                "dni": dni,
                                "cargo": cargo,
                                "usuario": nombre_empleado,
                                "contrasena": contrasena_empleado,
                                "alta": alta
                            }
                            usuarios[nombre_empleado] = nuevo_usuario
                            # Guardar todos los usuarios (incluyendo el nuevo) en el archivo JSON
                            guardar_usuarios(usuarios)
                            actualizar_treeview(treeview, usuarios)

                            mensaje_.config(
                                text=f"Usuario '{nombre_empleado}' modificado con éxito.", foreground="blue")
                            boton.destroy()
                            usuario_nombre_input.delete(0, tk.END)
                            usuario_apellido_input.delete(0, tk.END)
                            usuario_dni_input.delete(0, tk.END)
                            usuario_nombre_empleado_input.delete(0, tk.END)
                            usuario_contraseña_input.delete(0, tk.END)
                            tipo_usuario.set("")

                        else:
                            mensaje_.config(
                                text=f"El usuario '{nombre_empleado}' ya existe.", foreground="red")
                            messagebox.showerror(
                                "Error: ", f"El usuario '{nombre_empleado}' ya existe.")
                    else:
                        messagebox.showerror(
                            "Error: ", "La contraseña debe tener al menos 6 caracteres.")
                else:
                    messagebox.showerror(
                        "Error: ", "Ingrese un usuario y contraseña.")
            else:
                messagebox.showerror(
                    "Error: ", "Ingrese todos los datos del usuario.")

        boton = tk.Button(frame_formulario, text="Modificar Datos",
                          command=modificado, font=("Bookman", 14))
        boton.grid(row=3, column=0, sticky="news", padx=20, pady=20)
        if usuario in usuarios:
            info = usuarios[usuario]
            usuario_nombre_input.delete(0, END)
            usuario_nombre_input.insert(0, info["nombre"])
            usuario_apellido_input.delete(0, END)
            usuario_apellido_input.insert(0, info["apellido"])
            usuario_dni_input.delete(0, END)
            usuario_dni_input.insert(0, info["dni"])
            usuario_nombre_empleado_input.delete(0, END)
            usuario_nombre_empleado_input.insert(0, info["usuario"])
            usuario_contraseña_input.delete(0, END)
            usuario_contraseña_input.insert(0, info["contrasena"])
            tipo_usuario.set(info["cargo"])
            alta = info["alta"]

    def SalirModuloRegistro():
        ventana1.destroy()
        vent_madre.deiconify()

    ventana1 = tk.Tk()
    ventana1.title("Añadir Usuario")

    frame_formulario = tk.Frame(ventana1)
    frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame_lista = tk.Frame(ventana1)
    frame_lista.grid(row=0, column=1, padx=0, pady=10, sticky="nsew")
    # Información del usuario
    usuario_informacion_frame = ttk.LabelFrame(
        frame_formulario, text="Información de Usuario")
    usuario_informacion_frame.grid(row=0, column=0, padx=10, pady=20)

    # Campos de entrada de datos personales
    tk.Label(usuario_informacion_frame, text="Nombre",
             font=("Bookman", 14)).grid(row=0, column=0)
    usuario_nombre_input = tk.Entry(
        usuario_informacion_frame, font=("Bookman", 14))
    usuario_nombre_input.grid(row=1, column=0, pady=10, padx=10)

    tk.Label(usuario_informacion_frame, text="Apellido",
             font=("Bookman", 14)).grid(row=0, column=1)
    usuario_apellido_input = tk.Entry(
        usuario_informacion_frame, font=("Bookman", 14))
    usuario_apellido_input.grid(row=1, column=1, pady=20, padx=10)

    tk.Label(usuario_informacion_frame, text="DNI",
             font=("Bookman", 14)).grid(row=2, column=0)
    usuario_dni_input = tk.Entry(
        usuario_informacion_frame, font=("Bookman", 14))
    usuario_dni_input.grid(row=3, column=0, pady=20, padx=10)

    # Campos de entrada de datos de acceso
    tk.Label(usuario_informacion_frame, text="Nombre de Usuario",
             font=("Bookman", 14)).grid(row=2, column=1)
    usuario_nombre_empleado_input = tk.Entry(
        usuario_informacion_frame, font=("Bookman", 14))
    usuario_nombre_empleado_input.grid(row=3, column=1, pady=20, padx=10)

    tk.Label(usuario_informacion_frame, text="Contraseña",
             font=("Bookman", 14)).grid(row=4, column=0)
    usuario_contraseña_input = tk.Entry(
        usuario_informacion_frame, show="*", font=("Bookman", 14))
    usuario_contraseña_input.grid(row=5, column=0, pady=20, padx=10)

    # Selección de cargo
    tipo_usua = ttk.LabelFrame(frame_formulario, text="Seleccione su cargo")
    tipo_usua.grid(row=1, column=0, padx=20, pady=20)
    opciones = ["Administrador", "Empleado"]
    tipo_usuario = Combobox(
        tipo_usua, width=13, values=opciones, state="readonly", font=("Bookman", 19))
    tipo_usuario.pack()

    # Botón de confirmación
    boton = tk.Button(frame_formulario, text="Guardar Datos",
                      command=confirmacion, font=("Bookman", 14))
    boton.grid(row=6, column=0, sticky="news", padx=20, pady=20)

    botonSalir = tk.Button(frame_formulario, text="Salir",
                           command=SalirModuloRegistro, font=("Bookman", 14))
    botonSalir.grid(row=7, column=0, sticky="news", padx=20, pady=20)

    mensaje_ = tk.Label(frame_formulario, text="", foreground="red")
    mensaje_.grid()

    # Treeview para mostrar los datos de los usuarios
    treeview = ttk.Treeview(frame_lista, columns=(
        "Nombre", "Apellido", "DNI", "Usuario", "Cargo", "Fecha de Alta"), show="headings")
    treeview.heading("Nombre", text="Nombre")
    treeview.heading("Apellido", text="Apellido")
    treeview.heading("DNI", text="DNI")
    treeview.heading("Usuario", text="Usuario")
    treeview.heading("Cargo", text="Cargo")
    treeview.heading("Fecha de Alta", text="alta")
    treeview.grid(row=0, column=0, columnspan=2,
                  padx=20, pady=20, sticky="nsew")

    # Configurar scrollbar
    scrollbar = tk.Scrollbar(
        frame_lista, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=2, sticky="ns")

    treeview.config(yscrollcommand=scrollbar.set)

    # Botones para eliminar y modificar usuarios
    boton_eliminar = tk.Button(
        frame_lista, text="Eliminar Usuario", command=eliminar_usuario, font=("Bookman", 14))
    boton_eliminar.grid(row=1, column=0, padx=20, pady=10)

    boton_modificar = tk.Button(
        frame_lista, text="Modificar Usuario", command=modificar_usuario, font=("Bookman", 14))
    boton_modificar.grid(row=1, column=1, padx=20, pady=10)

    # Cargar usuarios existentes en el Treeview
    usuarios = cargar_usuarios()
    actualizar_treeview(treeview, usuarios)

    ventana1.mainloop()
