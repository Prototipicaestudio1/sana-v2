"""
🌿 Sana - Módulo de Juegos HTML
Solo Admin puede agregar/quitar juegos
"""

import json, os
from datetime import datetime

class Juegos:
    def __init__(self):
        self.juegos = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/juegos.json"):
                with open("datos/juegos.json", "r") as f:
                    self.juegos = json.load(f)
        except:
            self.juegos = []

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/juegos.json", "w") as f:
            json.dump(self.juegos, f, indent=2, ensure_ascii=False)

    def agregar_juego(self, titulo, descripcion, html_code, categoria="general"):
        juego = {
            "id": len(self.juegos) + 1,
            "titulo": titulo,
            "descripcion": descripcion,
            "html_code": html_code,
            "categoria": categoria,
            "fecha": datetime.now().isoformat(),
            "activo": True
        }
        self.juegos.append(juego)
        self._guardar()
        return juego

    def obtener_juegos(self, categoria=None):
        resultado = [j for j in self.juegos if j["activo"]]
        if categoria: resultado = [j for j in resultado if j["categoria"] == categoria]
        return resultado

    def eliminar_juego(self, id_juego):
        for j in self.juegos:
            if j["id"] == id_juego:
                j["activo"] = False
                self._guardar()
                return True
        return False

    def obtener_juego(self, id_juego):
        for j in self.juegos:
            if j["id"] == id_juego: return j
        return None
