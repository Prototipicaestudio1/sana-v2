"""
🌿 Sana - Gestión de Escuelas y Códigos de Acceso
"""

import json, os, random, string
from datetime import datetime

class Escuelas:
    def __init__(self):
        self.escuelas = {}
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/escuelas.json"):
                with open("datos/escuelas.json", "r") as f:
                    self.escuelas = json.load(f)
        except:
            self.escuelas = {}

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/escuelas.json", "w") as f:
            json.dump(self.escuelas, f, indent=2)

    def _gen_codigo(self, prefijo="SAN"):
        return f"{prefijo}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

    def registrar_escuela(self, nombre, num_docentes, num_admin):
        codigo_escuela = self._gen_codigo("ESC")
        codigos_docentes = [self._gen_codigo("DOC") for _ in range(num_docentes)]
        codigos_admin = [self._gen_codigo("ADM") for _ in range(num_admin)]

        self.escuelas[codigo_escuela] = {
            "nombre": nombre,
            "codigo_escuela": codigo_escuela,
            "num_docentes": num_docentes,
            "num_admin": num_admin,
            "codigos_docentes": codigos_docentes,
            "codigos_admin": codigos_admin,
            "fecha_creacion": datetime.now().isoformat(),
            "docentes_registrados": [],
            "material": [],
            "planes": []
        }
        self._guardar()
        return self.escuelas[codigo_escuela]

    def obtener_escuela(self, codigo_escuela):
        return self.escuelas.get(codigo_escuela)

    def listar_escuelas(self):
        return list(self.escuelas.values())

    def validar_codigo_docente(self, codigo):
        for escuela in self.escuelas.values():
            if codigo in escuela.get("codigos_docentes", []):
                return {"valido": True, "escuela": escuela["nombre"], "codigo_escuela": escuela["codigo_escuela"], "tipo": "docente"}
        return {"valido": False}

    def validar_codigo_admin(self, codigo):
        for escuela in self.escuelas.values():
            if codigo in escuela.get("codigos_admin", []):
                return {"valido": True, "escuela": escuela["nombre"], "codigo_escuela": escuela["codigo_escuela"], "tipo": "admin"}
        return {"valido": False}

    def validar_codigo(self, codigo):
        docente = self.validar_codigo_docente(codigo)
        if docente["valido"]:
            return docente
        admin = self.validar_codigo_admin(codigo)
        if admin["valido"]:
            return admin
        return {"valido": False}

    def agregar_material(self, codigo_escuela, material):
        if codigo_escuela in self.escuelas:
            self.escuelas[codigo_escuela]["material"].append({
                **material,
                "fecha": datetime.now().isoformat()
            })
            self._guardar()
            return True
        return False

    def obtener_material(self, codigo_escuela):
        return self.escuelas.get(codigo_escuela, {}).get("material", [])

    def agregar_plan(self, codigo_escuela, plan):
        if codigo_escuela in self.escuelas:
            self.escuelas[codigo_escuela]["planes"].append({
                **plan,
                "fecha": datetime.now().isoformat()
            })
            self._guardar()
            return True
        return False

    def obtener_planes(self, codigo_escuela):
        return self.escuelas.get(codigo_escuela, {}).get("planes", [])
