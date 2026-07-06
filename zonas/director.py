"""
🌿 Sana - Módulo de Director Escolar
Avisos, bajas de docentes, bitácora especial, reportes
"""

import json, os
from datetime import datetime

class Director:
    def __init__(self):
        self.avisos = []
        self.bajas = []
        self.bitacora_director = []
        self._cargar()

    def _cargar(self):
        try:
            if os.path.exists("datos/director.json"):
                with open("datos/director.json", "r") as f:
                    data = json.load(f)
                    self.avisos = data.get("avisos", [])
                    self.bajas = data.get("bajas", [])
                    self.bitacora_director = data.get("bitacora_director", [])
        except:
            self.avisos = []
            self.bajas = []
            self.bitacora_director = []

    def _guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/director.json", "w") as f:
            json.dump({
                "avisos": self.avisos,
                "bajas": self.bajas,
                "bitacora_director": self.bitacora_director
            }, f, indent=2, ensure_ascii=False)

    # ──── AVISOS ────
    def publicar_aviso(self, escuela, titulo, mensaje, autor):
        aviso = {
            "id": len(self.avisos) + 1,
            "escuela": escuela,
            "titulo": titulo,
            "mensaje": mensaje,
            "autor": autor,
            "fecha": datetime.now().isoformat(),
            "activo": True
        }
        self.avisos.append(aviso)
        self._guardar()
        return aviso

    def obtener_avisos(self, escuela):
        return [a for a in self.avisos if a["escuela"] == escuela and a["activo"]]

    def eliminar_aviso(self, id_aviso):
        for a in self.avisos:
            if a["id"] == id_aviso:
                a["activo"] = False
                self._guardar()
                return True
        return False

    # ──── BAJAS DE DOCENTES ────
    def dar_baja_docente(self, escuela, codigo_docente, motivo, autor):
        baja = {
            "id": len(self.bajas) + 1,
            "escuela": escuela,
            "codigo_docente": codigo_docente,
            "motivo": motivo,
            "autor": autor,
            "fecha": datetime.now().isoformat(),
            "reporte_enviado": False
        }
        self.bajas.append(baja)
        self._guardar()
        return baja

    def obtener_bajas(self, escuela=None):
        if escuela:
            return [b for b in self.bajas if b["escuela"] == escuela]
        return self.bajas

    def generar_reporte_mensual(self, escuela):
        """Genera reporte de bajas del mes actual"""
        mes_actual = datetime.now().month
        bajas_mes = [b for b in self.bajas 
                     if b["escuela"] == escuela 
                     and datetime.fromisoformat(b["fecha"]).month == mes_actual]
        return {
            "escuela": escuela,
            "mes": mes_actual,
            "total_bajas": len(bajas_mes),
            "bajas": bajas_mes,
            "fecha_reporte": datetime.now().isoformat()
        }

    # ──── BITÁCORA DEL DIRECTOR ────
    def agregar_bitacora(self, escuela, texto, autor, compartir_con=None):
        entrada = {
            "id": len(self.bitacora_director) + 1,
            "escuela": escuela,
            "texto": texto,
            "autor": autor,
            "fecha": datetime.now().isoformat(),
            "compartido_con": compartir_con or [],
            "tipo": "director"
        }
        self.bitacora_director.append(entrada)
        self._guardar()
        return entrada

    def obtener_bitacora(self, escuela=None, codigo_destino=None):
        resultado = self.bitacora_director
        if escuela:
            resultado = [b for b in resultado if b["escuela"] == escuela]
        if codigo_destino:
            resultado = [b for b in resultado if codigo_destino in b.get("compartido_con", [])]
        return resultado

    def compartir_bitacora(self, id_entrada, codigo):
        for b in self.bitacora_director:
            if b["id"] == id_entrada:
                if "compartido_con" not in b:
                    b["compartido_con"] = []
                if codigo not in b["compartido_con"]:
                    b["compartido_con"].append(codigo)
                self._guardar()
                return True
        return False
