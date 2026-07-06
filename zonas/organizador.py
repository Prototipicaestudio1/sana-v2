"""
🌿 Sana - Organizador de Planes Personalizados
"""

import json, os
from datetime import datetime

class Organizador:
    def __init__(self):
        self.planes = []
        self.tareas = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/organizador.json"):
                with open("datos/organizador.json", "r") as f:
                    data = json.load(f)
                    self.planes = data.get("planes", [])
                    self.tareas = data.get("tareas", [])
        except:
            self.planes = []
            self.tareas = []

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/organizador.json", "w") as f:
            json.dump({"planes": self.planes, "tareas": self.tareas}, f, indent=2)

    def crear_plan(self, nombre, materia, objetivo, actividades, escuela, autor):
        plan = {
            "id": len(self.planes) + 1,
            "nombre": nombre,
            "materia": materia,
            "objetivo": objetivo,
            "actividades": actividades,
            "escuela": escuela,
            "autor": autor,
            "fecha": datetime.now().isoformat(),
            "estado": "activo"
        }
        self.planes.append(plan)
        self._guardar()
        return plan

    def obtener_planes(self, escuela=None):
        if escuela:
            return [p for p in self.planes if p["escuela"] == escuela]
        return self.planes

    def agregar_tarea(self, titulo, materia, carga, fecha_limite):
        tarea = {
            "id": len(self.tareas) + 1,
            "titulo": titulo,
            "materia": materia,
            "carga_mental": carga,
            "fecha_limite": fecha_limite,
            "completada": False,
            "fecha": datetime.now().isoformat()
        }
        self.tareas.append(tarea)
        self._guardar()
        return tarea

    def obtener_tareas(self):
        return self.tareas

    def completar_tarea(self, id_tarea):
        for t in self.tareas:
            if t["id"] == id_tarea:
                t["completada"] = True
                break
        self._guardar()
