from config.connection import get_connection

def crearEventoClienteModel(nombre, fecha, estadoEvento, estadoPago, presupuesto, usuario, coordinador, sede):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()

            query = """
            insert into evento (nombre, fecha, estadoEvento, estadoPago, presupuesto, idCliente, idCoordinador, idSede) 
            select %s, %s, %s, %s, %s, c.idCliente, cr.idCoordinador, s.idSede from cliente c
            inner join usuario u on u.idUsuario = c.idUsuario
            inner join coordinador cr on cr.nombre = %s
            inner join sede s on s.nombre = %s
            where u.nombreUsuario = %s;"""

            cursor.execute(query, (nombre, fecha, estadoEvento, estadoPago, presupuesto, coordinador, sede, usuario))
            conn.commit()
            return True, "Evento registrado éxitosamente"
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def listarEventosClienteModel(usuario):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            select e.idEvento, e.nombre, c.nombre, e.fecha, e.presupuesto, s.nombre from evento e
            inner join sede s on s.idSede = e.idSede
            inner join usuario u on u.nombreUsuario = %s
            inner join cliente c on c.idUsuario = u.idUsuario 
            where c.idCliente = e.idCliente"""
            cursor.execute(query, (usuario,))
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            return None, f"Error: {e}"
        finally:
            if 'cursor' in locals(): 
                cursor.close()
            conn.close()

def eliminarEventoModel(idEvento):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM evento WHERE idEvento = %s;", (idEvento,))
            conn.commit()
            return True, "Eliminado correctamente"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()

def actualizarEventoClienteModel(idEvento, nombre, fecha, estadoEvento, estadoPago, presupuesto, usuario, coordinador, sede):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            update evento e
            inner join usuario u on u.nombreUsuario = %s
            inner join cliente c on c.idUsuario = u.idUsuario
            inner join coordinador cr on cr.nombre = %s
            inner join sede s on s.nombre = %s set
            e.nombre = %s,
            e.fecha = %s,
            e.estadoEvento = %s,
            e.estadoPago = %s,
            e.presupuesto = %s,
            e.idCliente = c.idCliente,
            e.idCoordinador = cr.idCoordinador,
            e.idSede = s.idSede
            where e.idEvento = %s"""
            cursor.execute(query, (usuario, coordinador, sede, nombre, fecha, estadoEvento, estadoPago, presupuesto, idEvento))
            conn.commit()
            return True, "Evento actualizado éxitosamente"
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

# CRUD ADMIN

