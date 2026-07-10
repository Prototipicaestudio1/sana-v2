"""
🌿 Sana - Bitácora Escolar con compartir universal
"""

import json, os
from datetime import datetime

class Bitacora:
    TIPOS = ["observacion", "reporte", "recomendacion", "calificacion"]

    def __init__(self):
        self.entradas = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/bitacora.json"):
                with open("datos/bitacora.json", "r") as f:
                    data = json.load(f)
                    self.entradas = data if isinstance(data, list) else data.get("entradas", [])
        except:
            self.entradas = []

    def guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/bitacora.json", "w") as f:
            json.dump(self.entradas, f, indent=2, ensure_ascii=False)

    def agregar_entrada(self, tipo, alumno, grupo, texto, autor, escuela, publico=False, calificacion=None):
        if tipo not in self.TIPOS: tipo = "observacion"
        entrada = {
            "id": len(self.entradas) + 1,
            "tipo": tipo, "alumno": alumno.strip(), "grupo": grupo.strip(),
            "texto": texto.strip(), "autor": autor.strip(), "escuela": escuela.strip(),
            "publico": publico, "calificacion": calificacion,
            "fecha": datetime.now().isoformat(),
            "compartido_con": [], "visible_para": []
        }
        self.entradas.append(entrada)
        self.guardar()
        return entrada

    def obtener_entradas(self, escuela=None):
        if escuela: return [e for e in self.entradas if e.get("escuela") == escuela]
        return self.entradas

    def compartir_entrada(self, id_entrada, destino):
        for e in self.entradas:
            if e["id"] == id_entrada:
                if "compartido_con" not in e: e["compartido_con"] = []
                if "visible_para" not in e: e["visible_para"] = []
                if destino not in e["compartido_con"]: e["compartido_con"].append(destino)
                if destino not in e["visible_para"]: e["visible_para"].append(destino)
                self.guardar()
                return True
        return False

    def obtener_compartidas(self, destino):
        return [e for e in self.entradas if destino in e.get("compartido_con", [])]

    def obtener_visibles(self, destino):
        return [e for e in self.entradas if destino in e.get("visible_para", []) or e.get("escuela") == destino]

    def eliminar_entrada(self, id_entrada):
        self.entradas = [e for e in self.entradas if e["id"] != id_entrada]
        self.guardar()
        return True
