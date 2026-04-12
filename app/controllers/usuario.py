from tkinter import messagebox
from app.models.usuario import crearUsuarioModel, leerUsuarioModel

def crearUsuarioController(entry_nom, entry_pass, entry_rol, al_exito):
    nombre = entry_nom.get()
    password = entry_pass.get()
    role = entry_rol.get()

    if not nombre or not password or not role:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return

    if role == "Administrador":
        rol = "ADMIN"
    elif role == "Cliente":
        rol = "CUST"

    exito, mensaje = crearUsuarioModel(nombre, password, rol)

    if exito:
        messagebox.showinfo("Éxito", mensaje)
        entry_nom.delete(0, 'end')
        entry_pass.delete(0, 'end')
        entry_rol.set("Cliente")
        id = leerUsuarioModel(nombre, password)[1]["id"] if leerUsuarioModel(nombre, password)[0] else None
        al_exito(rol, nombre, id)
    else:
        messagebox.showerror("Error", mensaje)

def leerUsuarioController(entry_user, entry_pass, al_exito):
    user_name = entry_user.get()
    password = entry_pass.get()

    if not user_name or not password:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return

    exito, resultado = leerUsuarioModel(user_name, password)

    if exito:
        messagebox.showinfo("Bienvenido", f"¡Hola {resultado['nombre']}! Has iniciado sesión correctamente.")
        al_exito(resultado["rol"], resultado["nombre"], resultado["id"])
        return resultado
    else:
        messagebox.showerror("Error", resultado)
        return None