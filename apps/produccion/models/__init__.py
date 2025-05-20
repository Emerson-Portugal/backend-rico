# apps/produccion/models/__init__.py
from .producto import Producto
from .maquina import Maquina
from .turno import Turno
from .base import RegistroProduccionBase
from .R145 import RegistroR145

__all__ = ['Producto', 'Maquina', 'Turno', 'RegistroProduccionBase', 'RegistroR145']