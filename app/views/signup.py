import tkinter as tk
from app.controllers.usuario import leerUsuarioController

def SignUpView(container, navegar, exito):
    frame = tk.Frame(container, bg="#F8F9F1")
    frame.pack(fill="both", expand=True)

    form = tk.Frame(frame, bg="#2C3E50", padx=70, pady=50)
    form.pack(pady=50, fill="y", expand=True)

    label = tk.Label(form, text="Iniciar Sesión", font=("Arial", 30), bg="#2C3E50", fg="#f0f0f0")
    label.pack(pady=20)

    label_input_usuario = tk.Label(form, text="Nombre de usuario (@)", font=("Arial", 10), bg="#2C3E50", fg="#f0f0f0")
    label_input_usuario.pack(pady=5, anchor="w")
    input_usuario = tk.Entry(form, bg="#FFFFFF", relief="flat")
    input_usuario.pack(pady=10, ipady=10, fill="x", expand=True)

    label_input_pass = tk.Label(form, text="Contraseña", font=("Arial", 10), bg="#2C3E50", fg="#f0f0f0")
    label_input_pass.pack(pady=5, anchor="w")
    input_pass = tk.Entry(form, show="*", bg="#FFFFFF", relief="flat")
    input_pass.pack(pady=10, ipady=10, fill="x", expand=True)

    btn_iniciar_sesion = tk.Button(form, text="Iniciar sesión", font=("Arial", 15, "bold"), padx=10, pady=10, relief="flat", bd=0, command=lambda: leerUsuarioController(input_usuario, input_pass, exito))
    btn_iniciar_sesion.pack(pady=20, fill="x", expand=True)

    label_registrar = tk.Label(form, text="¿No has creado una cuenta?", font=("Arial", 10), bg="#2C3E50", fg="#f0f0f0")
    label_registrar.pack(pady=10)

    btn_registrar = tk.Button(form, text="Registrate", font=("Arial", 10, "bold"), padx=10, pady=10, relief="flat", bd=0, command=lambda: navegar("login"))
    btn_registrar.pack(pady=5, fill="x", expand=True)

    def hover(boton, bg_color_hover, bg_color_original, fg_color_hover, fg_color_original):
        boton.bind("<Enter>", lambda e: boton.config(bg=bg_color_hover, fg=fg_color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=bg_color_original, fg=fg_color_original))

    hover(btn_iniciar_sesion, "#093766", "#f0f0f0", "#f0f0f0", "#2C3E50")
    hover(btn_registrar, "#093766", "#f0f0f0", "#f0f0f0", "#2C3E50")