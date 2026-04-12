import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

bg_color = "#FFFFFF"
accent_color = "#2C3E50" 
detail_color = "#3498DB"
text_muted = "#7F8C8D"

def HomeViewCustomer(container, state, navegar):
    container.configure(bg=bg_color)

    hero_frame = tk.Frame(container, bg="#222222", pady=250)
    hero_frame.pack(fill="both", expand=True)

    tk.Label(hero_frame, text="EventosPro Organizadores", font=("Segoe UI", 36, "bold"), bg="#222222", fg=detail_color).pack()
    tk.Label(hero_frame, text="Elevando la excelencia en eventos corporativos y sociales.", font=("Segoe UI", 14), bg="#222222", fg=text_muted).pack(pady=(10, 20))

    def bienvenida():
        if not state:
            navegar("signup")
        else:
            messagebox.showinfo("¡Bienvenido de nuevo!", "¡Gracias por volver a EventosPro! Explora nuestras opciones para descubrir cómo podemos ayudarte a organizar el evento perfecto.")

    btn_comenzar = tk.Button(hero_frame, text="EMPEZAR", font=("Segoe UI", 11, "bold"), bg=detail_color, fg="white", padx=30, pady=12, bd=0, cursor="hand2", command=lambda: bienvenida())
    btn_comenzar.pack()
    btn_comenzar.bind("<Enter>", lambda e: btn_comenzar.config(bg="#2980B9"))
    btn_comenzar.bind("<Leave>", lambda e: btn_comenzar.config(bg=detail_color))

    servicios_frame = tk.Frame(container, bg=bg_color, pady=250)
    servicios_frame.pack(fill="both", expand=True)

    tk.Label(servicios_frame, text="Especialistas en Experiencias", font=("Segoe UI", 18, "bold"), bg=bg_color, fg=accent_color).pack(pady=(50, 30))

    cards_container = tk.Frame(servicios_frame, bg=bg_color)
    cards_container.pack(fill="both", expand=True, padx=50)

    servicios = [
        ("🏢 Corporativos", "Congresos y lanzamientos\nde productos de alto nivel."),
        ("💍 Sociales", "Bodas y fiestas de grado\ncon atención al detalle."),
        ("🤝 Proveedores", "Coordinación integral de\ncatering, sonido y logística.")
    ]

    for i, (titulo, desc) in enumerate(servicios):
        card = tk.Frame(cards_container, bg="white", highlightbackground="#F0F0F0", highlightthickness=2, padx=20, pady=20)
        card.grid(row=0, column=i, padx=15, sticky="nsew")
        cards_container.columnconfigure(i, weight=1)
        tk.Label(card, text=titulo, font=("Segoe UI", 13, "bold"), bg="white", fg=detail_color).pack(pady=(0, 10))
        tk.Label(card, text=desc, font=("Segoe UI", 10), bg="white", fg=text_muted, justify="center").pack()

    beneficios_frame = tk.Frame(container, bg=bg_color, pady=250)
    beneficios_frame.pack(fill="both", expand=True)

    tk.Label(beneficios_frame, text="Nuestro Valor Agregado", font=("Segoe UI", 18, "bold"), bg=bg_color, fg=accent_color).pack(pady=(50, 10))
    tk.Label(beneficios_frame, text="Tecnología y experiencia al servicio de tu próximo gran momento.", font=("Segoe UI", 11), bg=bg_color, fg=text_muted).pack(pady=(0, 30))

    beneficios_pro = [
        ("📊", "Control Total", "Presupuestos claros y sin sorpresas de última hora."),
        ("🤝", "Alianzas Estratégicas", "Proveedores verificados y coordinados con precisión."),
        ("🚀", "Eficiencia Real", "Procesos optimizados para una organización rápida y sin errores."),
        ("📍", "Sedes Exclusivas", "Gestión directa de los mejores espacios de la ciudad.")
    ]

    beneficios_container = tk.Frame(beneficios_frame, bg=bg_color)
    beneficios_container.pack(fill="x", padx=50)

    for i, (icono, titulo, desc) in enumerate(beneficios_pro):
        b_card = tk.Frame(beneficios_container, bg="#FDFDFD", padx=15, pady=15, highlightbackground="#EEEEEE", highlightthickness=1)
        b_card.grid(row=0, column=i, padx=10, sticky="nsew")
        beneficios_container.columnconfigure(i, weight=1)

        tk.Label(b_card, text=icono, font=("Segoe UI", 20), bg="#FDFDFD").pack()
        tk.Label(b_card, text=titulo, font=("Segoe UI", 11, "bold"), bg="#FDFDFD", fg=detail_color).pack(pady=5)
        tk.Label(b_card, text=desc, font=("Segoe UI", 9), bg="#FDFDFD", fg=text_muted, wraplength=150, justify="center").pack()

    footer = tk.Label(container, text="© 2026 EventosPro Organizadores S.A.S - Barranquilla, Colombia", font=("Segoe UI", 9), bg=accent_color, fg="#BDC3C7", pady=60)
    footer.pack(pady=(40, 0), expand=True, fill="both")

import tkinter as tk
from tkinter import messagebox

