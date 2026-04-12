from tkinter import messagebox
from app.models.cliente import crearClienteModel, listarClientesModel, actualizarClienteModel, eliminarClienteModel

def crearClienteController(nombre, email, telefono, nuip, nombreUsuario):
    if not all([nombre, email, telefono, nuip, nombreUsuario]):
        return False, messagebox.showerror("Error", "Todos los campos son obligatorios.")
    
    n = nombre.upper()
    
    resultado, mensaje = crearClienteModel(n, email, telefono, nuip, nombreUsuario)
    return resultado, messagebox.showinfo("Resultado", mensaje) if resultado else messagebox.showerror("Error", mensaje)

def listarClientesController():
    clientes, mensaje = listarClientesModel()
    
    if clientes is None:
        messagebox.showerror("Error", mensaje)
        return []
    
    return clientes

def actualizarClienteController(idCliente, nombre, email, telefono, nuip):
    if not idCliente or not all([nombre, email, telefono, nuip]):
        return False, messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
    
    n = nombre.upper()
    
    resultado, mensaje = actualizarClienteModel(idCliente, n, email, telefono, nuip)
    if resultado:
        messagebox.showinfo("Éxito", mensaje)
        return True
    else:
        messagebox.showerror("Error", mensaje)
        return False

def eliminarClienteController(idCliente):
    if not idCliente:
        return False, messagebox.showerror("Error", "El ID del cliente es obligatorio.")
    resultado, mensaje = eliminarClienteModel(idCliente)
    return resultado, messagebox.showinfo("Resultado", mensaje) if resultado else messagebox.showerror("Error", mensaje)