# apps/produccion/utils/turno_utils.py

from django.utils.timezone import localtime
from apps.produccion.models.turno import AsignacionTurno
from datetime import time


def esta_dentro_del_rango(hora_actual, inicio, fin):
    """
    Evalúa si hora_actual está entre inicio y fin.
    Soporta rangos que cruzan medianoche.
    """
    if inicio < fin:
        return inicio <= hora_actual <= fin
    else:
        return hora_actual >= inicio or hora_actual <= fin


def obtener_asignacion_usuario_en_turno_actual(usuario):
    """
    Devuelve la asignación de turno del usuario si está activa y dentro del horario.
    """
    ahora = localtime()
    hora_actual = ahora.time()
    fecha_actual = ahora.date()

    asignaciones = AsignacionTurno.objects.select_related('turno_trabajo__turno').filter(
        usuario=usuario,
        turno_trabajo__fecha_inicio__lte=fecha_actual,
        turno_trabajo__fecha_fin__gte=fecha_actual,
    )

    for asignacion in asignaciones:
        turno = asignacion.turno_trabajo.turno
        if esta_dentro_del_rango(hora_actual, turno.start_time, turno.end_time):
            return asignacion  # solo una válida

    return None


def obtener_usuarios_en_turno_actual():
    """
    Devuelve un diccionario con usuarios por rol que están en un turno activo.
    """
    ahora = localtime()
    hora_actual = ahora.time()
    fecha_actual = ahora.date()

    asignaciones = AsignacionTurno.objects.select_related('turno_trabajo__turno', 'usuario').filter(
        turno_trabajo__fecha_inicio__lte=fecha_actual,
        turno_trabajo__fecha_fin__gte=fecha_actual,
    )

    usuarios_por_rol = {
        'OPERADOR': [],
        'REVISADOR': [],
        'AUXILIAR': [],
        'SUPERVISOR': [],
    }

    for asignacion in asignaciones:
        turno = asignacion.turno_trabajo.turno
        if esta_dentro_del_rango(hora_actual, turno.start_time, turno.end_time):
            rol = asignacion.usuario.role.upper()
            if rol in usuarios_por_rol:
                usuarios_por_rol[rol].append(asignacion.usuario)

    return usuarios_por_rol
