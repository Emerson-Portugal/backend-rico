#apps/produccion/notificaciones.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notificar_a_usuarios(usuarios, mensaje):
    channel_layer = get_channel_layer()

    for usuario in usuarios:
        if usuario:
            print(f"[NOTIFICACIÓN] A {usuario.username}: {mensaje}")
            async_to_sync(channel_layer.group_send)(
                f"notificaciones_{usuario.username}",
                {
                    "type": "recibir_notificacion",
                    "mensaje": mensaje
                }
            )