def crearEventoAdminModel(nombre, fecha, estadoEvento, estadoPago, presupuesto, nombreCliente, nombreCoordinador, nombreSede, proovedor):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()

            query_e = """INSERT INTO evento (nombre, fecha, estadoEvento, estadoPago, presupuesto, idCliente, idCoordinador, idSede)
            SELECT 
                %s,             
                %s,       
                %s,
                %s,       
                %s,         
                c.idCliente, 
                cr.idCoordinador, 
                s.idSede
            FROM cliente c
            CROSS JOIN coordinador cr
            CROSS JOIN sede s
            WHERE c.nombre = %s AND cr.nombre = %s AND s.nombre = %s LIMIT 1"""
            cursor.execute(query_e, (nombre, fecha, estadoEvento, estadoPago, presupuesto, nombreCliente, nombreCoordinador, nombreSede))
            
            id_evento = cursor.lastrowid
            costo_evento = obtenerCostoTotalEventoModel(id_evento)
            
            query_d = """
            insert into detalles_evento (
            costoEvento,
            idEvento,
            idProovedor) select %s, %s,
            p.idProovedor from proovedor p
            where p.empresa = %s"""
            cursor.execute(query_d, (costo_evento, id_evento, proovedor))

            conn.commit()
            return True, "Evento registrado éxitosamente"
        except Exception as e:
            return False, f"Error al registrar: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def crearDetallesAdminModel(idEvento, proovedor):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            costo_evento = obtenerCostoTotalEventoModel(idEvento)
            
            query_d = """
            insert into detalles_evento (
            costoEvento,
            idEvento,
            idProovedor) select %s, %s,
            p.idProovedor from proovedor p
            where p.empresa = %s"""
            cursor.execute(query_d, (costo_evento, idEvento, proovedor))

            conn.commit()
            return True, "Detalles del evento registrados éxitosamente"
        except Exception as e:
            return False, f"Error al registrar: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def listarEventosAdminModel():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            select e.idEvento, 
            e.nombre, 
            e.fecha, 
            e.estadoEvento,
            e.estadoPago, 
            e.presupuesto, 
            c.nombre, 
            cr.nombre, 
            s.nombre,
            max(d.costoEvento)
            from evento e
            left join detalles_evento d on d.idEvento = e.idEvento
            inner join cliente c on e.idCliente = c.idCliente
            inner join coordinador cr on e.idCoordinador = cr.idCoordinador
            inner join sede s on e.idSede = s.idSede
            group by e.idEvento"""
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            return None, f"Error al listar: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def listarEventosDetallesAdminModel():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            select 
            d.idDetalles, 
            c.nombre,
            e.nombre,
            d.costoEvento, 
            p.empresa, 
            p.costoServicio
            from detalles_evento d
            inner join evento e on e.idEvento = d.idEvento
            inner join cliente c on c.idCliente = e.idCliente
            inner join proovedor p on p.idProovedor = d.idProovedor
            order by c.nombre"""
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            return None, f"Error al listar: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def actualizarEventosAdminModel(nombreCliente, nombreCoordinador, nombreSede, nombre, fecha, estadoEvento,idEvento, estadoPago, idDetalles):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query_e = """
            UPDATE evento e
            INNER JOIN cliente c ON c.nombre = %s
            INNER JOIN coordinador cr ON cr.nombre = %s
            INNER JOIN sede s ON s.nombre = %s
            SET 
                e.nombre = %s,
                e.fecha = %s,
                e.estadoEvento = %s,
                e.estadoPago = %s,
                e.idCliente = c.idCliente,
                e.idCoordinador = cr.idCoordinador,
                e.idSede = s.idSede
            WHERE e.idEvento = %s"""
            cursor.execute(query_e, (nombreCliente, nombreCoordinador, nombreSede, nombre, fecha, estadoEvento, estadoPago, idEvento))

            costo_evento = obtenerCostoTotalEventoModel(idEvento)

            query_d = """
            update detalles_evento d 
            set
            d.costoEvento = %s,
            where d.idDetalles = %s"""
            cursor.execute(query_d, (costo_evento, idDetalles))

            conn.commit()
            return True, "Evento actualizado éxitosamente"
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def eliminarEventoDetallesModel(idDetalles):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detalles_evento WHERE idDetalles = %s;", (idDetalles,))
            conn.commit()
            return True, "Eliminado correctamente"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()

# HELPERS

def filtrarEventosAdminModel(estado_evento, estado_pago, coordinador, cliente):
    conn = get_connection()
    if not conn:
        return {"eventos": [], "detalles": []}

    try:
        cursor = conn.cursor()
        
        # 1. Filtrar Tabla Principal de Eventos
        query_eventos = """
            SELECT e.idEvento, e.nombre, e.fecha, e.estadoEvento, e.estadoPago, 
                    e.presupuesto, c.nombre, cr.nombre, s.nombre, MAX(d.costoEvento)
            FROM evento e
            LEFT JOIN detalles_evento d ON d.idEvento = e.idEvento
            INNER JOIN cliente c ON e.idCliente = c.idCliente
            INNER JOIN coordinador cr ON e.idCoordinador = cr.idCoordinador
            INNER JOIN sede s ON e.idSede = s.idSede
            WHERE 1=1
        """
        params = []
        if estado_evento != "TODOS":
            query_eventos += " AND e.estadoEvento = %s"
            params.append(estado_evento)
        if estado_pago != "TODOS":
            query_eventos += " AND e.estadoPago = %s"
            params.append(estado_pago)
        if coordinador != "TODOS":
            query_eventos += " AND cr.nombre = %s"
            params.append(coordinador)
        if cliente != "TODOS":
            query_eventos += " AND c.nombre = %s"
            params.append(cliente)
            
        query_eventos += " GROUP BY e.idEvento"
        cursor.execute(query_eventos, tuple(params))
        eventos_res = cursor.fetchall()

        # 2. Filtrar Tabla de Detalles
        query_detalles = """
            SELECT d.idDetalles, c.nombre, e.nombre, d.costoEvento, p.empresa, p.costoServicio
            FROM detalles_evento d
            INNER JOIN evento e ON e.idEvento = d.idEvento
            INNER JOIN cliente c ON c.idCliente = e.idCliente
            INNER JOIN proovedor p ON p.idProovedor = d.idProovedor
            WHERE 1=1
        """
        params_d = []
        if estado_evento != "TODOS":
            query_detalles += " AND e.estadoEvento = %s"
            params_d.append(estado_evento)
        if estado_pago != "TODOS":
            query_detalles += " AND e.estadoPago = %s"
            params_d.append(estado_pago)
        if coordinador != "TODOS":
            query_detalles += " AND e.idCoordinador = (SELECT idCoordinador FROM coordinador WHERE nombre = %s)"
            params_d.append(coordinador)
        if cliente != "TODOS":
            query_detalles += " AND c.nombre = %s"
            params_d.append(cliente)
            
        query_detalles += " ORDER BY c.nombre"
        cursor.execute(query_detalles, tuple(params_d))
        detalles_res = cursor.fetchall()

        return {
            "eventos": eventos_res,
            "detalles": detalles_res
        }
    except Exception as e:
        print(f"Error al filtrar eventos: {e}")
        return {"eventos": [], "detalles": []}
    finally:
        cursor.close()
        conn.close()

def obtenerNombresCoordinadoresModel():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM coordinador")
        res = [f[0] for f in cursor.fetchall()]
        cursor.close()
        return res

def obtenerNombresSedesModel():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM sede")
        res = [f[0] for f in cursor.fetchall()]
        cursor.close()
        return res

def obtenerEmpresasProveedoresModel():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT empresa FROM proovedor")
        res = [f[0] for f in cursor.fetchall()]
        cursor.close()
        return res

def obtenerNombreClientes():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "select c.nombre from cliente c"
        cursor.execute(query)
        res = [f[0] for f in cursor.fetchall()]
        cursor.close()
        return res

def obtenerCostoTotalEventoModel(idEvento):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            SELECT (s.costoAlquiler + c.salario + COALESCE(SUM(p.costoServicio), 0))
            FROM evento e
            INNER JOIN sede s ON e.idSede = s.idSede
            INNER JOIN coordinador c ON e.idCoordinador = c.idCoordinador
            LEFT JOIN detalles_evento d ON e.idEvento = d.idEvento
            LEFT JOIN proovedor p ON d.idProovedor = p.idProovedor
            WHERE e.idEvento = %s
            -- GROUP BY e.idEvento, s.costoAlquiler, c.salario
            """
            cursor.execute(query, (idEvento,))
            res = cursor.fetchone()
            
            if res and res[0] is not None:
                return float(res[0]) 
            return 0.0
            
        except Exception as e:
            print(f"Error en obtenerCostoTotal: {e}")
            return 0.0
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
    return 0.0