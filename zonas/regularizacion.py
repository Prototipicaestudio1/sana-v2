"""
🌿 Sana - Material de Regularización con soporte PDF e imágenes
"""

import json, os, base64
from datetime import datetime

class Regularizacion:
    MATERIAS = [
        "Matemáticas", "Español", "Ciencias Naturales", "Historia",
        "Geografía", "Formación Cívica", "Inglés", "Educación Física",
        "Artes", "Tecnología"
    ]

    def __init__(self):
        self.material = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/regularizacion.json"):
                with open("datos/regularizacion.json", "r") as f:
                    self.material = json.load(f)
        except:
            self.material = []

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/regularizacion.json", "w") as f:
            json.dump(self.material, f, indent=2, ensure_ascii=False)

    def agregar_guia(self, materia, titulo, contenido, autor, escuela, archivo_base64=None, tipo_archivo=None, nombre_archivo=None):
        guia = {
            "id": len(self.material) + 1,
            "materia": materia,
            "titulo": titulo,
            "contenido": contenido,
            "autor": autor,
            "escuela": escuela,
            "fecha": datetime.now().isoformat(),
            "tiene_archivo": bool(archivo_base64),
            "tipo_archivo": tipo_archivo,
            "nombre_archivo": nombre_archivo,
            "archivo_base64": archivo_base64
        }
        self.material.append(guia)
        self._guardar()
        return guia

    def obtener_guias(self, materia=None, escuela=None):
        resultado = self.material
        if materia:
            resultado = [g for g in resultado if g["materia"] == materia]
        if escuela:
            resultado = [g for g in resultado if g["escuela"] == escuela]
        return resultado

    def obtener_materias(self):
        return self.MATERIAS

    def eliminar_guia(self, id_guia):
        self.material = [g for g in self.material if g["id"] != id_guia]
        self._guardar()
        return True

    def obtener_guia(self, id_guia):
        for g in self.material:
            if g["id"] == id_guia:
                return g
        return None
