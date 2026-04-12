import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.controllers.dashboard import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def DashBoard(container, navegar):
    for widget in container.winfo_children():
        widget.destroy()
    container.configure(bg="#F4F7F6")

    # Obtener datos procesados
    data = logica_obtener_datos_dashboard()

    # --- HEADER ---
    header = tk.Frame(container, bg="#F4F7F6", pady=20)
    header.pack(fill="x", padx=50)
    
    tk.Label(header, text="Análisis de Gestión Administrativa", 
             font=("Segoe UI", 22, "bold"), bg="#F4F7F6", fg="#2C3E50").pack(side="left")
    
    tk.Button(header, text="⬅ Volver al Inicio", font=("Segoe UI", 10, "bold"),
              bg="#95A5A6", fg="white", bd=0, padx=20, pady=8, cursor="hand2",
              command=lambda: navegar("home")).pack(side="right")

    # --- CUERPO PRINCIPAL (DOS COLUMNAS) ---
    body = tk.Frame(container, bg="#F4F7F6")
    body.pack(fill="both", expand=True, padx=40)
    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=1)

    # --- COLUMNA IZQUIERDA: ESTADOS ---
    col_izq = tk.Frame(body, bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#E0E0E0")
    col_izq.grid(row=0, column=0, padx=10, sticky="nsew")

    # Gráfico de Pastel
    fig_pie = Figure(figsize=(4, 3), dpi=90)
    ax_pie = fig_pie.add_subplot(111)
    labels, values = data["graficos"]["pie"]
    if values:
        ax_pie.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, 
                   colors=["#3498DB", "#2ECC71", "#E74C3C", "#F1C40F"])
    ax_pie.set_title("Eventos por Estado")
    
    canvas_pie = FigureCanvasTkAgg(fig_pie, master=col_izq)
    canvas_pie.get_tk_widget().pack(fill="x")
    canvas_pie.draw()

    # Tabla de Estados
    tk.Label(col_izq, text="Detalle Numérico", font=("Segoe UI", 11, "bold"), bg="white", fg="#7F8C8D").pack(pady=(15,5))
    tabla_est = ttk.Treeview(col_izq, columns=("Estado", "Cant"), show="headings", height=5)
    tabla_est.heading("Estado", text="Estado")
    tabla_est.heading("Cant", text="Cantidad")
    tabla_est.column("Estado", width=150)
    tabla_est.column("Cant", width=70, anchor="center")
    
    for item in data["tablas"]["estados"]:
        tabla_est.insert("", "end", values=(item['estadoEvento'], item['total']))
    tabla_est.pack(fill="x")


    # --- COLUMNA DERECHA: INGRESOS ---
    col_der = tk.Frame(body, bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#E0E0E0")
    col_der.grid(row=0, column=1, padx=10, sticky="nsew")

    # Gráfico de Barras
    fig_bar = Figure(figsize=(4, 3), dpi=90)
    ax_bar = fig_bar.add_subplot(111)
    periodos, montos = data["graficos"]["bar"]
    if montos:
        ax_bar.bar(periodos, montos, color="#8E44AD")
    ax_bar.set_title("Ingresos Mensuales ($)")
    ax_bar.tick_params(axis='x', rotation=30, labelsize=8)
    
    canvas_bar = FigureCanvasTkAgg(fig_bar, master=col_der)
    canvas_bar.get_tk_widget().pack(fill="x")
    canvas_bar.draw()

    # Tabla de Ingresos
    tk.Label(col_der, text="Historial de Ingresos", font=("Segoe UI", 11, "bold"), bg="white", fg="#7F8C8D").pack(pady=(15,5))
    tabla_ing = ttk.Treeview(col_der, columns=("Mes", "Monto"), show="headings", height=5)
    tabla_ing.heading("Mes", text="Mes")
    tabla_ing.heading("Monto", text="Presupuesto")
    tabla_ing.column("Mes", width=120)
    tabla_ing.column("Monto", width=120, anchor="e")
    
    for ing in data["tablas"]["ingresos"]:
        tabla_ing.insert("", "end", values=(ing['periodo'], f"$ {ing['total']:,.2f}"))
    tabla_ing.pack(fill="x")