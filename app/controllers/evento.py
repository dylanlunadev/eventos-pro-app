from app.models.evento import *

def obtenerListas():
    return {
        "coordinadores": obtenerNombresCoordinadoresModel() or [],
        "sedes": obtenerNombresSedesModel() or [],
        "proovedores": obtenerEmpresasProveedoresModel() or [],
        "clientes": obtenerNombreClientes() or []
    }

# CONTROLLERS CLIENTE

def guardarEventoClienteController(id_ev, nombre, fecha, estadoEvento, estadoPago, presupuesto, idUsuario, coordinador, sede):
    if estadoEvento == "CONFIRMADO":
        res_costo = obtenerCostoTotalEventoModel(id_ev)
        if res_costo:
            costo_total = res_costo[5]
            if costo_total < float(presupuesto):
                return False, f"Presupuesto insuficiente. Costo actual: ${costo_total}"
    if not id_ev:
        return crearEventoClienteModel(nombre, fecha, estadoEvento, estadoPago, presupuesto, idUsuario, coordinador, sede)
    else:
        return actualizarEventoClienteModel(id_ev, nombre, fecha, estadoEvento, estadoPago, presupuesto, idUsuario, coordinador, sede)

def listarEventosClienteController(usuario):
    return listarEventosClienteModel(usuario)

def eliminarEventoController(id_ev):
    return eliminarEventoModel(id_ev)

# CONTROLLERS ADMIN

def guardarEventoAdminController(idEvento, nombre, fecha, estadoEvento, estadoPago, presupuesto, nombreCliente, nombreCoordinador, nombreSede, proovedor, idDetalle):
    if estadoEvento == "CONFIRMADO":
        costo_total = obtenerCostoTotalEventoModel(idEvento)
        if costo_total:
            if float(costo_total) > float(presupuesto):
                return False, f"Presupuesto insuficiente. Costo actual: ${costo_total}"
    if not idEvento and not idDetalle:
        return crearEventoAdminModel(nombre, fecha, estadoEvento, estadoPago, presupuesto, nombreCliente, nombreCoordinador, nombreSede, proovedor)
    else:
        return actualizarEventosAdminModel(nombreCliente, nombreCoordinador, nombreSede, nombre, fecha, estadoEvento, estadoPago,idEvento, proovedor, idDetalle)

def guardarDetallesAdminController(idEvento, proovedor):
    return crearDetallesAdminModel(idEvento, proovedor)

def listarEventosAdminController():
    return listarEventosAdminModel()

def listarEventosDetallesAdminController():
    return listarEventosDetallesAdminModel()

def eliminarEventoDetallesController(idDetalles):
    return eliminarEventoDetallesModel(idDetalles)

def filtrarEventosController(estado_e, estado_p, coord, cliente):
    return filtrarEventosAdminModel(estado_e, estado_p, coord, cliente)