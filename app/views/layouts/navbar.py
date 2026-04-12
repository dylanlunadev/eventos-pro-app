import tkinter as tk

def NavbarLayout(parent, navegar, role, state, salir):
    navbar = tk.Frame(parent, height=60, bg="#2C3E50", padx=20)
    navbar.pack(side="top", fill="x")
    navbar.pack_propagate(False)

    logo = tk.Label(
        navbar, 
        text="EventosPro App", 
        font=("Segoe UI", 16, "bold"), 
        bg="#2C3E50", 
        fg="#ffffff",
        cursor="hand2"
    )
    logo.pack(side="left", fill="y")
    logo.bind("<Button-1>", lambda e: navegar("inicio"))

    btns_frame = tk.Frame(navbar, bg="#2C3E50")
    btns_frame.pack(side="right", fill="y")

    btn_params = {
        "bd": 0,
        "bg": "#2C3E50",
        "fg": "#ffffff",
        "padx": 15,
        "font": ("Segoe UI", 10, "bold"),
        "activebackground": "#34495E",
        "activeforeground": "#ffffff",
        "highlightthickness": 0,
        "cursor": "hand2"
    }

    def hover(boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="#34495E"))
        boton.bind("<Leave>", lambda e: boton.config(bg="#2C3E50"))

    if not state:
        btn_login = tk.Button(btns_frame, text="Iniciar Sesión", **btn_params, command=lambda: navegar("signup"))
        btn_login.pack(side="left", fill="y")
        hover(btn_login)

        btn_registro = tk.Button(btns_frame, text="Registrarse", **btn_params, command=lambda: navegar("login"))
        btn_registro.pack(side="left", fill="y")
        hover(btn_registro)

    else:
        btn_inicio = tk.Button(btns_frame, text="Inicio", **btn_params, command=lambda: navegar("inicio"))
        btn_inicio.pack(side="left", fill="y")
        hover(btn_inicio)

        if role == "ADMIN":
            btn_gestionar = tk.Menubutton(btns_frame, text="Gestionar", **btn_params)
            
            menu_desplegable = tk.Menu(btn_gestionar, tearoff=0, bg="#ffffff", fg="#2C3E50", activebackground="#3498DB", activeforeground="white", font=("Segoe UI", 10))
            menu_desplegable.add_command(label="👥 Clientes", command=lambda: navegar("clientes"))
            menu_desplegable.add_command(label="📅 Eventos", command=lambda: navegar("eventos"))
            menu_desplegable.add_command(label="👔 Coordinadores", command=lambda: navegar("coordinadores"))
            menu_desplegable.add_command(label="🚚 Proveedores", command=lambda: navegar("proveedores"))
            menu_desplegable.add_command(label="🏨 Sedes", command=lambda: navegar("sedes"))
            
            btn_gestionar.config(menu=menu_desplegable)
            btn_gestionar.pack(side="left", fill="y")
            hover(btn_gestionar)

        else:
            btn_gest_eventos = tk.Button(btns_frame, text="Gestionar Eventos", **btn_params, command=lambda: navegar("eventos"))
            btn_gest_eventos.pack(side="left", fill="y")

            btn_perfil = tk.Button(btns_frame, text="Perfil", **btn_params, command=lambda: navegar("perfil"))
            btn_perfil.pack(side="left", fill="y")
            
            hover(btn_gest_eventos)
            hover(btn_perfil)

        btn_salir = tk.Button(btns_frame, text="Salir", **btn_params, command=salir)
        btn_salir.config(fg="#E74C3C")
        btn_salir.pack(side="left", fill="y")
        hover(btn_salir)

    return navbar