# apps/produccion/utils/turno_utils.py

from datetime import time
from django.utils.timezone import localtime
import apps.produccion.models.turno as turno_models


def obtener_turno_actual():
    """
    Devuelve el TurnoTrabajo actual según la hora local.
    """
    ahora = localtime().time()
    hoy = localtime().date()

    

    turnos_de_hoy = turno_models.TurnoTrabajo.objects.select_related('turno').filter(fecha=hoy)

    print(f"⏰ Ahora: {ahora}, Fecha: {hoy}")
    for turno_trabajo in turnos_de_hoy:
        print(f"🔍 Evaluando: {turno_trabajo.turno.shift} ({turno_trabajo.turno.start_time} - {turno_trabajo.turno.end_time})")
        if turno_trabajo.turno.start_time <= ahora <= turno_trabajo.turno.end_time:
            return turno_trabajo

    return None


def obtener_usuarios_en_turno_actual():
    """
    Devuelve un diccionario con usuarios por rol que están asignados al turno actual.
    """
    turno_actual = obtener_turno_actual()
    if not turno_actual:
        return None

    asignaciones = turno_actual.asignacionturno_set.select_related('usuario')

    usuarios_por_rol = {
        'OPERADOR': [],
        'REVISADOR': [],
        'AUXILIAR': []
    }

    for asignacion in asignaciones:
        rol = asignacion.usuario.role.upper()  # Asegúrate que los roles estén en mayúsculas
        if rol in usuarios_por_rol:
            usuarios_por_rol[rol].append(asignacion.usuario)

    return usuarios_por_rol
