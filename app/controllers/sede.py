from tkinter import messagebox
from app.models.sede import *

def crearSedeController(nombre, direccion, capacidad, costo):
    if not all([nombre, direccion, capacidad, costo]):
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return False
    
    n = nombre.upper()
    d = direccion.upper()

    return crearSedeModel(n, d, capacidad, costo)[0]

def listarSedesController():
    datos, err = listarSedesModel()
    return datos if datos is not None else []

def actualizarSedeController(idS, nombre, direccion, capacidad, costo):
    if not all([idS, nombre, direccion, capacidad, costo]):
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return False
    
    n = nombre.upper()
    d = direccion.upper()

    return actualizarSedeModel(idS, n, d, capacidad, costo)[0]

def eliminarSedeController(idS):
    return eliminarSedeModel(idS)[0]