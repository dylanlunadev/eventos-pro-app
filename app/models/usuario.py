from config.connection import get_connection

def crearUsuarioModel(nombre_usuario, contrasenia, rol):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "insert into usuario(nombreUsuario, contrasenia, rol) values (%s, %s, %s)"
            cursor.execute(query, (nombre_usuario, contrasenia, rol))
            conn.commit()
            
            return True, "Registro exitoso"
        except Exception as e:
            return False, f"Error al registrar: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def leerUsuarioModel(nombreUsuario, contrasenia):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "SELECT idUsuario, nombreUsuario, rol, contrasenia FROM usuario WHERE nombreUsuario = %s"
            cursor.execute(query, (nombreUsuario,))
            user = cursor.fetchone()
            if user and user[3] == contrasenia:
                return True, {"id": user[0], "nombre": user[1], "rol": user[2] }
            else:
                return False, "Credenciales incorrectas"
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

def eliminarUsuarioModel(user_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            return True, "Usuario eliminado exitosamente"
        except Exception as e:
            return False, f"Error al eliminar usuario: {e}"
        finally:
            cursor.close()
            conn.close()

def actualizarUsusarioModel(user_id, nombre=None, contrasenia=None, roll=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            fields = []
            values = []
            if nombre:
                fields.append("nombre = %s")
                values.append(nombre)
            if contrasenia:
                fields.append("password = %s")
                values.append(contrasenia)
            if roll:
                fields.append("roll = %s")
                values.append(roll)
            values.append(user_id)
            query = f"UPDATE usuarios SET {', '.join(fields)} WHERE id = %s"
            cursor.execute(query, tuple(values))
            conn.commit()
            return True, "Usuario actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar usuario: {e}"
        finally:
            cursor.close()
            conn.close()