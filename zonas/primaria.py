"""
🌿 Sana - Módulo de Escuelas Primarias
Grupos, anuncios para padres, muro de tareas
"""

import json, os
from datetime import datetime

class Primaria:
    def __init__(self):
        self.grupos = {}
        self.anuncios_padres = []
        self.muro_tareas = {}
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/primaria.json"):
                with open("datos/primaria.json", "r") as f:
                    data = json.load(f)
                    self.grupos = data.get("grupos", {})
                    self.anuncios_padres = data.get("anuncios_padres", [])
                    self.muro_tareas = data.get("muro_tareas", {})
        except:
            self.grupos = {}
            self.anuncios_padres = []
            self.muro_tareas = {}

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/primaria.json", "w") as f:
            json.dump({
                "grupos": self.grupos,
                "anuncios_padres": self.anuncios_padres,
                "muro_tareas": self.muro_tareas
            }, f, indent=2, ensure_ascii=False)

    # ──── GRUPOS ────
    def crear_grupo(self, escuela, nombre, docente):
        id_grupo = f"GRP-{len(self.grupos)+1:03d}"
        self.grupos[id_grupo] = {
            "id": id_grupo,
            "escuela": escuela,
            "nombre": nombre,
            "docente": docente,
            "fecha": datetime.now().isoformat(),
            "alumnos": []
        }
        if escuela not in self.muro_tareas:
            self.muro_tareas[escuela] = {}
        self.muro_tareas[escuela][id_grupo] = []
        self._guardar()
        return self.grupos[id_grupo]

    def obtener_grupos(self, escuela=None, docente=None):
        resultado = list(self.grupos.values())
        if escuela: resultado = [g for g in resultado if g["escuela"] == escuela]
        if docente: resultado = [g for g in resultado if g["docente"] == docente]
        return resultado

    def eliminar_grupo(self, id_grupo):
        if id_grupo in self.grupos:
            del self.grupos[id_grupo]
            self._guardar()
            return True
        return False

    # ──── ANUNCIOS PARA PADRES ────
    def publicar_anuncio_padres(self, escuela, titulo, mensaje, autor):
        anuncio = {
            "id": len(self.anuncios_padres) + 1,
            "escuela": escuela,
            "titulo": titulo,
            "mensaje": mensaje,
            "autor": autor,
            "fecha": datetime.now().isoformat(),
            "activo": True
        }
        self.anuncios_padres.append(anuncio)
        self._guardar()
        return anuncio

    def obtener_anuncios_padres(self, escuela):
        return [a for a in self.anuncios_padres if a["escuela"] == escuela and a["activo"]]

    def eliminar_anuncio_padres(self, id_anuncio):
        for a in self.anuncios_padres:
            if a["id"] == id_anuncio:
                a["activo"] = False
                self._guardar()
                return True
        return False

    # ──── MURO DE TAREAS ────
    def agregar_tarea(self, escuela, id_grupo, titulo, descripcion, fecha_entrega=None):
        tarea = {
            "id": len(self.muro_tareas.get(escuela, {}).get(id_grupo, [])) + 1,
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_entrega": fecha_entrega,
            "fecha": datetime.now().isoformat(),
            "completada": False
        }
        if escuela not in self.muro_tareas: self.muro_tareas[escuela] = {}
        if id_grupo not in self.muro_tareas[escuela]: self.muro_tareas[escuela][id_grupo] = []
        self.muro_tareas[escuela][id_grupo].append(tarea)
        self._guardar()
        return tarea

    def obtener_tareas(self, escuela, id_grupo):
        return self.muro_tareas.get(escuela, {}).get(id_grupo, [])

    def eliminar_tarea(self, escuela, id_grupo, id_tarea):
        if escuela in self.muro_tareas and id_grupo in self.muro_tareas[escuela]:
            self.muro_tareas[escuela][id_grupo] = [
                t for t in self.muro_tareas[escuela][id_grupo] if t["id"] != id_tarea
            ]
            self._guardar()
            return True
        return False
