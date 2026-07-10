"""
🌿 Sana - Sistema de Buzón
Notificaciones de contenido compartido para todos los usuarios
"""

import json, os
from datetime import datetime

class Buzon:
    def __init__(self):
        self.mensajes = {}
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/buzon.json"):
                with open("datos/buzon.json", "r") as f:
                    self.mensajes = json.load(f)
        except:
            self.mensajes = {}

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/buzon.json", "w") as f:
            json.dump(self.mensajes, f, indent=2, ensure_ascii=False)

    def enviar(self, destino, remitente, tipo, contenido, id_referencia):
        """Envía un mensaje al buzón del destinatario"""
        if destino not in self.mensajes:
            self.mensajes[destino] = []
        
        msg = {
            "id": len(self.mensajes[destino]) + 1,
            "remitente": remitente,
            "tipo": tipo,  # "bitacora", "guia", "plan", "aviso"
            "contenido": contenido,
            "id_referencia": id_referencia,
            "fecha": datetime.now().isoformat(),
            "leido": False
        }
        self.mensajes[destino].append(msg)
        self._guardar()
        return msg

    def obtener(self, destino):
        """Obtiene mensajes del buzón"""
        return self.mensajes.get(destino, [])

    def no_leidos(self, destino):
        """Cuenta mensajes no leídos"""
        return len([m for m in self.mensajes.get(destino, []) if not m["leido"]])

    def marcar_leido(self, destino, id_mensaje):
        """Marca un mensaje como leído"""
        for m in self.mensajes.get(destino, []):
            if m["id"] == id_mensaje:
                m["leido"] = True
                self._guardar()
                return True
        return False

    def eliminar(self, destino, id_mensaje):
        """Elimina un mensaje"""
        if destino in self.mensajes:
            self.mensajes[destino] = [m for m in self.mensajes[destino] if m["id"] != id_mensaje]
            self._guardar()
            return True
        return False
