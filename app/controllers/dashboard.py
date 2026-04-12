from app.models.dashboard import *

def logica_obtener_datos_dashboard():
    # Datos crudos para las tablas
    estados = db_get_eventos_por_estado()
    ingresos = db_get_ingresos_por_periodo()
    
    # Procesamiento para gráficos
    labels_pie = [e['estadoEvento'] for e in estados]
    values_pie = [e['total'] for e in estados]
    
    labels_bar = [i['periodo'] for i in ingresos]
    values_bar = [i['total'] for i in ingresos]
    
    return {
        "tablas": {"estados": estados, "ingresos": ingresos},
        "graficos": {"pie": (labels_pie, values_pie), "bar": (labels_bar, values_bar)}
    }