from config.connection import get_connection

def crearClienteModel(nombre, email, telefono, nuip, nombreUsuarioDigitado):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO cliente (nombre, email, telefono, nuip, idUsuario) SELECT %s, %s, %s, %s, idUsuario FROM usuario WHERE nombreUsuario = %s"
            cursor.execute(query, (nombre, email, telefono, nuip, nombreUsuarioDigitado))
            
            if cursor.rowcount == 0:
                return False, "Error: El nombre de usuario no existe en el sistema."
            
            conn.commit()
            return True, "Cliente registrado exitosamente"
        except Exception as e:
            return False, f"Error al registrar cliente: {str(e)}"
        finally:
            cursor.close()
            conn.close()

def listarClientesModel():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT cliente.*, usuario.nombreUsuario FROM cliente INNER JOIN usuario ON cliente.idUsuario = usuario.idUsuario"
            cursor.execute(query)
            clientes = cursor.fetchall()
            return clientes, "" 
        except Exception as e:
            return None, f"Error al listar clientes: {str(e)}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def actualizarClienteModel(idCliente, nombre, email, telefono, nuip):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE cliente SET nombre=%s, email=%s, telefono=%s, nuip=%s WHERE idCliente=%s"
            cursor.execute(query, (nombre, email, telefono, nuip, idCliente))
            conn.commit()
            return True, "Cliente actualizado con éxito"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

def eliminarClienteModel(idCliente):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "delete from cliente where idCliente = %s"
            cursor.execute(query, (idCliente,))
            conn.commit()
            return True, "Cliente eliminado éxitosamente"
        except Exception as e:
            return False, f"Error al eliminar cliente: {str(e)}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()