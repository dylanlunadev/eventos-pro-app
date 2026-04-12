from config.connection import get_connection

def crearSedeModel(nombre, direccion, capacidad, costo):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO sede (nombre, direccion, capacidad, costoAlquiler) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, direccion, capacidad, costo))
            conn.commit()
            return True, "Sede registrada correctamente"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

def listarSedesModel():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sede")
            return cursor.fetchall(), ""
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            conn.close()

def actualizarSedeModel(idS, nombre, direccion, capacidad, costo):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE sede SET nombre=%s, direccion=%s, capacidad=%s, costoAlquiler=%s WHERE idSede=%s"
            cursor.execute(query, (nombre, direccion, capacidad, costo, idS))
            conn.commit()
            return True, "Sede actualizada"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

def eliminarSedeModel(idS):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sede WHERE idSede=%s", (idS,))
            conn.commit()
            return True, "Sede eliminada"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()