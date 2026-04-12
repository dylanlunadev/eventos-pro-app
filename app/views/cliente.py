import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.cliente import (
    crearClienteController, 
    listarClientesController,
    actualizarClienteController,
    eliminarClienteController
)

def ClientesView(container, navegar):
    container.configure(bg="#F4F7F6")

    # --- HEADER ---
    header = tk.Frame(container, bg="#F4F7F6", pady=20)
    header.pack(fill="x", padx=40)
    
    tk.Label(header, text="👥 Gestión de Clientes", font=("Segoe UI", 20, "bold"), bg="#F4F7F6", fg="#2C3E50").pack(side="left")
    
    nav_btns = tk.Frame(header, bg="#F4F7F6")
    nav_btns.pack(side="right")
    tk.Button(nav_btns, text="➕ Nuevo usuario", command=lambda: navegar('login'), bg="#27AE60", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="left", padx=10)
    tk.Button(nav_btns, text="← Volver", command=lambda: navegar("inicio"), bg="#BDC3C7", bd=0, padx=15, pady=5, cursor="hand2").pack(side="left")

    # --- CONTENIDO PRINCIPAL ---
    main_content = tk.Frame(container, bg="#F4F7F6")
    main_content.pack(fill="both", expand=True, padx=40, pady=10)

    # --- PANEL IZQUIERDO: FORMULARIO (MÁS DELGADO) ---
    form_frame = tk.LabelFrame(main_content, text=" Datos del Cliente ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15, fg="#2C3E50")
    form_frame.pack(side="left", fill="y", padx=(0, 15))

    id_seleccionado = tk.StringVar(value="")
    
    # Configuración de campos de texto
    fields_config = [
        ("nombre", "Nombre Completo:"),
        ("email", "Correo Electrónico:"),
        ("telefono", "Teléfono:"),
        ("nuip", "Identificación (NUIP):"),
        ("nombreUsuario", "Usuario (@):") # Etiqueta más corta para ahorrar espacio
    ]

    entries = {}
    for key, label_text in fields_config:
        tk.Label(form_frame, text=label_text, bg="white", fg="#7F8C8D", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#E0E0E0", width=30)
        entry.pack(fill="x", ipady=3)
        entries[key] = entry

    def guardar():
        id_actual = id_seleccionado.get()
        nombre, email = entries["nombre"].get(), entries["email"].get()
        tel, nuip = entries["telefono"].get(), entries["nuip"].get()
        user = entries["nombreUsuario"].get()

        if id_actual == "":
            exito, _ = crearClienteController(nombre, email, tel, nuip, user)
        else:
            if messagebox.askyesno("Confirmar", "¿Deseas guardar los cambios?"):
                exito = actualizarClienteController(id_actual, nombre, email, tel, nuip)
            else: exito = False

        if exito:
            limpiar()
            cargar_datos_tabla()

    def limpiar():
        id_seleccionado.set("")
        for v in entries.values(): v.delete(0, tk.END)
        btn_guardar.config(text="Registrar Cliente", bg="#27AE60")

    btn_container = tk.Frame(form_frame, bg="white")
    btn_container.pack(fill="x", pady=15)

    btn_guardar = tk.Button(btn_container, text="Registrar Cliente", bg="#27AE60", fg="white", font=("Segoe UI", 10, "bold"), bd=0, pady=8, cursor="hand2", command=guardar)
    btn_guardar.pack(fill="x", pady=5)
    
    tk.Button(btn_container, text="Limpiar / Nuevo", bg="#BDC3C7", bd=0, pady=5, command=limpiar, cursor="hand2").pack(fill="x")

    # --- PANEL DERECHO: TABLA (MÁS ESPACIO) ---
    table_frame = tk.Frame(main_content, bg="white", highlightthickness=1, highlightbackground="#E0E0E0")
    table_frame.pack(side="right", fill="both", expand=True)

    columns = ("ID", "Nombre", "Email", "Teléfono", "NUIP", "Evento", "Usuario")
    tabla = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    for col in columns:
        tabla.heading(col, text=col.upper())
        # Ajustamos anchos automáticos
        anchos = {"ID": 40, "Nombre": 150, "Email": 150, "Teléfono": 100, "NUIP": 100, "Evento": 180, "Usuario": 100}
        tabla.column(col, width=anchos.get(col, 100), minwidth=50)

    # Scrollbar para la tabla
    scrolly = ttk.Scrollbar(table_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrolly.set)
    scrolly.pack(side="right", fill="y")
    tabla.pack(side="left", fill="both", expand=True)
    
    def al_seleccionar(event):
        item = tabla.selection()
        if item:
            val = tabla.item(item, "values")
            id_seleccionado.set(val[0])
            entries["nombre"].delete(0, tk.END); entries["nombre"].insert(0, val[1])
            entries["email"].delete(0, tk.END); entries["email"].insert(0, val[2])
            entries["telefono"].delete(0, tk.END); entries["telefono"].insert(0, val[3])
            entries["nuip"].delete(0, tk.END); entries["nuip"].insert(0, val[4])
            entries["nombreUsuario"].delete(0, tk.END); entries["nombreUsuario"].insert(0, val[5])
            btn_guardar.config(text="Actualizar Datos", bg="#3498DB")

    tabla.bind("<<TreeviewSelect>>", al_seleccionar)

    def cargar_datos_tabla():
        for item in tabla.get_children(): tabla.delete(item)
        clientes = listarClientesController()
        if clientes:
            for c in clientes:
                # c[7] es el nombreUsuario por el JOIN del modelo
                filtro = (c[0], c[1], c[2], c[3], c[4], c[6])
                tabla.insert("", tk.END, values=filtro)

    def borrar():
        if id_seleccionado.get():
            if messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
                eliminarClienteController(id_seleccionado.get())
                limpiar()
                cargar_datos_tabla()
        else:
            messagebox.showwarning("Atención", "Seleccione un cliente de la tabla")

    tk.Button(container, text="🗑 Eliminar Cliente Seleccionado", bg="#E74C3C", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=10, command=borrar, cursor="hand2").pack(pady=20)

    cargar_datos_tabla()