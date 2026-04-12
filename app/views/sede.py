import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.sede import *

def SedesView(container, navegar):
    container.configure(bg="#F4F7F6")

    # --- HEADER ---
    header = tk.Frame(container, bg="#F4F7F6", pady=20)
    header.pack(fill="x", padx=40)
    tk.Label(header, text="🏢 Gestión de Sedes", font=("Segoe UI", 20, "bold"), bg="#F4F7F6", fg="#2C3E50").pack(side="left")
    tk.Button(header, text="← Volver", command=lambda: navegar("inicio"), bg="#BDC3C7", bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")

    # --- CONTENIDO ---
    main_content = tk.Frame(container, bg="#F4F7F6")
    main_content.pack(fill="both", expand=True, padx=40, pady=10)

    # Panel Formulario Delgado
    form_frame = tk.LabelFrame(main_content, text=" Datos de la Sede ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15)
    form_frame.pack(side="left", fill="y", padx=(0, 15))

    id_sel = tk.StringVar(value="")
    fields = [("nombre", "Nombre:"), ("direccion", "Dirección:"), ("capacidad", "Capacidad:"), ("costo", "Costo Alquiler ($):")]
    entries = {}

    for key, txt in fields:
        tk.Label(form_frame, text=txt, bg="white", fg="#7F8C8D", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5,0))
        entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F9F9F9", highlightthickness=1, highlightbackground="#E0E0E0", relief="flat", width=25)
        entry.pack(fill="x", ipady=3, pady=5)
        entries[key] = entry

    # --- LÓGICA ---
    def cargar_tabla():
        for item in tabla.get_children(): tabla.delete(item)
        for s in listarSedesController():
            tabla.insert("", tk.END, values=s)

    def guardar():
        n, d, c, co = entries["nombre"].get(), entries["direccion"].get(), entries["capacidad"].get(), entries["costo"].get()
        if id_sel.get() == "":
            if crearSedeController(n, d, c, co): 
                messagebox.showinfo("Éxito", "Sede guardada"); limpiar()
        else:
            if actualizarSedeController(id_sel.get(), n, d, c, co):
                messagebox.showinfo("Éxito", "Sede actualizada"); limpiar()
        cargar_tabla()

    def limpiar():
        id_sel.set("")
        for e in entries.values(): e.delete(0, tk.END)
        btn_save.config(text="Registrar Sede", bg="#27AE60")

    def borrar():
        if id_sel.get() and messagebox.askyesno("Confirmar", "¿Eliminar esta sede?"):
            eliminarSedeController(id_sel.get())
            limpiar(); cargar_tabla()

    # Botones
    btn_save = tk.Button(form_frame, text="Registrar Sede", bg="#27AE60", fg="white", font=("Segoe UI", 10, "bold"), command=guardar, bd=0, pady=8, cursor="hand2")
    btn_save.pack(fill="x", pady=10)
    tk.Button(form_frame, text="Limpiar", command=limpiar, bg="#BDC3C7", bd=0, cursor="hand2").pack(fill="x")

    # --- TABLA ---
    table_frame = tk.Frame(main_content, bg="white", highlightthickness=1, highlightbackground="#E0E0E0")
    table_frame.pack(side="right", fill="both", expand=True)

    cols = ("ID", "Nombre", "Dirección", "Capacidad", "Costo")
    tabla = ttk.Treeview(table_frame, columns=cols, show="headings")
    for col in cols:
        tabla.heading(col, text=col.upper())
        tabla.column(col, width=100)

    scrolly = ttk.Scrollbar(table_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrolly.set)
    scrolly.pack(side="right", fill="y")
    tabla.pack(side="left", fill="both", expand=True)

    def on_select(e):
        item = tabla.selection()
        if item:
            v = tabla.item(item, "values")
            id_sel.set(v[0])
            for i, key in enumerate(["nombre", "direccion", "capacidad", "costo"]):
                entries[key].delete(0, tk.END); entries[key].insert(0, v[i+1])
            btn_save.config(text="Actualizar Sede", bg="#3498DB")

    tabla.bind("<<TreeviewSelect>>", on_select)

    tk.Button(container, text="🗑 Eliminar Seleccionada", bg="#E74C3C", fg="white", font=("Segoe UI", 10, "bold"), command=borrar, bd=0, padx=20, pady=10, cursor="hand2").pack(pady=20)

    cargar_tabla()