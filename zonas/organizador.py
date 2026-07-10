"""
🌿 Sana - Organizador con compartir universal
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
            json.dump({"planes": self.planes, "tareas": self.tareas}, f, indent=2, ensure_ascii=False)

    def crear_plan(self, nombre, materia, objetivo, actividades, escuela, autor, visibilidad="privado", alumno_id=None):
        plan = {
            "id": len(self.planes) + 1,
            "nombre": nombre, "materia": materia, "objetivo": objetivo,
            "actividades": actividades, "escuela": escuela, "autor": autor,
            "visibilidad": visibilidad, "alumno_id": alumno_id,
            "compartido_con": [], "visible_para": [],
            "fecha": datetime.now().isoformat(), "estado": "activo"
        }
        self.planes.append(plan)
        self._guardar()
        return plan

    def obtener_planes(self, escuela=None, visibilidad=None):
        resultado = self.planes
        if escuela: resultado = [p for p in resultado if p["escuela"] == escuela]
        if visibilidad: resultado = [p for p in resultado if p["visibilidad"] == visibilidad]
        return resultado

    def obtener_planes_publicos(self):
        return [p for p in self.planes if p["visibilidad"] == "publico"]

    def obtener_planes_alumno(self, alumno_id):
        return [p for p in self.planes if alumno_id in p.get("compartido_con", []) or p.get("alumno_id") == alumno_id or alumno_id in p.get("visible_para", [])]

    def obtener_planes_docente(self, autor, escuela):
        return [p for p in self.planes if p["autor"] == autor and p["escuela"] == escuela]

    def compartir_plan(self, id_plan, destino):
        for p in self.planes:
            if p["id"] == id_plan:
                if "compartido_con" not in p: p["compartido_con"] = []
                if "visible_para" not in p: p["visible_para"] = []
                if destino not in p["compartido_con"]: p["compartido_con"].append(destino)
                if destino not in p["visible_para"]: p["visible_para"].append(destino)
                if p["visibilidad"] == "privado": p["visibilidad"] = "compartido"
                self._guardar()
                return True
        return False

    def hacer_publico(self, id_plan):
        for p in self.planes:
            if p["id"] == id_plan: p["visibilidad"] = "publico"; self._guardar(); return True
        return False

    def hacer_privado(self, id_plan):
        for p in self.planes:
            if p["id"] == id_plan: p["visibilidad"] = "privado"; self._guardar(); return True
        return False

    def agregar_tarea(self, titulo, materia, carga, fecha_limite, alumno_id=None):
        tarea = {"id": len(self.tareas) + 1, "titulo": titulo, "materia": materia, "carga_mental": carga, "fecha_limite": fecha_limite, "alumno_id": alumno_id, "completada": False, "fecha": datetime.now().isoformat()}
        self.tareas.append(tarea); self._guardar(); return tarea

    def obtener_tareas(self, alumno_id=None):
        if alumno_id: return [t for t in self.tareas if t.get("alumno_id") == alumno_id]
        return self.tareas

    def completar_tarea(self, id_tarea):
        for t in self.tareas:
            if t["id"] == id_tarea: t["completada"] = True; break
        self._guardar()

    def eliminar_plan(self, id_plan):
        self.planes = [p for p in self.planes if p["id"] != id_plan]
        self._guardar()
        return True
