"""
🌿 Sana - Módulo de Escuelas Primarias
Grupos con padres, códigos de acceso, economía de fichas
"""

import json, os, random, string
from datetime import datetime

class Primaria:
    def __init__(self):
        self.grupos = {}
        self.anuncios_padres = []
        self.muro_tareas = {}
        self.padres = {}
        self.fichas = {}  # Economía de fichas por padre
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/primaria.json"):
                with open("datos/primaria.json", "r") as f:
                    data = json.load(f)
                    self.grupos = data.get("grupos", {})
                    self.anuncios_padres = data.get("anuncios_padres", [])
                    self.muro_tareas = data.get("muro_tareas", {})
                    self.padres = data.get("padres", {})
                    self.fichas = data.get("fichas", {})
        except:
            self.grupos = {}
            self.anuncios_padres = []
            self.muro_tareas = {}
            self.padres = {}
            self.fichas = {}

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/primaria.json", "w") as f:
            json.dump({
                "grupos": self.grupos,
                "anuncios_padres": self.anuncios_padres,
                "muro_tareas": self.muro_tareas,
                "padres": self.padres,
                "fichas": self.fichas
            }, f, indent=2, ensure_ascii=False)

    def _gen_codigo(self):
        return f"PAD-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

    # ──── GRUPOS CON PADRES ────
    def crear_grupo(self, escuela, nombre, docente, padres_lista):
        """
        padres_lista: [{"nombre_padre": "...", "nombre_nino": "...", "relacion": "..."}, ...]
        """
        id_grupo = f"GRP-{len(self.grupos)+1:03d}"
        codigos_padres = []
        
        for i, padre_data in enumerate(padres_lista):
            codigo = self._gen_codigo()
            self.padres[codigo] = {
                "codigo": codigo,
                "nombre_padre": padre_data.get("nombre_padre", ""),
                "nombre_nino": padre_data.get("nombre_nino", ""),
                "relacion": padre_data.get("relacion", "Padre/Madre"),
                "id_grupo": id_grupo,
                "escuela": escuela,
                "fecha": datetime.now().isoformat()
            }
            codigos_padres.append(codigo)
            # Inicializar economía de fichas para este padre
            if codigo not in self.fichas:
                self.fichas[codigo] = {"tareas": [], "puntos": 0, "recompensas": []}

        self.grupos[id_grupo] = {
            "id": id_grupo,
            "escuela": escuela,
            "nombre": nombre,
            "docente": docente,
            "fecha": datetime.now().isoformat(),
            "num_padres": len(padres_lista),
            "codigos_padres": codigos_padres,
            "padres": padres_lista
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

    # ──── PADRES ────
    def login_padre(self, codigo):
        return self.padres.get(codigo)

    def obtener_padres_grupo(self, id_grupo):
        return {c: p for c, p in self.padres.items() if p.get("id_grupo") == id_grupo}

    # ──── ANUNCIOS PARA PADRES ────
    def publicar_anuncio_padres(self, escuela, titulo, mensaje, autor):
        anuncio = {
            "id": len(self.anuncios_padres) + 1,
            "escuela": escuela, "titulo": titulo,
            "mensaje": mensaje, "autor": autor,
            "fecha": datetime.now().isoformat(), "activo": True
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
            "titulo": titulo, "descripcion": descripcion,
            "fecha_entrega": fecha_entrega, "fecha": datetime.now().isoformat()
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

    # ──── ECONOMÍA DE FICHAS ────
    def agregar_ficha_tarea(self, codigo_padre, titulo, puntos, recompensa=None):
        if codigo_padre not in self.fichas:
            self.fichas[codigo_padre] = {"tareas": [], "puntos": 0, "recompensas": []}
        tarea_ficha = {
            "id": len(self.fichas[codigo_padre]["tareas"]) + 1,
            "titulo": titulo, "puntos": puntos,
            "completada": False, "fecha": datetime.now().isoformat()
        }
        self.fichas[codigo_padre]["tareas"].append(tarea_ficha)
        if recompensa:
            self.fichas[codigo_padre]["recompensas"].append({
                "nombre": recompensa, "puntos_necesarios": puntos, "activa": True
            })
        self._guardar()
        return tarea_ficha

    def completar_ficha_tarea(self, codigo_padre, id_tarea):
        if codigo_padre in self.fichas:
            for t in self.fichas[codigo_padre]["tareas"]:
                if t["id"] == id_tarea and not t["completada"]:
                    t["completada"] = True
                    self.fichas[codigo_padre]["puntos"] += t["puntos"]
                    self._guardar()
                    return True
        return False

    def obtener_fichas(self, codigo_padre):
        return self.fichas.get(codigo_padre, {"tareas": [], "puntos": 0, "recompensas": []})

    def eliminar_ficha_tarea(self, codigo_padre, id_tarea):
        if codigo_padre in self.fichas:
            self.fichas[codigo_padre]["tareas"] = [
                t for t in self.fichas[codigo_padre]["tareas"] if t["id"] != id_tarea
            ]
            self._guardar()
            return True
        return False
