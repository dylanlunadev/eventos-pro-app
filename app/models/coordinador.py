from config.connection import get_connection

def crearCoordinadorModel(nombre, nuip, estado, salario):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO coordinador (nombre, nuip, estado, salario) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, nuip, estado, salario))
            conn.commit()
            return True, "Coordinador registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

def listarCoordinadoresModel():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coordinador")
            res = cursor.fetchall()
            return res, ""
        except Exception as e:
            return None, f"Error al listar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

def actualizarCoordinadorModel(idC, nombre, nuip, estado, salario):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE coordinador SET nombre=%s, nuip=%s, estado=%s, salario=%s WHERE idCoordinador=%s"
            cursor.execute(query, (nombre, nuip, estado, salario, idC))
            conn.commit()
            return True, "Datos actualizados correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

def eliminarCoordinadorModel(idC):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM coordinador WHERE idCoordinador = %s", (idC,))
            conn.commit()
            return True, "Coordinador eliminado"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
        finally:
            cursor.close()
            conn.close()