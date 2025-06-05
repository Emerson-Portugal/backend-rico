# apps/produccion/models/__init__.py
from .producto import Producto
from .maquina import Maquina
from .turno import Turno, AsignacionTurno, TurnoTrabajo
from .base import RegistroProduccionBase
from .R145 import RegistroR145

__all__ = ['Producto', 'Maquina', 'Turno', 'RegistroProduccionBase', 'RegistroR145', 'AsignacionTurno', 'TurnoTrabajo']