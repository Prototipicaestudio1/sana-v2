"""
🌿 Sana - Módulo de Bitácora Escolar
═══════════════════════════════════════════════════════════════
Registro de observaciones, reportes, recomendaciones y
calificaciones de alumnos. Compartible entre docentes de
la misma institución. 100% local · Persistencia JSON.
═══════════════════════════════════════════════════════════════
"""

import json
import os
from datetime import datetime


class Bitacora:
    """
    Bitácora escolar de Sana.
    
    Permite a docentes:
    - Registrar observaciones de alumnos
    - Crear reportes de comportamiento
    - Agregar recomendaciones personalizadas
    - Registrar calificaciones
    - Compartir entradas con otros docentes de la misma escuela
    - Editar y eliminar entradas propias
    - Filtrar por alumno, grupo, tipo, fecha
    """

    TIPOS = ["observacion", "reporte", "recomendacion", "calificacion"]

    def __init__(self):
        self.entradas = []
        self._asegurar_directorio()
        self.cargar()

    def _asegurar_directorio(self):
        if not os.path.exists("datos"):
            os.makedirs("datos", exist_ok=True)

    def cargar(self):
        try:
            if os.path.exists("datos/bitacora.json"):
                with open("datos/bitacora.json", "r", encoding="utf-8") as f:
                    self.entradas = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.entradas = []

    def guardar(self):
        self._asegurar_directorio()
        with open("datos/bitacora.json", "w", encoding="utf-8") as f:
            json.dump(self.entradas, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════════════
    # AGREGAR ENTRADAS
    # ═══════════════════════════════════════════════════════════

    def agregar_entrada(self, tipo: str, alumno: str, grupo: str,
                        texto: str, autor: str, escuela: str,
                        publico: bool = False, calificacion: float = None) -> dict:
        if tipo not in self.TIPOS:
            tipo = "observacion"

        entrada = {
            "id": len(self.entradas) + 1,
            "tipo": tipo,
            "alumno": alumno.strip(),
            "grupo": grupo.strip(),
            "texto": texto.strip(),
            "autor": autor.strip(),
            "escuela": escuela.strip(),
            "publico": publico,
            "calificacion": calificacion,
            "fecha": datetime.now().isoformat(),
            "editado": False,
            "fecha_edicion": None
        }
        self.entradas.append(entrada)
        self.guardar()
        return entrada

    # ═══════════════════════════════════════════════════════════
    # CONSULTAS
    # ═══════════════════════════════════════════════════════════

    def obtener_entradas(self, escuela: str = None, grupo: str = None,
                         alumno: str = None, tipo: str = None,
                         solo_publicas: bool = False,
                         autor: str = None) -> list:
        resultado = self.entradas.copy()

        if escuela:
            resultado = [e for e in resultado if e.get("escuela", "").upper() == escuela.upper()]
        if grupo:
            resultado = [e for e in resultado if e.get("grupo", "").upper() == grupo.upper()]
        if alumno:
            resultado = [e for e in resultado if alumno.lower() in e.get("alumno", "").lower()]
        if tipo:
            resultado = [e for e in resultado if e.get("tipo") == tipo]
        if solo_publicas:
            resultado = [e for e in resultado if e.get("publico", False)]
        if autor:
            resultado = [e for e in resultado if autor.lower() in e.get("autor", "").lower()]

        return sorted(resultado, key=lambda e: e.get("fecha", ""), reverse=True)

    def obtener_entrada_por_id(self, id_entrada: int) -> dict:
        for entrada in self.entradas:
            if entrada["id"] == id_entrada:
                return entrada
        return None

    def obtener_alumnos(self, escuela: str = None, grupo: str = None) -> list:
        entradas = self.obtener_entradas(escuela=escuela, grupo=grupo)
        alumnos = list(set(e["alumno"] for e in entradas))
        return sorted(alumnos)

    def obtener_grupos(self, escuela: str = None) -> list:
        entradas = self.obtener_entradas(escuela=escuela)
        grupos = list(set(e["grupo"] for e in entradas))
        return sorted(grupos)

    # ═══════════════════════════════════════════════════════════
    # MODIFICAR ENTRADAS
    # ═══════════════════════════════════════════════════════════

    def editar_entrada(self, id_entrada: int, texto: str) -> dict:
        for entrada in self.entradas:
            if entrada["id"] == id_entrada:
                entrada["texto"] = texto.strip()
                entrada["editado"] = True
                entrada["fecha_edicion"] = datetime.now().isoformat()
                self.guardar()
                return {"exito": True, "mensaje": "✅ Entrada editada correctamente.", "entrada": entrada}
        return {"exito": False, "mensaje": "Entrada no encontrada."}

    def eliminar_entrada(self, id_entrada: int) -> dict:
        for i, entrada in enumerate(self.entradas):
            if entrada["id"] == id_entrada:
                self.entradas.pop(i)
                self.guardar()
                return {"exito": True, "mensaje": "🗑️ Entrada eliminada."}
        return {"exito": False, "mensaje": "Entrada no encontrada."}

    def toggle_publico(self, id_entrada: int) -> dict:
        for entrada in self.entradas:
            if entrada["id"] == id_entrada:
                entrada["publico"] = not entrada.get("publico", False)
                self.guardar()
                estado = "pública" if entrada["publico"] else "privada"
                return {
                    "exito": True,
                    "mensaje": f"🔓 Entrada ahora es {estado}.",
                    "publico": entrada["publico"]
                }
        return {"exito": False, "mensaje": "Entrada no encontrada."}

    # ═══════════════════════════════════════════════════════════
    # ESTADÍSTICAS
    # ═══════════════════════════════════════════════════════════

    def obtener_estadisticas(self, escuela: str = None) -> dict:
        entradas = self.obtener_entradas(escuela=escuela)

        if not entradas:
            return {
                "total": 0, "observaciones": 0, "reportes": 0,
                "recomendaciones": 0, "calificaciones": 0,
                "publicas": 0, "privadas": 0,
                "alumnos_unicos": 0, "grupos_unicos": 0,
                "promedio_calificaciones": 0
            }

        calificaciones = [e["calificacion"] for e in entradas
                         if e["tipo"] == "calificacion" and e.get("calificacion") is not None]

        return {
            "total": len(entradas),
            "observaciones": len([e for e in entradas if e["tipo"] == "observacion"]),
            "reportes": len([e for e in entradas if e["tipo"] == "reporte"]),
            "recomendaciones": len([e for e in entradas if e["tipo"] == "recomendacion"]),
            "calificaciones": len(calificaciones),
            "publicas": len([e for e in entradas if e.get("publico")]),
            "privadas": len([e for e in entradas if not e.get("publico")]),
            "alumnos_unicos": len(set(e["alumno"] for e in entradas)),
            "grupos_unicos": len(set(e["grupo"] for e in entradas)),
            "promedio_calificaciones": round(sum(calificaciones) / len(calificaciones), 1) if calificaciones else 0
        }

    def obtener_historial_alumno(self, alumno: str, escuela: str = None) -> list:
        return self.obtener_entradas(escuela=escuela, alumno=alumno)


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas para Bitacora"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/bitacora.py")
    print("=" * 60)

    p = 0
    f = 0
    def t(c, d):
        nonlocal p, f
        if c:
            print(f"  ✅ {d}")
            p += 1
        else:
            print(f"  ❌ {d}")
            f += 1

    try:
        os.remove("datos/bitacora.json")
    except:
        pass

    b = Bitacora()
    t(isinstance(b, Bitacora), "Instancia creada")
    t(len(b.entradas) == 0, "Bitácora vacía al inicio")
    t(len(b.TIPOS) == 4, "4 tipos de entrada")

    # Agregar entradas
    e1 = b.agregar_entrada("observacion", "Ana López", "3A",
                           "Excelente participación en clase",
                           "María García", "ESBJ001")
    t(e1["tipo"] == "observacion", "Observación guardada")
    t(e1["alumno"] == "Ana López", "Alumno guardado")
    t(e1["autor"] == "María García", "Autor guardado")
    t(not e1["publico"], "Por defecto es privada")
    t(e1["id"] == 1, "ID autoincremental")

    e2 = b.agregar_entrada("reporte", "Carlos Ruiz", "3A",
                           "No entregó tareas en 3 ocasiones",
                           "María García", "ESBJ001", publico=True)
    t(e2["publico"], "Entrada pública guardada")

    e3 = b.agregar_entrada("calificacion", "Ana López", "3A",
                           "Examen final de álgebra",
                           "María García", "ESBJ001",
                           publico=True, calificacion=9.5)
    t(e3["calificacion"] == 9.5, "Calificación guardada")

    e4 = b.agregar_entrada("recomendacion", "Diana Martínez", "3B",
                           "Se sugiere reforzar lectura en casa",
                           "Juan Pérez", "ESBJ001", publico=True)
    t(e4["tipo"] == "recomendacion", "Recomendación guardada")

    e5 = b.agregar_entrada("observacion", "Eduardo Sánchez", "3B",
                           "Falta de atención en clase",
                           "Juan Pérez", "CMH002")

    # Total
    t(len(b.entradas) == 5, "5 entradas en total")

    # Filtrar por escuela
    t(len(b.obtener_entradas(escuela="ESBJ001")) == 4, "Filtro escuela: 4 entradas")
    t(len(b.obtener_entradas(escuela="CMH002")) == 1, "Filtro escuela: 1 entrada")

    # Filtrar por tipo
    t(len(b.obtener_entradas(tipo="observacion")) == 2, "Filtro tipo: 2 observaciones")
    t(len(b.obtener_entradas(tipo="reporte")) == 1, "Filtro tipo: 1 reporte")
    t(len(b.obtener_entradas(tipo="calificacion")) == 1, "Filtro tipo: 1 calificación")
    t(len(b.obtener_entradas(tipo="recomendacion")) == 1, "Filtro tipo: 1 recomendación")

    # Filtrar públicas
    t(len(b.obtener_entradas(solo_publicas=True)) == 3, "Filtro públicas: 3 entradas")

    # Filtrar por alumno (ANTES de editar/eliminar)
    entradas_ana = b.obtener_entradas(alumno="Ana")
    t(len(entradas_ana) >= 1, f"Filtro alumno 'Ana': {len(entradas_ana)} entradas")
    t(len(b.obtener_entradas(alumno="Carlos")) == 1, "Filtro alumno 'Carlos': 1 entrada")
    t(len(b.obtener_entradas(alumno="Diana")) == 1, "Filtro alumno 'Diana': 1 entrada")

    # Filtrar por autor
    t(len(b.obtener_entradas(autor="María")) == 3, "Filtro autor 'María': 3 entradas")
    t(len(b.obtener_entradas(autor="Juan")) == 2, "Filtro autor 'Juan': 2 entradas")

    # Filtrar por grupo
    t(len(b.obtener_entradas(grupo="3A")) == 3, "Filtro grupo '3A': 3 entradas")

    # Obtener alumnos
    alumnos = b.obtener_alumnos(escuela="ESBJ001")
    t(len(alumnos) == 3, "3 alumnos únicos en ESBJ001")
    t("Ana López" in alumnos, "Ana López en lista")

    # Obtener grupos
    grupos = b.obtener_grupos(escuela="ESBJ001")
    t(len(grupos) == 2, "2 grupos en ESBJ001")

    # Historial alumno (ANTES de eliminar)
    historial = b.obtener_historial_alumno("Ana López", "ESBJ001")
    t(len(historial) == 2, "Historial Ana: 2 entradas")

    # Obtener por ID
    entrada = b.obtener_entrada_por_id(1)
    t(entrada["alumno"] == "Ana López", "Entrada por ID encontrada")
    t(b.obtener_entrada_por_id(999) is None, "ID inexistente: None")

    # Editar
    resultado = b.editar_entrada(1, "Texto editado de prueba")
    t(resultado["exito"], "Entrada editada")
    t(b.obtener_entrada_por_id(1)["texto"] == "Texto editado de prueba", "Texto actualizado")
    t(b.obtener_entrada_por_id(1)["editado"], "Marcada como editada")

    # Editar inexistente
    resultado = b.editar_entrada(999, "No existe")
    t(not resultado["exito"], "Editar ID inexistente: False")

    # Toggle público
    resultado = b.toggle_publico(1)
    t(resultado["exito"], "Toggle público exitoso")
    t(b.obtener_entrada_por_id(1)["publico"], "Ahora es pública")

    resultado = b.toggle_publico(1)
    t(not b.obtener_entrada_por_id(1)["publico"], "Ahora es privada")

    # Eliminar
    resultado = b.eliminar_entrada(2)
    t(resultado["exito"], "Entrada eliminada")
    t(len(b.entradas) == 4, "4 entradas restantes")

    # Eliminar inexistente
    resultado = b.eliminar_entrada(999)
    t(not resultado["exito"], "Eliminar ID inexistente: False")

    # Estadísticas
    stats = b.obtener_estadisticas(escuela="ESBJ001")
    t(stats["total"] == 3, "Estadísticas total: 3")
    t(stats["observaciones"] == 1, "Estadísticas: 1 observación")
    t(stats["calificaciones"] == 1, "Estadísticas: 1 calificación")
    t(stats["recomendaciones"] == 1, "Estadísticas: 1 recomendación")
    t(stats["alumnos_unicos"] == 2, "Estadísticas: 2 alumnos únicos")
    t(stats["promedio_calificaciones"] == 9.5, "Estadísticas: promedio 9.5")

    # Persistencia
    b2 = Bitacora()
    t(len(b2.entradas) == 4, "Datos persisten tras recargar")

    # Limpiar
    try:
        os.remove("datos/bitacora.json")
    except:
        pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Bitácora validada\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()