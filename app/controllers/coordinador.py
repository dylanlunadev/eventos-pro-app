from tkinter import messagebox
from app.models.coordinador import (
    crearCoordinadorModel, listarCoordinadoresModel, 
    actualizarCoordinadorModel, eliminarCoordinadorModel
)

def crearCoordinadorController(nombre, nuip, estado, salario):
    if not all([nombre, nuip, estado, salario]):
        return False, messagebox.showwarning("Atención", "Todos los campos son obligatorios")

    n = nombre.upper()
    
    exito, msj = crearCoordinadorModel(n, nuip, estado, salario)
    if exito: messagebox.showinfo("Éxito", msj)
    else: messagebox.showerror("Error", msj)
    return exito

def listarCoordinadoresController():
    datos, msj = listarCoordinadoresModel()
    if datos is None:
        messagebox.showerror("Error", msj)
        return []
    return datos

def actualizarCoordinadorController(idC, nombre, nuip, estado, salario):
    if not all([idC, nombre, nuip, estado, salario]):
        return False, messagebox.showwarning("Atención", "Todos los campos son obligatorios")

    n = nombre.upper()

    exito, msj = actualizarCoordinadorModel(idC, n, nuip, estado, salario)
    if exito: messagebox.showinfo("Éxito", msj)
    else: messagebox.showerror("Error", msj)
    return exito

def eliminarCoordinadorController(idC):
    exito, msj = eliminarCoordinadorModel(idC)
    if exito: messagebox.showinfo("Éxito", msj)
    return exito