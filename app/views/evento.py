import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.evento import *

def EventosView(container, rol, navegar, username):
    for widget in container.winfo_children():
        widget.destroy()
    if rol == "ADMIN":
        EventosViewAdmin(container, navegar)
    else:
        EventosViewCliente(container, navegar, username)

def EventosViewAdmin(container, navegar):
    colors = {
        "primary": "#34495E",    # Azul Grisáceo (Header)
        "secondary": "#2C3E50",  # Azul Oscuro (Formulario)
        "bg": "#f0f0f0",         # Gris Claro (Fondo)
        "accent": "#A9C462",     # Verde (Guardar)
        "danger": "#D96459",     # Rojo (Eliminar)
        "warning": "#E9B872",    # Amarillo/Naranja
        "info": "#709CA7"        # Azul Aqua (Actualizar/Volver)
    }

    container.config(bg=colors["bg"])

    eventos = [
        "LANZAMIENTO DE PRODUCTO", "CONFERENCIA / SEMINARIO", "CONGRESO O CONVENCIÓN",
        "TEAM BUILDING / INTEGRACIÓN", "FIESTA DE FIN DE AÑO", "WORKSHOP / TALLER",
        "BODA (MATRIMONIO)", "FIESTA DE QUINCEAÑERA", "BABY SHOWER",
        "FIESTA DE GRADUACIÓN (PROM)", "ANIVERSARIO", "FIESTA DE CUMPLEAÑOS",
        "CONCIERTO / RECITAL", "EXPOSICIÓN DE ARTE", "FESTIVAL GASTRONÓMICO",
        "DESFILE DE MODA", "FORO / DEBATE ACADÉMICO", "SIMPOSIO"
    ]

    listas = obtenerListas()
    coordinadores = (listas["coordinadores"] if listas["coordinadores"] else [])
    clientes = (listas["clientes"] if listas["clientes"] else [])
    estado_evento = ["PENDIENTE", "EN PLANEACIÓN", "CONFIRMADO", "HECHO"]
    estado_pago = ["PENDIENTE", "ANTICIPADO", "PAGADO"]
    proovedores = listas["proovedores"] if listas["proovedores"] else ["Sin proovedores"]
    sedes = listas["sedes"] if listas["sedes"] else ["Sin sedes disponibles"]

    id_evento_var = tk.StringVar(value="")
    id_detalles_evento_var = tk.StringVar(value="")
    eventos_var = tk.StringVar(value=eventos[0])
    clientes_var = tk.StringVar(value=clientes[0])
    sedes_var = tk.StringVar(value=sedes[0])
    coordinadores_var = tk.StringVar(value=coordinadores[0])
    proovedores_var = tk.StringVar(value=proovedores[0])
    estado_evento_var = tk.StringVar(value=estado_evento[0])
    estado_pago_var = tk.StringVar(value=estado_pago[0])
    costo_servicio_var = tk.StringVar(value="")

        # --- Variables para los Filtros (Header) ---
    # Agregamos "TODOS" para que el filtro sea opcional
    f_coord_var = tk.StringVar(value="TODOS")
    f_clie_var = tk.StringVar(value="TODOS")
    f_est_e_var = tk.StringVar(value="TODOS")
    f_est_p_var = tk.StringVar(value="TODOS")

    # --- Encabezado y Filtros ---
    header = tk.Frame(container, bg=colors["primary"], pady=10)
    header.pack(fill="x")
    
    tk.Label(header, text="Gestión de Eventos", font=("Segoe UI", 16, "bold"), bg=colors["primary"], fg="white").pack(side="left", padx=20)
    
    # Contenedor de filtros
    filtro_div = tk.Frame(header, bg=colors["primary"])
    filtro_div.pack(side="right", padx=10)

    # Función interna para disparar el filtro
    def filtrar():
        # Llamada al controlador que definimos previamente
        data = filtrarEventosController(
            f_est_e_var.get(), 
            f_est_p_var.get(), 
            f_coord_var.get(), 
            f_clie_var.get()
        )

        # Limpiar y recargar Tabla de Eventos
        for i in tabla_eventos.get_children(): tabla_eventos.delete(i)
        for v in data["eventos"]:
            tabla_eventos.insert("", tk.END, values=v)

        # Limpiar y recargar Tabla de Detalles
        for i in tabla_detalles.get_children(): tabla_detalles.delete(i)
        for v in data["detalles"]:
            tabla_detalles.insert("", tk.END, values=v)

    # Menús desplegables de filtro en el Header
    tk.OptionMenu(filtro_div, f_coord_var, "TODOS", *coordinadores).pack(side="left", padx=2)
    tk.OptionMenu(filtro_div, f_clie_var, "TODOS", *clientes).pack(side="left", padx=2)
    tk.OptionMenu(filtro_div, f_est_e_var, "TODOS", *estado_evento).pack(side="left", padx=2)
    tk.OptionMenu(filtro_div, f_est_p_var, "TODOS", *estado_pago).pack(side="left", padx=2)
    
    tk.Button(filtro_div, text="Filtrar", command=filtrar, bg=colors["info"], fg="white", relief="flat", padx=15).pack(side="left", padx=5)
    
    tk.Button(header, text="← Volver", command=lambda: navegar("inicio"), bg="#5D6D7E", fg="white", relief="flat", padx=15).pack(side="right", padx=20)

    main_content = tk.Frame(container, bg=colors["bg"])
    main_content.pack(fill="both", expand=True, padx=20, pady=20)

    form_frame = tk.LabelFrame(main_content, text=" Datos y Detalles de Evento ", font=("Segoe UI", 10, "bold"), bg=colors["secondary"], fg="white", padx=15, pady=15)
    form_frame.pack(side="left", fill="y", padx=(0, 20))

    def crear_label(texto):
        tk.Label(form_frame, text=texto, bg=colors["secondary"], fg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 0))

    crear_label("Tipo de Evento:")
    evento_menu = ttk.Combobox(form_frame, textvariable=eventos_var, values=eventos, state="readonly")
    evento_menu.set(eventos[0])
    evento_menu.pack(fill="x", pady=5)

    crear_label("Fecha (AAAA-MM-DD):")
    input_fecha = tk.Entry(form_frame, font=("Segoe UI", 10))
    input_fecha.pack(fill="x", pady=5, ipady=3)

    crear_label("Estado del Evento:")
    estado_evento_menu = ttk.Combobox(form_frame, textvariable=estado_evento_var, values=estado_evento, state="readonly")
    estado_evento_menu.set(estado_evento[0])
    estado_evento_menu.pack(fill="x", pady=5)

    crear_label("Estado de Pago:")
    estado_pago_menu = ttk.Combobox(form_frame, textvariable=estado_pago_var, value=estado_pago, state="readonly")
    estado_pago_menu.set(estado_pago[0])
    estado_pago_menu.pack(fill="x", pady=5)

    crear_label("Presupuesto Estimado ($):")
    input_presupuesto = tk.Entry(form_frame, font=("Segoe UI", 10))
    input_presupuesto.pack(fill="x", pady=5, ipady=3)

    crear_label("Cliente:")
    clientes_menu = ttk.Combobox(form_frame, textvariable=clientes_var, value=clientes, state="readonly")
    clientes_menu.set(clientes[0])
    clientes_menu.pack(fill="x", pady=5)

    crear_label("Coordinadores:")
    coordinador_menu = ttk.Combobox(form_frame, textvariable=coordinadores_var, value=coordinadores, state="readonly")
    coordinador_menu.set(coordinadores[0])
    coordinador_menu.pack(fill="x", pady=5)

    crear_label("Sede Solicitada:")
    sede_menu = ttk.Combobox(form_frame, textvariable=sedes_var, value=sedes, state="readonly")
    sede_menu.set(sedes[0])
    sede_menu.pack(fill="x", pady=5)

    crear_label("---Detalles del Evento---")

    crear_label("Proveedores:")
    proovedor_menu = ttk.Combobox(form_frame, textvariable=proovedores_var, value=proovedores, state="readonly")
    proovedor_menu.set(proovedores[0])
    proovedor_menu.pack(fill="x", pady=5)

    def cargar_datos_tabla_eventos():
        for item in tabla_eventos.get_children(): 
            tabla_eventos.delete(item)
        eventos = listarEventosAdminController()
        if eventos:
            for v in eventos:
                tabla_eventos.insert("", tk.END, values=(v[0], v[1], v[2], v[3], v[4], f"{v[5]:,.2f}", v[6], v[7], v[8], f"{v[9]:,.2f}"))

    def cargar_datos_tabla_detalles():
        for i in tabla_detalles.get_children():
            tabla_detalles.delete(i)
        detalles = listarEventosDetallesAdminController()
        if detalles:
            for v in detalles:
                tabla_detalles.insert("", tk.END, values=(v[0], v[1], v[2], v[4], f"{v[5]:,.2f}"))

    
    def limpiar():
        id_evento_var.set("")
        eventos_var.set(eventos[0])
        input_fecha.delete(0, tk.END)
        estado_evento_var.set(estado_evento[0])
        input_presupuesto.delete(0, tk.END)
        clientes_var.set(clientes[0])
        coordinadores_var.set(coordinadores[0])
        sedes_var.set(sedes[0])
        id_detalles_evento_var.set("")
        estado_pago_var.set(estado_pago[0])
        proovedores_var.set(proovedores[0])
        costo_servicio_var.set("")
        btn_guardar.config(text="Registrar", bg=colors["accent"])

    def guardar():
        id_ev = id_evento_var.get()
        id_de = id_detalles_evento_var.get()
        exito, msg = guardarEventoAdminController(
            id_ev if id_ev else None, 
            eventos_var.get() if eventos_var.get() else None, 
            input_fecha.get() if input_fecha.get() else None, 
            estado_evento_var.get() if estado_evento_var.get() else None, 
            estado_pago_var.get() if estado_pago_var.get() else None,
            input_presupuesto.get() if input_presupuesto.get() else None, 
            clientes_var.get() if clientes_var.get() else None,
            coordinadores_var.get() if coordinadores_var.get() else None, 
            sedes_var.get() if sedes_var.get() else None,
            proovedores_var.get() if proovedores_var.get() else None,
            id_de if id_de else None
        )
        if exito:
            messagebox.showinfo("Éxito", "Operación exitosa")
            limpiar()
            cargar_datos_tabla_eventos()
            cargar_datos_tabla_detalles()
        else:
            messagebox.showerror("Error", msg)

    def guardarDetalles():
        id_ev = id_evento_var.get()
        exito, msg = guardarDetallesAdminController(
            id_ev if id_ev else None,
            proovedores_var.get() if proovedores_var.get() else None,
        )
        if exito:
            messagebox.showinfo("Éxito", "Operación exitosa")
            limpiar()
            cargar_datos_tabla_eventos()
            cargar_datos_tabla_detalles()
        else:
            messagebox.showerror("Error", msg)

    def borrar():
        if id_detalles_evento_var.get():
            if messagebox.askyesno("Confirmar", "¿Deseas cancelar este evento definitivamente?"):
                eliminarEventoDetallesController(id_detalles_evento_var.get())
                limpiar()
                cargar_datos_tabla_eventos()
                cargar_datos_tabla_detalles()
        elif id_evento_var.get():
            if messagebox.askyesno("Confirmar", "¿Deseas cancelar este evento definitivamente?"):
                eliminarEventoController(id_evento_var.get())
                limpiar()
                cargar_datos_tabla_eventos()
                cargar_datos_tabla_detalles()
        else:
            messagebox.showwarning("Atención", "Por favor, selecciona un evento de la tabla.")

    btn_guardar_d = tk.Button(form_frame, text="Añadir proveedor", bg=colors["accent"], 
                            fg="white", font=("Segoe UI", 8, "bold"), bd=0, pady=5, 
                            cursor="hand2", command=guardarDetalles)
    btn_guardar_d.pack(fill="x", pady=(10, 5))

    btn_guardar = tk.Button(form_frame, text="Registrar", bg=colors["accent"], 
                            fg="white", font=("Segoe UI", 10, "bold"), bd=0, pady=10, 
                            cursor="hand2", command=guardar)
    btn_guardar.pack(fill="x", pady=(20, 10))

    tk.Button(form_frame, text="Cancelar Evento Seleccionado", bg=colors["danger"], fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=10, command=borrar, cursor="hand2").pack(pady=10)
    
    tk.Button(form_frame, text="Limpiar Formulario", bg="#BDC3C7", bd=0, pady=5, command=limpiar, cursor="hand2").pack(fill="x")

    table_container = tk.Frame(main_content, bg="white")
    table_container.pack(side="right", fill="both", expand=True)

    columns_tabla_eventos = ("ID", "EVENTO", "FECHA", "ESTADO DEL EVENTO", "ESTADO DE PAGO", "PRESUPUESTO", "CLIENTE", "COORDINADOR", "SEDE", "COSTO DEL EVENTO")
    tabla_eventos = ttk.Treeview(table_container, columns=columns_tabla_eventos, show="headings")
    columns_tabla_detalles = ("ID", "CLIENTE", "EVENTO", "PROVEEDOR", "COSTO DEL SERVICIO DEL PROOVEDOR")
    tabla_detalles = ttk.Treeview(table_container, columns=columns_tabla_detalles, show="headings")
    
    for col in columns_tabla_eventos:
        tabla_eventos.heading(col, text=col)
        tabla_eventos.column(col, width=120, anchor="center")
    
    for col in columns_tabla_detalles:
        tabla_detalles.heading(col, text=col)
        tabla_detalles.column(col, width=120, anchor="center")

    tabla_eventos.pack(side="top", fill="both", expand=True, pady=(0, 20))
    tabla_detalles.pack(side="bottom", fill="both", expand=True)

    def al_seleccionar_eventos(e):
        item = tabla_eventos.selection()
        if item:
            val = tabla_eventos.item(item, "values")
            id_evento_var.set(val[0])
            eventos_var.set(val[1])
            input_fecha.delete(0, tk.END); input_fecha.insert(0, val[2])
            estado_evento_var.set(val[3])
            estado_pago_var.set(val[4])
            input_presupuesto.delete(0, tk.END); input_presupuesto.insert(0, val[5])
            clientes_var.set(val[6])
            coordinadores_var.set(val[7])
            sedes_var.set(val[8])
            btn_guardar.config(text="Actualizar", bg=colors["info"])

    def al_seleccionar_detalles(e):
        item = tabla_detalles.selection()
        if item:
            v = tabla_detalles.item(item, "values")
            id_detalles_evento_var.set(v[0])
            clientes_var.set(v[1])
            eventos_var.set(v[2])
            proovedores_var.set(v[4])
            costo_servicio_var.set(v[5])
            btn_guardar.config(text="Actualizar", bg=colors["info"])

    tabla_eventos.bind("<<TreeviewSelect>>", al_seleccionar_eventos)
    tabla_detalles.bind("<<TreeviewSelect>>", al_seleccionar_detalles)

    cargar_datos_tabla_eventos()
    cargar_datos_tabla_detalles()

