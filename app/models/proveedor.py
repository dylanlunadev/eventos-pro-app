from config.connection import get_connection

def crearProovedorModel(empresa, telefono, email, servicio, costo):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO proovedor (empresa, telefono, email, servicioProducto, costoServicio) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (empresa, telefono, email, servicio, costo))
            conn.commit()
            return True, "Proveedor registrado con éxito"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            cursor.close()
            conn.close()

def listarProovedoresModel():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proovedor")
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            conn.close()

def actualizarProovedorModel(idP, empresa, telefono, email, servicio, costo):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE proovedor SET empresa=%s, telefono=%s, email=%s, servicioProducto=%s, costoServicio=%s WHERE idProovedor=%s"
            cursor.execute(query, (empresa, telefono, email, servicio, costo, idP))
            conn.commit()
            return True, "Proveedor actualizado"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

def eliminarProovedorModel(idP):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proovedor WHERE idProovedor=%s", (idP,))
            conn.commit()
            return True, "Proveedor eliminado"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()