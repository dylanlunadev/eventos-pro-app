from tkinter import messagebox
from app.models.proveedor import *

def crearProovedorController(emp, tel, mail, serv, costo):
    if not all([emp, tel, mail, serv, costo]):
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return False
    
    e = emp.upper()

    return crearProovedorModel(e, tel, mail, serv, costo)[0]

def listarProovedoresController():
    datos = listarProovedoresModel()
    return datos if datos is not None else []

def actualizarProovedorController(idP, emp, tel, mail, serv, costo):
    if not all([idP, emp, tel, mail, serv, costo]):
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return False
    
    e = emp.upper()

    return actualizarProovedorModel(idP, e, tel, mail, serv, costo)[0]

def eliminarProovedorController(idP):
    return eliminarProovedorModel(idP)[0]