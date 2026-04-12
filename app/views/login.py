from app.controllers.usuario import crearUsuarioController
import tkinter as tk

def LogInView(container, navegar, exito):
    frame = tk.Frame(container, bg="#F8F9F1")
    frame.pack(fill="both", expand=True)

    form = tk.Frame(frame, bg="#2C3E50", padx=70, pady=50)
    form.pack(pady=50, fill="y", expand=True)

    label = tk.Label(form, text="Registro de usuario", font=("Arial", 30), bg="#2C3E50", fg="#f0f0f0")
    label.pack(pady=20)

    label_input_user = tk.Label(form, text="Nombre de usuario", font=("Arial", 10), bg="#2C3E50", fg="#f0f0f0")
    label_input_user.pack(pady=5, anchor="w")
    input_user = tk.Entry(form, bg="#FFFFFF", relief="flat")
    input_user.pack(pady=10, ipady=10, fill="x", expand=True)

    label_input_pass = tk.Label(form, text="Contraseña", font=("Arial", 10), bg="#2C3E50", fg="#f0f0f0")
    label_input_pass.pack(pady=5, anchor="w")
    input_pass = tk.Entry(form, show="*", bg="#FFFFFF", relief="flat")
    input_pass.pack(pady=10, ipady=10, fill="x", expand=True)

    label_rol = tk.Label(form, text="Selecciona tu Rol:", bg="#2c3e50", fg="#f0f0f0")
    label_rol.pack(pady=(10, 0), anchor="w")
    rol_seleccionado = tk.StringVar(form)
    rol_seleccionado.set("Cliente")

    opciones_roles = ["Administrador", "Cliente"]

    menu_roles = tk.OptionMenu(form, rol_seleccionado, *opciones_roles)
    
    menu_roles.config(
        bg="#FFFFFF", 
        relief="flat", 
        highlightthickness=1, 
        highlightbackground="#e2edbb",
        activebackground="#E2EDBB"
    )
    
    menu_roles["menu"].config(bg="#FFFFFF", relief="flat")

    menu_roles.pack(pady=10, ipady=5, fill="x", expand=True)

    btn_registrar = tk.Button(form, text="Registrar", font=("Arial", 15, "bold"), padx=10, pady=10, relief="flat", bd=0,command=lambda: crearUsuarioController(input_user, input_pass, rol_seleccionado, exito))
    btn_registrar.pack(pady=20, fill="x", expand=True)

    label_iniciar_sesion = tk.Label(form, text="¿Ya tienes una cuenta?", font=("Arial", 10), bg="#2C3E50", fg="#f0f0f0")
    label_iniciar_sesion.pack(pady=10)

    btn_iniciar_sesion = tk.Button(form, text="Iniciar sesion", font=("Arial", 10, "bold"), padx=10, pady=10, relief="flat", bd=0, command=lambda: navegar("signup"))
    btn_iniciar_sesion.pack(pady=5, fill="x", expand=True)

    def hover(boton, color_hover, color_original, fg_color, fg_color_original):
        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover, fg=fg_color))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_original, fg=fg_color_original))

    hover(btn_registrar, "#093766", "#f0f0f0", "#f0f0f0", "#2C3E50")
    hover(btn_iniciar_sesion, "#093766", "#f0f0f0", "#f0f0f0", "#2C3E50")