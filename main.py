import tkinter as tk
from app.views.layouts.navbar import NavbarLayout
from app.views import *

current_user = {
    "state": False,
    "role": "CUST"
}

ventana = tk.Tk()
ventana.title("EventosPro App")
ventana.state("zoomed")
ventana.config(bg="#F8F9F1")

vistas = {
    "inicio": HomeView,
    "signup": SignUpView,
    "login": LogInView,
    "clientes": ClientesView,
    "perfil": PerfilView,
    "coordinadores": CoordinadoresView,
    "sedes" : SedesView,
    "proveedores" : ProveedoresView,
    "eventos" : EventosView,
    "dashboard" : DashBoard
}

def navegar(nombre):
    for widget in cuerpo.winfo_children():
        widget.destroy()
    
    vista = vistas.get(nombre)
    
    if vista:

        estado_actual = current_user["state"]
        rol_actual = current_user["role"]

        if nombre in ["login", "signup"]:
            vista(cuerpo, navegar, login_exitoso) 
        elif nombre == "inicio":
            vista(cuerpo, rol_actual, estado_actual, navegar)
        elif nombre == "perfil":
            nom_user = current_user.get("username")
            vista(cuerpo, navegar, nom_user)
        elif nombre == "eventos":
            user = current_user.get("username")
            vista(cuerpo, rol_actual, navegar, user)
        else:
            vista(cuerpo, navegar)
        
        cuerpo.update_idletasks()
        actualizar_scroll_dinamico()
        canvas.yview_moveto(0)
    else:
        print(f"Error: La vista '{nombre}' no existe.")

def login_exitoso(nuevo_rol, nombre_usuario, id_usuario):
    current_user["id"] = id_usuario
    current_user["state"] = True
    current_user["role"] = nuevo_rol
    current_user["username"] = nombre_usuario
    for widget in ventana.winfo_children():
        if isinstance(widget, tk.Frame) and widget != main_container:
            widget.destroy()
    
    navbar = NavbarLayout(ventana, navegar, current_user["role"], current_user["state"], cerrar_sesion)
    navbar.pack_forget()
    navbar.pack(side="top", fill="x", before=main_container)

    navegar("inicio")

def cerrar_sesion():
    current_user["state"] = False
    current_user["role"] = "CUST"
    
    for widget in ventana.winfo_children():
        if isinstance(widget, tk.Frame) and widget != main_container:
            widget.destroy()
    
    navbar = NavbarLayout(ventana, navegar, current_user["role"], current_user["state"], cerrar_sesion)
    navbar.pack(side="top", fill="x", before=main_container)
    
    navegar("inicio")

def actualizar_scroll_dinamico(event=None):
    ancho_visible = canvas.winfo_width()
    alto_visible = canvas.winfo_height()
    alto_necesario = cuerpo.winfo_reqheight()
    altura_final = max(alto_necesario, alto_visible)
    canvas.itemconfig(cuerpo_id, width=ancho_visible, height=altura_final)
    canvas.config(scrollregion=(0, 0, ancho_visible, altura_final))

NavbarLayout(ventana, navegar, current_user["role"], current_user["state"], cerrar_sesion)

main_container = tk.Frame(ventana, bg="#F8F9F1")
main_container.pack(fill="both", expand=True)

canvas = tk.Canvas(main_container, bg="#F8F9F1", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

cuerpo = tk.Frame(canvas, bg="#F8F9F1")
cuerpo_id = canvas.create_window((0, 0), window=cuerpo, anchor="nw")

canvas.bind("<Configure>", actualizar_scroll_dinamico)
ventana.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

def setup():
    ventana.update_idletasks()
    navegar("inicio")

ventana.after(100, setup)
ventana.mainloop()