"""
🌿 Sana - Bitácora Escolar con sistema de compartir
"""

import json, os
from datetime import datetime

class Bitacora:
    TIPOS = ["observacion", "reporte", "recomendacion", "calificacion"]

    def __init__(self):
        self.entradas = []
        self.compartidas = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/bitacora.json"):
                with open("datos/bitacora.json", "r") as f:
                    data = json.load(f)
                    self.entradas = data.get("entradas", [])
                    self.compartidas = data.get("compartidas", [])
        except:
            self.entradas = []
            self.compartidas = []

    def guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/bitacora.json", "w") as f:
            json.dump({"entradas": self.entradas, "compartidas": self.compartidas}, f, indent=2, ensure_ascii=False)

    def agregar_entrada(self, tipo, alumno, grupo, texto, autor, escuela, publico=False, calificacion=None):
        if tipo not in self.TIPOS: tipo = "observacion"
        entrada = {
            "id": len(self.entradas) + 1,
            "tipo": tipo, "alumno": alumno.strip(), "grupo": grupo.strip(),
            "texto": texto.strip(), "autor": autor.strip(), "escuela": escuela.strip(),
            "publico": publico, "calificacion": calificacion,
            "fecha": datetime.now().isoformat(), "compartido_con": []
        }
        self.entradas.append(entrada)
        self.guardar()
        return entrada

    def obtener_entradas(self, escuela=None):
        if escuela:
            return [e for e in self.entradas if e.get("escuela") == escuela]
        return self.entradas

    def compartir_entrada(self, id_entrada, codigo_docente):
        for e in self.entradas:
            if e["id"] == id_entrada:
                if "compartido_con" not in e: e["compartido_con"] = []
                if codigo_docente not in e["compartido_con"]:
                    e["compartido_con"].append(codigo_docente)
                self.guardar()
                return True
        return False

    def obtener_compartidas(self, codigo_docente):
        return [e for e in self.entradas if codigo_docente in e.get("compartido_con", [])]

    def eliminar_entrada(self, id_entrada):
        self.entradas = [e for e in self.entradas if e["id"] != id_entrada]
        self.guardar()
        return True
