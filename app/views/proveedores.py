import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.proveedor import *

def ProveedoresView(container, navegar):
    container.configure(bg="#F4F7F6")

    # --- LISTA DE SERVICIOS ---
    servicios_proveedores = [
        "CATERING Y BANQUETERÍA", "ALQUILER DE MOBILIARIO", "SONIDO E ILUMINACIÓN PROFESIONAL",
        "DECORACIÓN Y DISEÑO DE ESPACIOS", "FOTOGRAFÍA Y VIDEO (FILMACIÓN)",
        "REPOSTERÍA Y PASTELES TEMÁTICOS", "SERVICIOS DE COCTELERÍA Y BARRA LIBRE",
        "FLORISTERÍA Y ARREGLOS ORNAMENTALES", "ENTRETENIMIENTO (DJS, BANDAS, SHOWS)",
        "ALQUILER DE CARPAS Y ESTRUCTURAS", "LOGÍSTICA Y PERSONAL (MESEROS, HOSTS)",
        "EFECTOS ESPECIALES (PIROTECNIA, HUMO)", "TRANSPORTE Y TRASLADOS PRIVADOS",
        "SEGURIDAD PRIVADA Y PROTOCOLO", "SISTEMAS DE REGISTRO Y ACREDITACIÓN",
        "REGALOS EMPRESARIALES Y MERCHANDISING", "ALQUILER DE EQUIPOS AUDIOVISUALES (PANTALLAS LED)",
        "SERVICIOS DE LIMPIEZA POST-EVENTO"
    ]

    # --- HEADER ---
    header = tk.Frame(container, bg="#F4F7F6", pady=20)
    header.pack(fill="x", padx=40)
    tk.Label(header, text="🚚 Gestión de Proveedores", font=("Segoe UI", 20, "bold"), bg="#F4F7F6", fg="#2C3E50").pack(side="left")
    tk.Button(header, text="← Volver", command=lambda: navegar("inicio"), bg="#BDC3C7", bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")

    # --- CONTENIDO ---
    main_content = tk.Frame(container, bg="#F4F7F6")
    main_content.pack(fill="both", expand=True, padx=40, pady=10)

    # Panel Formulario (Diseño Slim)
    form_frame = tk.LabelFrame(main_content, text=" Datos del Proveedor ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15)
    form_frame.pack(side="left", fill="y", padx=(0, 15))

    id_sel = tk.StringVar(value="")
    
    # Campos de entrada normales
    fields = [("empresa", "Empresa:"), ("telefono", "Teléfono:"), ("email", "Email:"), ("costoServicio", "Costo del Servicio")]
    entries = {}

    for key, txt in fields:
        tk.Label(form_frame, text=txt, bg="white", fg="#7F8C8D", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5,0))
        entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F9F9F9", highlightthickness=1, highlightbackground="#E0E0E0", relief="flat", width=28)
        entry.pack(fill="x", ipady=3, pady=5)
        entries[key] = entry

    # --- NUEVO: CAMPO SERVICIO (OptionMenu) ---
    tk.Label(form_frame, text="Servicio / Producto:", bg="white", fg="#7F8C8D", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0))
    servicio_var = tk.StringVar(value=servicios_proveedores[0])
    
    menu_servicios = tk.OptionMenu(form_frame, servicio_var, *servicios_proveedores)
    menu_servicios.config(bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#E0E0E0", font=("Segoe UI", 9), anchor="w")
    menu_servicios["menu"].config(font=("Segoe UI", 9))
    menu_servicios.pack(fill="x", pady=5)

    # --- LÓGICA DE FUNCIONES ---
    def cargar_tabla():
        for item in tabla.get_children(): tabla.delete(item)
        for p in listarProovedoresController():
            tabla.insert("", tk.END, values=(p[0], p[1], p[2], p[3], p[4], p[5]))

    def guardar():
        emp, tel, mail, cost = entries["empresa"].get(), entries["telefono"].get(), entries["email"].get(), entries["costoServicio"].get()
        serv = servicio_var.get() # Tomamos el valor del menú desplegable
        
        if id_sel.get() == "":
            if crearProovedorController(emp, tel, mail, serv, cost): 
                messagebox.showinfo("Éxito", "Proveedor registrado"); limpiar()
        else:
            if actualizarProovedorController(id_sel.get(), emp, tel, mail, serv, cost):
                messagebox.showinfo("Éxito", "Proveedor actualizado"); limpiar()
        cargar_tabla()

    def limpiar():
        id_sel.set("")
        for e in entries.values(): e.delete(0, tk.END)
        servicio_var.set(servicios_proveedores[0]) # Reset al primer elemento
        btn_save.config(text="Registrar Proveedor", bg="#27AE60")

    def borrar():
        if id_sel.get() and messagebox.askyesno("Confirmar", "¿Eliminar este proveedor?"):
            eliminarProovedorController(id_sel.get())
            limpiar(); cargar_tabla()

    # Botones de acción
    btn_save = tk.Button(form_frame, text="Registrar Proveedor", bg="#27AE60", fg="white", font=("Segoe UI", 10, "bold"), command=guardar, bd=0, pady=10, cursor="hand2")
    btn_save.pack(fill="x", pady=10)
    tk.Button(form_frame, text="Limpiar / Nuevo", command=limpiar, bg="#BDC3C7", bd=0, cursor="hand2").pack(fill="x")

    # --- TABLA ---
    table_frame = tk.Frame(main_content, bg="white", highlightthickness=1, highlightbackground="#E0E0E0")
    table_frame.pack(side="right", fill="both", expand=True)

    cols = ("ID", "Empresa", "Teléfono", "Email", "Servicio/Producto", "Costo del Servicio")
    tabla = ttk.Treeview(table_frame, columns=cols, show="headings")
    
    for col in cols:
        tabla.heading(col, text=col.upper())
        # Ajustamos el ancho de la columna de servicio por ser texto largo
        ancho = 200 if col == "Servicio/Producto" else 100
        tabla.column(col, width=ancho)

    scrolly = ttk.Scrollbar(table_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrolly.set)
    scrolly.pack(side="right", fill="y")
    tabla.pack(side="left", fill="both", expand=True)

    def on_select(e):
        item = tabla.selection()
        if item:
            v = tabla.item(item, "values")
            id_sel.set(v[0])
            entries["empresa"].delete(0, tk.END); entries["empresa"].insert(0, v[1])
            entries["telefono"].delete(0, tk.END); entries["telefono"].insert(0, v[2])
            entries["email"].delete(0, tk.END); entries["email"].insert(0, v[3])
            servicio_var.set(v[4])
            entries["costoServicio"].delete(0, tk.END); entries["costoServicio"].insert(0, v[5])
            btn_save.config(text="Actualizar Proveedor", bg="#3498DB")

    tabla.bind("<<TreeviewSelect>>", on_select)

    tk.Button(container, text="🗑 Eliminar Proveedor Seleccionado", bg="#E74C3C", fg="white", font=("Segoe UI", 10, "bold"), command=borrar, bd=0, padx=20, pady=10, cursor="hand2").pack(pady=20)

    cargar_tabla()