def EventosViewCliente(container, navegar, usuario):
    # --- CONFIGURACIÓN DE COLORES Y ESTILOS ---
    COLORS = {
        "primary": "#34495E",    # Azul Grisáceo (Header)
        "secondary": "#2C3E50",  # Azul Oscuro (Formulario)
        "bg": "#f0f0f0",         # Gris Claro (Fondo)
        "accent": "#A9C462",     # Verde (Guardar)
        "danger": "#D96459",     # Rojo (Eliminar)
        "warning": "#E9B872",    # Amarillo/Naranja
        "info": "#709CA7"        # Azul Aqua (Actualizar/Volver)
    }
    
    container.configure(bg=COLORS["bg"])

    # --- DATOS PARA MENÚS DESPLEGABLES ---
    tipos_eventos = [
        "LANZAMIENTO DE PRODUCTO", "CONFERENCIA / SEMINARIO", "CONGRESO O CONVENCIÓN",
        "TEAM BUILDING / INTEGRACIÓN", "FIESTA DE FIN DE AÑO", "WORKSHOP / TALLER",
        "BODA (MATRIMONIO)", "FIESTA DE QUINCEAÑERA", "BABY SHOWER",
        "FIESTA DE GRADUACIÓN (PROM)", "ANIVERSARIO", "FIESTA DE CUMPLEAÑOS",
        "CONCIERTO / RECITAL", "EXPOSICIÓN DE ARTE", "FESTIVAL GASTRONÓMICO",
        "DESFILE DE MODA", "FORO / DEBATE ACADÉMICO", "SIMPOSIO"
    ]
    
    listas = obtenerListas()
    sedes = listas["sedes"] if listas["sedes"] else ["Sin sedes disponibles"]
    coords = listas["coordinadores"] if listas["coordinadores"] else ["Sin coordinadores"]

    # --- VARIABLES DE CONTROL ---
    id_seleccionado = tk.StringVar(value="")
    tipo_var = tk.StringVar(value=tipos_eventos[0])
    sede_var = tk.StringVar(value=sedes[0])
    coord_var = tk.StringVar(value=coords[0])

    # --- HEADER ---
    header = tk.Frame(container, bg=COLORS["primary"], pady=15)
    header.pack(fill="x")
    
    tk.Label(header, text="Mis Solicitudes de Eventos", font=("Segoe UI", 16, "bold"), bg=COLORS["primary"], fg="white").pack(side="left", padx=20)
    
    tk.Button(header, text="← Volver al Inicio", command=lambda: navegar("inicio"), bg=COLORS["info"], fg="white", bd=0, padx=15, cursor="hand2").pack(side="right", padx=20)

    # --- CONTENIDO PRINCIPAL ---
    main_content = tk.Frame(container, bg=COLORS["bg"])
    main_content.pack(fill="both", expand=True, padx=20, pady=20)

    # --- PANEL IZQUIERDO: FORMULARIO (Gris Oscuro) ---
    form_frame = tk.LabelFrame(main_content, text=" Nueva Solicitud / Edición ", font=("Segoe UI", 10, "bold"), bg=COLORS["secondary"], fg="white", padx=15, pady=15)
    form_frame.pack(side="left", fill="y", padx=(0, 20))

    def crear_label(texto):
        tk.Label(form_frame, text=texto, bg=COLORS["secondary"], fg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 0))

    crear_label("Tipo de Evento:")
    tk.OptionMenu(form_frame, tipo_var, *tipos_eventos).pack(fill="x", pady=5)

    crear_label("Fecha (AAAA-MM-DD):")
    ent_fecha = tk.Entry(form_frame, font=("Segoe UI", 10))
    ent_fecha.pack(fill="x", pady=5, ipady=3)

    crear_label("Presupuesto Estimado ($):")
    ent_presupuesto = tk.Entry(form_frame, font=("Segoe UI", 10))
    ent_presupuesto.pack(fill="x", pady=5, ipady=3)

    crear_label("Sede Solicitada:")
    tk.OptionMenu(form_frame, sede_var, *sedes).pack(fill="x", pady=5)

    # --- BOTONES DE ACCIÓN ---
    def cargar_datos_tabla():
        for item in tabla.get_children(): tabla.delete(item)
        eventos = listarEventosClienteController(usuario)
        if eventos:
            for ev in eventos:
                tabla.insert("", tk.END, values=(ev[0], ev[1], ev[2], ev[3], ev[4], ev[5]))

    def limpiar():
        id_seleccionado.set("")
        ent_fecha.delete(0, tk.END)
        ent_presupuesto.delete(0, tk.END)
        tipo_var.set(tipos_eventos[0])
        btn_guardar.config(text="Registrar Solicitud", bg=COLORS["accent"])

    def guardar():
        id_ev = id_seleccionado.get()
        exito, msg = guardarEventoClienteController(
            id_ev if id_ev else None, 
            tipo_var.get(), 
            ent_fecha.get(), 
            "PENDIENTE",
            "PENDIENTE", 
            ent_presupuesto.get(), 
            usuario,
            coord_var.get(), 
            sede_var.get()
        )
        if exito:
            messagebox.showinfo("Éxito", "Operación exitosa")
            limpiar()
            cargar_datos_tabla()
        else:
            messagebox.showerror("Error", msg)

    btn_guardar = tk.Button(form_frame, text="Registrar Solicitud", bg=COLORS["accent"], 
                            fg="white", font=("Segoe UI", 10, "bold"), bd=0, pady=10, 
                            cursor="hand2", command=guardar)
    btn_guardar.pack(fill="x", pady=(20, 10))
    
    tk.Button(form_frame, text="Limpiar Formulario", bg="#BDC3C7", bd=0, pady=5, command=limpiar, cursor="hand2").pack(fill="x")

    # --- PANEL DERECHO: TABLA ---
    table_container = tk.Frame(main_content, bg="white")
    table_container.pack(side="right", fill="both", expand=True)

    columns = ("ID", "EVENTO", "CLIENTE", "FECHA", "PRESUPUESTO", "SEDE")
    tabla = ttk.Treeview(table_container, columns=columns, show="headings")
    
    for col in columns:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")

    tabla.pack(fill="both", expand=True)

    def al_seleccionar(event):
        item = tabla.selection()
        if item:
            val = tabla.item(item, "values")
            id_seleccionado.set(val[0])
            tipo_var.set(val[1])
            ent_fecha.delete(0, tk.END); ent_fecha.insert(0, val[3])
            ent_presupuesto.delete(0, tk.END); ent_presupuesto.insert(0, val[4])
            sede_var.set(val[5])
            btn_guardar.config(text="Actualizar Solicitud", bg=COLORS["info"])

    tabla.bind("<<TreeviewSelect>>", al_seleccionar)

    # --- BOTÓN ELIMINAR ---
    def borrar():
        if id_seleccionado.get():
            if messagebox.askyesno("Confirmar", "¿Deseas cancelar este evento definitivamente?"):
                eliminarEventoController(id_seleccionado.get())
                limpiar()
                cargar_datos_tabla()
        else:
            messagebox.showwarning("Atención", "Por favor, selecciona un evento de la tabla.")

    tk.Button(container, text="🗑 Cancelar Evento Seleccionado", bg=COLORS["danger"], fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=10, command=borrar, cursor="hand2").pack(pady=10)

    # --- CARGA INICIAL ---
    cargar_datos_tabla()