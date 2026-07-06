"""
🌿 Sana - Sistema de Usuarios
Registro, login, perfiles para alumnos y profesores
"""

import json, os, random, string
from datetime import datetime

class Usuarios:
    def __init__(self):
        self.usuarios = {}
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/usuarios.json"):
                with open("datos/usuarios.json", "r") as f:
                    self.usuarios = json.load(f)
        except:
            self.usuarios = {}

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/usuarios.json", "w") as f:
            json.dump(self.usuarios, f, indent=2)

    def _gen_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def registrar(self, nombre, tipo, codigo_escuela=None, codigo_docente=None):
        user_id = self._gen_id()
        self.usuarios[user_id] = {
            "id": user_id,
            "nombre": nombre,
            "tipo": tipo,  # "alumno" o "docente"
            "codigo_escuela": codigo_escuela,
            "codigo_docente": codigo_docente,
            "fecha_registro": datetime.now().isoformat(),
            "diario": [],
            "bitacoras": [],
            "planes": [],
            "guias": []
        }
        self._guardar()
        return self.usuarios[user_id]

    def login(self, user_id):
        return self.usuarios.get(user_id)

    def obtener_por_id(self, user_id):
        return self.usuarios.get(user_id)

    def actualizar_perfil(self, user_id, nombre):
        if user_id in self.usuarios:
            self.usuarios[user_id]["nombre"] = nombre
            self._guardar()
            return True
        return False

    def agregar_diario(self, user_id, entrada):
        if user_id in self.usuarios:
            entrada["id"] = len(self.usuarios[user_id]["diario"]) + 1
            entrada["fecha"] = datetime.now().isoformat()
            self.usuarios[user_id]["diario"].append(entrada)
            self._guardar()
            return entrada
        return None

    def obtener_diario(self, user_id):
        return self.usuarios.get(user_id, {}).get("diario", [])

    def borrar_diario(self, user_id, entrada_id):
        if user_id in self.usuarios:
            self.usuarios[user_id]["diario"] = [
                e for e in self.usuarios[user_id]["diario"] if e["id"] != entrada_id
            ]
            self._guardar()
            return True
        return False

    def obtener_docentes_escuela(self, codigo_escuela):
        return [u for u in self.usuarios.values() if u["tipo"] == "docente" and u.get("codigo_escuela") == codigo_escuela]

    def obtener_todos(self):
        return list(self.usuarios.values())