def HomeViewAdmin(container, navegar):
    # --- Configuración Base ---
    for widget in container.winfo_children():
        widget.destroy()
    
    container.configure(bg="#F8FAFC") # Gris azulado muy claro (estilo SaaS)
    
    # Paleta de colores
    primary = "#4F46E5"     # Índigo moderno
    secondary = "#10B981"   # Esmeralda
    text_main = "#1E293B"   # Slate oscuro
    text_muted = "#64748B"  # Slate gris
    bg_white = "#FFFFFF"

    # --- 1. HERO SECTION (Encabezado tipo Banner) ---
    hero_frame = tk.Frame(container, bg=primary, pady=40)
    hero_frame.pack(fill="x")
    
    hero_content = tk.Frame(hero_frame, bg=primary)
    hero_content.pack(padx=60, fill="x")
    
    tk.Label(
        hero_content, 
        text="Panel Administrativo", 
        font=("Segoe UI", 28, "bold"), 
        fg="white", bg=primary
    ).pack(anchor="w")
    
    tk.Label(
        hero_content, 
        text="Bienvenido de nuevo. Aquí tienes el resumen de tu operación hoy.", 
        font=("Segoe UI", 12), 
        fg="#E0E7FF", bg=primary
    ).pack(anchor="w", pady=(5, 0))

    # --- 2. KPI CARDS (Métricas Rápidas) ---
    # Contenedor para que las tarjetas floten sobre el hero ligeramente
    stats_container = tk.Frame(container, bg="#F8FAFC")
    stats_container.pack(fill="x", padx=50, pady=( 50, 20)) # Margen negativo para solapar

    kpis = [
        ("Eventos", "12", "#4F46E5"),
        ("Clientes", "45", "#0EA5E9"),
        ("Ingresos", "$12.5M", "#10B981"),
        ("Alertas", "3", "#F59E0B")
    ]

    for i, (title, val, color) in enumerate(kpis):
        card = tk.Frame(stats_container, bg=bg_white, padx=20, pady=20, 
                        highlightthickness=1, highlightbackground="#E2E8F0")
        card.grid(row=0, column=i, padx=10, sticky="nsew")
        stats_container.columnconfigure(i, weight=1)

        tk.Label(card, text=title, font=("Segoe UI", 10, "bold"), bg=bg_white, fg=text_muted).pack(anchor="w")
        tk.Label(card, text=val, font=("Segoe UI", 20, "bold"), bg=bg_white, fg=color).pack(anchor="w", pady=(5,0))

    # --- 3. SECCIÓN DE ACCIONES (Grilla de Navegación) ---
    tk.Label(
        container, text="Accesos Directos de Gestión", 
        font=("Segoe UI", 14, "bold"), bg="#F8FAFC", fg=text_main
    ).pack(padx=60, anchor="w", pady=(30, 10))

    actions_frame = tk.Frame(container, bg="#F8FAFC")
    actions_frame.pack(fill="x", padx=50)

    # Definición de botones (Icono, Texto, Ruta, Color)
    botones = [
        ("📊", "Reportes Detallados", "dashboard", "#6366F1"),
        ("📅", "Gestionar Eventos", "eventos", "#8B5CF6"),
        ("🚚", "Proveedores", "proveedores", "#F43F5E"),
    ]

    for i, (icon, text, route, color) in enumerate(botones):
        # Frame del botón para efecto de tarjeta
        btn_card = tk.Frame(actions_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E2E8F0")
        btn_card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
        actions_frame.columnconfigure(i%3, weight=1)

        # Contenido del "Botón"
        l_icon = tk.Label(btn_card, text=icon, font=("Segoe UI", 24), bg=bg_white)
        l_icon.pack(pady=(20, 5))
        
        btn = tk.Button(
            btn_card, text=text, font=("Segoe UI", 11, "bold"),
            bg=bg_white, fg=color, bd=0, cursor="hand2",
            activebackground=bg_white, activeforeground=color,
            command=lambda r=route: navegar(r)
        )
        btn.pack(pady=(0, 20), fill="x", padx=10)

        # Efectos Hover (Cambia el fondo de la tarjeta)
        def on_enter(e, c=btn_card): c.config(highlightbackground=primary, highlightthickness=2)
        def on_leave(e, c=btn_card): c.config(highlightbackground="#E2E8F0", highlightthickness=1)
        
        btn_card.bind("<Enter>", on_enter)
        btn_card.bind("<Leave>", on_leave)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # --- 4. FOOTER / STATUS BAR ---
    footer = tk.Frame(container, bg=bg_white, height=40, bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
    footer.pack(fill="x", side="bottom")
    
    tk.Label(
        footer, text="● Sistema Operativo - v2.1.0", 
        font=("Segoe UI", 9), bg=bg_white, fg="#10B981", padx=20
    ).pack(side="left", pady=10)
    
    tk.Label(
        footer, text="2026 Eventos Pro S.A.", 
        font=("Segoe UI", 9), bg=bg_white, fg=text_muted, padx=20
    ).pack(side="right", pady=10)

def HomeView(container, role, state, navegar):
    for widget in container.winfo_children():
        widget.destroy()

    if role == "ADMIN":
        HomeViewAdmin(container, navegar)
    else:
        HomeViewCustomer(container, state, navegar)