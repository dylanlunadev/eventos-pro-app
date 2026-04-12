from config.connection import get_connection
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def db_get_eventos_por_estado():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT estadoEvento, COUNT(*) as total FROM evento GROUP BY estadoEvento")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def db_get_ingresos_por_periodo():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT DATE_FORMAT(fecha, '%Y-%m') as periodo, SUM(presupuesto) as total 
        FROM evento 
        GROUP BY periodo 
        ORDER BY periodo ASC
    """
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res