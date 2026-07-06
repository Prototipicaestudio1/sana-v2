"""
🌿 Sana - Red de Apoyo y Alertas
"""

import json, os

class Alertas:
    def __init__(self):
        self.red_apoyo = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/alertas.json"):
                with open("datos/alertas.json", "r") as f:
                    self.red_apoyo = json.load(f)
        except:
            self.red_apoyo = []

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/alertas.json", "w") as f:
            json.dump(self.red_apoyo, f, indent=2)

    def agregar_contacto(self, nombre, telefono, relacion, escuela):
        contacto = {
            "id": len(self.red_apoyo) + 1,
            "nombre": nombre,
            "telefono": telefono,
            "relacion": relacion,
            "escuela": escuela
        }
        self.red_apoyo.append(contacto)
        self._guardar()
        return contacto

    def obtener_red(self, escuela=None):
        if escuela:
            return [c for c in self.red_apoyo if c["escuela"] == escuela]
        return self.red_apoyo

    def eliminar_contacto(self, id_contacto):
        self.red_apoyo = [c for c in self.red_apoyo if c["id"] != id_contacto]
        self._guardar()
        return True
