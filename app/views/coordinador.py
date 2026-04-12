import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.coordinador import listarCoordinadoresController, crearCoordinadorController, actualizarCoordinadorController, eliminarCoordinadorController

def CoordinadoresView(container, navegar):
    container.configure(bg="#F4F7F6")

    # --- HEADER ---
    header = tk.Frame(container, bg="#F4F7F6", pady=20)
    header.pack(fill="x", padx=40)

    tk.Label(header, text="👔 Gestión de Coordinadores", font=("Segoe UI", 20, "bold"), bg="#F4F7F6", fg="#2C3E50").pack(side="left")
    tk.Button(header, text="Volver", font=("Segoe UI", 10, "bold"), bg="#BDC3C7", bd=0, padx=15, pady=5, cursor="hand2", command=lambda: navegar("inicio")).pack(side="right")
    
    # --- CONTENIDO ---
    main_content = tk.Frame(container, bg="#F4F7F6")
    main_content.pack(fill="both", expand=True, padx=40, pady=10)

    form_frame = tk.LabelFrame(main_content, text=" Datos del Coordinador ", font=("Segoe UI", 10, "bold"), bg="white", padx=20, pady=20)
    form_frame.pack(side="left", fill="y", padx=(0, 20))

    id_sel = tk.StringVar(value="")
    entries = {}

    # --- CAMPOS NORMALES (Entry) ---
    campos_texto = [("nombre", "Nombre:"), ("nuip", "NUIP:"), ("salario", "Salario ($):")]
    
    for key, txt in campos_texto:
        tk.Label(form_frame, text=txt, bg="white", fg="#7F8C8D").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#F9F9F9", highlightthickness=1, highlightbackground="#E0E0E0", relief="flat")
        entry.pack(fill="x", ipady=5, pady=5)
        entries[key] = entry

    # --- CAMPO ESTADO (OptionMenu) ---
    tk.Label(form_frame, text="Estado:", bg="white", fg="#7F8C8D").pack(anchor="w", pady=(5, 0))
    estado_opcion = tk.StringVar(value="DISPONIBLE")
    opciones = ["DISPONIBLE", "OCUPADO"]
    
    menu_estado = tk.OptionMenu(form_frame, estado_opcion, *opciones)
    menu_estado.config(bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#E0E0E0", font=("Segoe UI", 10))
    menu_estado.pack(fill="x", pady=5)

    # --- FUNCIONES ---
    def cargar_tabla():
        for item in tabla.get_children(): tabla.delete(item)
        for c in listarCoordinadoresController():
            tabla.insert("", tk.END, values=c)

    def guardar():
        n = entries["nombre"].get()
        ni = entries["nuip"].get()
        e = estado_opcion.get()
        s = entries["salario"].get()
        
        if id_sel.get() == "":
            if crearCoordinadorController(n, ni, e, s): limpiar()
        else:
            if actualizarCoordinadorController(id_sel.get(), n, ni, e, s): limpiar()
        cargar_tabla()

    def limpiar():
        id_sel.set("")
        for e in entries.values(): e.delete(0, tk.END)
        estado_opcion.set("DISPONIBLE") # Reset del menú
        btn_save.config(text="Registrar", bg="#27AE60")

    def borrar():
        if id_sel.get() and messagebox.askyesno("Confirmar", "¿Eliminar coordinador?"):
            eliminarCoordinadorController(id_sel.get())
            limpiar()
            cargar_tabla()

    btn_save = tk.Button(form_frame, text="Registrar", bg="#27AE60", fg="white", font=("Segoe UI", 11, "bold"), command=guardar, bd=0, pady=10, cursor="hand2")
    btn_save.pack(fill="x", pady=10)
    tk.Button(form_frame, text="Nuevo / Limpiar", command=limpiar, bg="#BDC3C7", bd=0, cursor="hand2").pack(fill="x")

    # --- TABLA ---
    table_frame = tk.Frame(main_content, bg="white")
    table_frame.pack(side="right", fill="both", expand=True)

    cols = ("id", "nombre", "nuip", "estado", "salario")
    tabla = ttk.Treeview(table_frame, columns=cols, show="headings")
    for col in cols: 
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=100)
    tabla.pack(side="left", fill="both", expand=True)

    def on_select(e):
        item = tabla.selection()
        if item:
            val = tabla.item(item, "values")
            id_sel.set(val[0])
            entries["nombre"].delete(0, tk.END); entries["nombre"].insert(0, val[1])
            entries["nuip"].delete(0, tk.END); entries["nuip"].insert(0, val[2])
            entries["salario"].delete(0, tk.END); entries["salario"].insert(0, val[4])
            estado_opcion.set(val[3])
            
            btn_save.config(text="Actualizar Datos", bg="#3498DB")

    tabla.bind("<<TreeviewSelect>>", on_select)

    tk.Button(container, text="🗑 Eliminar Seleccionado", bg="#E74C3C", fg="white", font=("Segoe UI", 10, "bold"), command=borrar, bd=0, padx=20, pady=10, cursor="hand2").pack(pady=20)

    cargar_tabla()