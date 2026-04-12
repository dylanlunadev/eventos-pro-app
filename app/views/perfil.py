import tkinter as tk
from tkinter import messagebox
from app.controllers.cliente import (
    crearClienteController, 
    actualizarClienteController, 
    eliminarClienteController,
    listarClientesController
)

def PerfilView(container, navegar, nombre_usuario_logueado):
    container.configure(bg="#F4F7F6")

    # --- CARD PRINCIPAL ---
    card = tk.Frame(container, bg="white", padx=40, pady=30, highlightthickness=1, highlightbackground="#E0E0E0")
    card.pack(fill="both", expand=True, padx=50, pady=50)

    tk.Label(card, text="👤 Mi Perfil", font=("Segoe UI", 22, "bold"), bg="white", fg="#2C3E50").pack(pady=(0, 5))
    
    id_cliente_db = tk.StringVar(value="")

    # --- CAMPOS ---
    fields = [
        ("nombre", "Nombre Completo:"),
        ("email", "Correo Electrónico:"),
        ("telefono", "Teléfono:"),
        ("nuip", "Identificación (NUIP):")
    ]
    entries = {}

    for key, label_text in fields:
        tk.Label(card, text=label_text, bg="white", fg="#34495E", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 0))
        entry = tk.Entry(card, font=("Segoe UI", 11), bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#DCDCDC", width=45)
        entry.pack(fill="x", ipady=8, pady=5)
        entries[key] = entry

    # --- LÓGICA DE CARGA ---
    def buscar_datos_perfil():
        todos = listarClientesController()
        perfil_encontrado = next((c for c in todos if c[6] == nombre_usuario_logueado), None)

        if perfil_encontrado:
            id_cliente_db.set(perfil_encontrado[0])
            entries["nombre"].insert(0, perfil_encontrado[1])
            entries["email"].insert(0, perfil_encontrado[2])
            entries["telefono"].insert(0, perfil_encontrado[3])
            entries["nuip"].insert(0, perfil_encontrado[4])
            
            btn_principal.config(text="Actualizar mi Información", bg="#3498DB")
            btn_eliminar.pack(fill="x", pady=5)

    # --- ACCIONES ---
    def manejar_guardado():
        nombre = entries["nombre"].get()
        email = entries["email"].get()
        tel = entries["telefono"].get()
        nuip = entries["nuip"].get()

        if id_cliente_db.get() == "":
            crearClienteController(nombre, email, tel, nuip, nombre_usuario_logueado)
        else:
            actualizarClienteController(id_cliente_db.get(), nombre, email, tel, nuip, None)
        
        navegar("inicio")

    def manejar_eliminacion():
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar tu perfil de cliente? \n(Tu cuenta de usuario seguirá activa)"):
            eliminarClienteController(id_cliente_db.get())
            navegar("inicio")

    # --- BOTONES ---
    btn_principal = tk.Button(card, text="Vincular Perfil", bg="#27AE60", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=12, cursor="hand2", command=manejar_guardado)
    btn_principal.pack(fill="x", pady=(20, 10))

    btn_eliminar = tk.Button(card, text="🗑 Eliminar Perfil de Cliente", bg="#E74C3C", fg="white", font=("Segoe UI", 10), bd=0, pady=8, cursor="hand2", command=manejar_eliminacion)

    tk.Button(card, text="Cancelar", bg="white", fg="#7F8C8D", bd=0, command=lambda: navegar("inicio")).pack()

    buscar_datos_perfil()