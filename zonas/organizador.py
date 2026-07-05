"""
🌿 Sana - Módulo Organizador de Tareas Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Gestión de tareas con sistema de carga mental (1-5), priorización
inteligente, rachas, logros, estadísticas y mensajes empáticos.
Diseñado para adolescentes que necesitan organizarse sin culpa.
Persistencia JSON · 100% funcional · Test integrado.
═══════════════════════════════════════════════════════════════
"""

import json
import os
import random
from datetime import datetime, timedelta
from collections import Counter


class Organizador:
    """
    Organizador de tareas empático de Sana.
    
    No es solo una lista de tareas. Es un acompañante que entiende
    que la productividad no es lineal, que hay días buenos y días malos,
    y que la salud mental es más importante que cualquier entrega.
    
    Cada tarea tiene:
    - texto, carga mental (1-5), fecha, estado
    - prioridad calculada automáticamente
    - etiquetas para categorizar
    - historial de modificaciones
    """

    # ═══════════════════════════════════════════════════════════
    # ETIQUETAS PREDEFINIDAS
    # ═══════════════════════════════════════════════════════════

    ETIQUETAS = [
        "escuela", "tarea", "examen", "proyecto", "lectura",
        "deporte", "arte", "música", "idiomas", "programación",
        "casa", "personal", "salud", "social", "otro"
    ]

    # ═══════════════════════════════════════════════════════════
    # MENSAJES EMPÁTICOS
    # ═══════════════════════════════════════════════════════════

    MENSAJES_COMPLETAR = [
        "🎉 ¡Tarea completada! Eso es un paso menos en tu mochila. Date crédito por esto.",
        "✅ ¡Fuera de la lista! Cada tarea terminada es una pequeña victoria. Celebra esto.",
        "⭐ ¡Lo lograste! Tachar algo de la lista es de las mejores sensaciones. Disfrútala.",
        "💪 ¡Completada! Mira todo lo que estás avanzando. Eres más productivo/a de lo que crees.",
        "🌟 ¡Eso es! Una tarea menos. Respira hondo. Ya está. Pasemos a lo siguiente cuando tú quieras.",
        "🏆 ¡Tarea finalizada! Tu yo del futuro te lo agradece. Sigue así, a tu ritmo.",
        "👏 ¡Bien hecho! Completar tareas es cuidar de ti mismo/a. Eso es amor propio.",
        "🎯 ¡Justo en el blanco! Tarea completada con éxito. ¿Cómo te sientes?"
    ]

    MENSAJES_CARGA_ALTA = [
        "😰 Tu carga mental está alta. ¿Has considerado dividir algunas tareas en pasos más pequeños? Eso ayuda mucho.",
        "📊 Veo que tienes varias tareas pesadas. Recuerda: no eres una máquina. Prioriza y haz una a la vez.",
        "💭 Carga mental elevada detectada. ¿Qué tal si respiras hondo y eliges SOLO UNA tarea para empezar?",
        "⚠️ Tienes mucha carga. Sana te recuerda: tu salud mental es más importante que cualquier tarea.",
        "🆘 ¿Necesitas ayuda con algo? A veces compartir la carga, aunque sea hablándolo, ya alivia.",
        "🧘 Tareas pesadas detectadas. Recuerda la técnica Pomodoro: 25 minutos de trabajo, 5 de descanso."
    ]

    MENSAJES_SIN_TAREAS = [
        "✨ ¡No tienes tareas pendientes! Disfruta este momento de libertad. Te lo mereces.",
        "🌿 Lista vacía. Qué paz. Aprovecha para hacer algo que te guste, no solo lo 'productivo'.",
        "🎈 ¡Sin tareas! Respira hondo. El mundo no se va a acabar. Date un gusto.",
        "☀️ Nada pendiente. Así da gusto. Recuerda: descansar también es importante.",
        "🌸 Lista limpia. ¿Qué tal si haces algo creativo? O simplemente... nada. Eso también vale."
    ]

    MENSAJES_PRIMERA_TAREA = [
        "📝 ¡Tu primera tarea registrada! Así empiezan los grandes hábitos. Un paso a la vez.",
        "🌱 Primera tarea en la lista. No te abrumes. Roma no se construyó en un día.",
        "🎯 ¡Empezamos! Registrar tus tareas ya es un acto de responsabilidad contigo mismo/a."
    ]

    def __init__(self, archivo="datos/tareas.json"):
        self.archivo_tareas = archivo
        self.tareas = []
        self.historial_completadas = []
        self.rachas = {"actual": 0, "mejor": 0, "ultima_fecha": None}
        self._asegurar_directorio()
        self.cargar()
        self._actualizar_rachas()

    def _asegurar_directorio(self):
        directorio = os.path.dirname(self.archivo_tareas)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

    def cargar(self):
        try:
            if os.path.exists(self.archivo_tareas):
                with open(self.archivo_tareas, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.tareas = datos.get("tareas", [])
                    self.historial_completadas = datos.get("historial_completadas", [])
                    self.rachas = datos.get("rachas", {"actual": 0, "mejor": 0, "ultima_fecha": None})
            else:
                self.tareas = []
                self.historial_completadas = []
                self.rachas = {"actual": 0, "mejor": 0, "ultima_fecha": None}
        except (json.JSONDecodeError, IOError, KeyError):
            self.tareas = []
            self.historial_completadas = []
            self.rachas = {"actual": 0, "mejor": 0, "ultima_fecha": None}

    def guardar(self):
        self._asegurar_directorio()
        with open(self.archivo_tareas, "w", encoding="utf-8") as f:
            json.dump({
                "tareas": self.tareas,
                "historial_completadas": self.historial_completadas,
                "rachas": self.rachas,
                "ultima_actualizacion": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    def _actualizar_rachas(self):
        hoy = datetime.now().date()
        if self.rachas.get("ultima_fecha"):
            ultima = datetime.fromisoformat(self.rachas["ultima_fecha"]).date()
            diferencia = (hoy - ultima).days
            if diferencia == 0:
                pass
            elif diferencia == 1:
                self.rachas["actual"] += 1
                self.rachas["mejor"] = max(self.rachas["actual"], self.rachas["mejor"])
                self.rachas["ultima_fecha"] = hoy.isoformat()
            else:
                self.rachas["actual"] = 1
                self.rachas["ultima_fecha"] = hoy.isoformat()
        elif self.historial_completadas:
            self.rachas["actual"] = 1
            self.rachas["mejor"] = max(1, self.rachas["mejor"])
            self.rachas["ultima_fecha"] = hoy.isoformat()

    def _generar_id(self) -> int:
        if not self.tareas:
            return 1
        return max(t.get("id", 0) for t in self.tareas) + 1

    def _calcular_prioridad(self, carga: int, fecha_limite: str = None) -> str:
        if fecha_limite:
            try:
                limite = datetime.fromisoformat(fecha_limite).date()
                dias_restantes = (limite - datetime.now().date()).days
                if dias_restantes <= 1: return "urgente"
                elif dias_restantes <= 3: return "alta"
                elif dias_restantes <= 7: return "media"
            except (ValueError, TypeError):
                pass
        if carga >= 5: return "alta"
        elif carga >= 4: return "media"
        return "baja"

    def agregar_tarea(self, texto: str, carga: int = 3, etiquetas: list = None,
                      fecha_limite: str = None) -> dict:
        carga = max(1, min(5, int(carga)))
        etiquetas = etiquetas or []
        etiquetas = [e for e in etiquetas if e in self.ETIQUETAS]
        tarea = {
            "id": self._generar_id(),
            "texto": texto.strip(),
            "carga": carga,
            "prioridad": self._calcular_prioridad(carga, fecha_limite),
            "etiquetas": etiquetas,
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_limite": fecha_limite,
            "completada": False,
            "fecha_completada": None,
            "dividida_en": [],
            "notas": "",
            "pomodoro_count": 0
        }
        self.tareas.append(tarea)
        self.guardar()
        return tarea

    def obtener_tareas(self, solo_pendientes: bool = False, ordenar_por: str = None,
                       etiqueta: str = None, prioridad: str = None) -> list:
        resultado = self.tareas.copy()
        if solo_pendientes:
            resultado = [t for t in resultado if not t.get("completada", False)]
        if etiqueta:
            resultado = [t for t in resultado if etiqueta in t.get("etiquetas", [])]
        if prioridad:
            resultado = [t for t in resultado if t.get("prioridad") == prioridad]
        if ordenar_por == "carga":
            resultado.sort(key=lambda t: t.get("carga", 0), reverse=True)
        elif ordenar_por == "fecha":
            resultado.sort(key=lambda t: t.get("fecha_limite") or "9999", reverse=False)
        elif ordenar_por == "prioridad":
            orden = {"urgente": 0, "alta": 1, "media": 2, "baja": 3}
            resultado.sort(key=lambda t: orden.get(t.get("prioridad", "baja"), 3))
        return resultado

    def completar_tarea(self, id_tarea: int) -> dict:
        for tarea in self.tareas:
            if tarea["id"] == id_tarea and not tarea.get("completada", False):
                tarea["completada"] = True
                tarea["fecha_completada"] = datetime.now().isoformat()
                self.historial_completadas.append({
                    "id": id_tarea,
                    "texto": tarea["texto"],
                    "fecha": tarea["fecha_completada"],
                    "carga": tarea["carga"]
                })
                self._actualizar_rachas()
                self.guardar()
                return {
                    "exito": True,
                    "mensaje": random.choice(self.MENSAJES_COMPLETAR),
                    "tarea": tarea,
                    "racha_actual": self.rachas["actual"]
                }
        return {"exito": False, "mensaje": "Tarea no encontrada o ya estaba completada.", "tarea": None}

    def descompletar_tarea(self, id_tarea: int) -> bool:
        for tarea in self.tareas:
            if tarea["id"] == id_tarea and tarea.get("completada", False):
                tarea["completada"] = False
                tarea["fecha_completada"] = None
                self.guardar()
                return True
        return False

    def eliminar_tarea(self, id_tarea: int) -> bool:
        for i, tarea in enumerate(self.tareas):
            if tarea["id"] == id_tarea:
                self.tareas.pop(i)
                self.guardar()
                return True
        return False

    def editar_tarea(self, id_tarea: int, **kwargs) -> bool:
        for tarea in self.tareas:
            if tarea["id"] == id_tarea:
                if "texto" in kwargs:
                    tarea["texto"] = kwargs["texto"].strip()
                if "carga" in kwargs:
                    tarea["carga"] = max(1, min(5, int(kwargs["carga"])))
                if "etiquetas" in kwargs:
                    tarea["etiquetas"] = [e for e in kwargs["etiquetas"] if e in self.ETIQUETAS]
                if "notas" in kwargs:
                    tarea["notas"] = kwargs["notas"].strip()
                if "fecha_limite" in kwargs:
                    tarea["fecha_limite"] = kwargs["fecha_limite"]
                    tarea["prioridad"] = self._calcular_prioridad(tarea["carga"], kwargs["fecha_limite"])
                self.guardar()
                return True
        return False

    def dividir_tarea(self, id_tarea: int, pasos: list) -> dict:
        for tarea in self.tareas:
            if tarea["id"] == id_tarea:
                tarea["dividida_en"] = pasos
                tarea["carga"] = max(1, tarea["carga"] - 1)
                tarea["prioridad"] = self._calcular_prioridad(tarea["carga"], tarea.get("fecha_limite"))
                self.guardar()
                return {
                    "exito": True,
                    "mensaje": f"✅ Tarea dividida en {len(pasos)} pasos. Carga reducida a {tarea['carga']}/5. ¡Mucho mejor!",
                    "tarea": tarea
                }
        return {"exito": False, "mensaje": "Tarea no encontrada."}

    def agregar_nota(self, id_tarea: int, nota: str) -> bool:
        for tarea in self.tareas:
            if tarea["id"] == id_tarea:
                tarea["notas"] = nota.strip()
                self.guardar()
                return True
        return False

    def incrementar_pomodoro(self, id_tarea: int) -> bool:
        for tarea in self.tareas:
            if tarea["id"] == id_tarea:
                tarea["pomodoro_count"] = tarea.get("pomodoro_count", 0) + 1
                self.guardar()
                return True
        return False

    def obtener_carga_promedio(self) -> float:
        pendientes = self.obtener_tareas(solo_pendientes=True)
        if not pendientes:
            return 0.0
        return round(sum(t["carga"] for t in pendientes) / len(pendientes), 1)

    def _completadas_hoy(self) -> int:
        hoy = datetime.now().date().isoformat()
        return sum(1 for h in self.historial_completadas if h.get("fecha", "").startswith(hoy))

    def obtener_recomendacion(self) -> str:
        promedio = self.obtener_carga_promedio()
        pendientes = len(self.obtener_tareas(solo_pendientes=True))
        completadas_hoy = self._completadas_hoy()

        if pendientes == 0:
            return random.choice(self.MENSAJES_SIN_TAREAS)

        mensaje = f"📊 Tienes {pendientes} tarea(s) pendiente(s). "
        if completadas_hoy > 0:
            mensaje += f"Hoy ya completaste {completadas_hoy}. ¡Vas bien! "
        if promedio <= 2:
            mensaje += "Carga ligera. Puedes con esto sin problema. ¿Empezamos por la más fácil?"
        elif promedio <= 3.5:
            mensaje += "Carga moderada. Te recomiendo usar la técnica Pomodoro: 25 min de trabajo, 5 de descanso."
        elif promedio <= 4.5:
            mensaje += random.choice(self.MENSAJES_CARGA_ALTA)
        else:
            mensaje += "😰 Carga muy alta. Considera:\n• Dividir tareas en micro-pasos\n• Priorizar: ¿qué es realmente urgente?\n• Pedir ayuda si la necesitas\n• Tu salud mental es primero. Siempre."
        return mensaje

    def resumen(self) -> str:
        pendientes = len(self.obtener_tareas(solo_pendientes=True))
        completadas_total = len(self.historial_completadas)
        completadas_hoy = self._completadas_hoy()
        promedio = self.obtener_carga_promedio()
        racha = self.rachas["actual"]
        mejor_racha = self.rachas["mejor"]

        resumen = "📋 RESUMEN DE TAREAS\n"
        resumen += "─" * 30 + "\n"
        resumen += f"📌 Pendientes: {pendientes}\n"
        resumen += f"✅ Completadas hoy: {completadas_hoy}\n"
        resumen += f"🏆 Total completadas: {completadas_total}\n"
        resumen += f"📊 Carga promedio: {promedio}/5\n"
        resumen += f"🔥 Racha actual: {racha} día(s)\n"
        resumen += f"⭐ Mejor racha: {mejor_racha} día(s)\n\n"
        resumen += self.obtener_recomendacion()
        return resumen

    def obtener_estadisticas(self) -> dict:
        pendientes = self.obtener_tareas(solo_pendientes=True)
        etiquetas_usadas = []
        for t in self.tareas:
            etiquetas_usadas.extend(t.get("etiquetas", []))
        return {
            "total_tareas": len(self.tareas),
            "pendientes": len(pendientes),
            "completadas_total": len(self.historial_completadas),
            "completadas_hoy": self._completadas_hoy(),
            "carga_promedio": self.obtener_carga_promedio(),
            "racha_actual": self.rachas["actual"],
            "mejor_racha": self.rachas["mejor"],
            "etiquetas_mas_usadas": Counter(etiquetas_usadas).most_common(3),
            "tarea_mas_pesada": max(self.tareas, key=lambda t: t.get("carga", 0)) if self.tareas else None,
            "pomodoros_totales": sum(t.get("pomodoro_count", 0) for t in self.tareas)
        }

    def sugerir_tarea(self) -> dict:
        pendientes = self.obtener_tareas(solo_pendientes=True, ordenar_por="prioridad")
        if not pendientes:
            return {"exito": False, "mensaje": random.choice(self.MENSAJES_SIN_TAREAS)}
        for tarea in pendientes:
            if tarea.get("prioridad") == "urgente":
                return {"exito": True, "tarea": tarea,
                       "mensaje": f"🚨 Te sugiero empezar por: '{tarea['texto']}' (¡Es urgente!)"}
        for tarea in pendientes:
            if tarea.get("dividida_en"):
                return {"exito": True, "tarea": tarea,
                       "mensaje": f"📝 Sigue con: '{tarea['texto']}' - Primer paso: {tarea['dividida_en'][0]}"}
        tarea = pendientes[0]
        return {"exito": True, "tarea": tarea,
               "mensaje": f"💡 Te sugiero: '{tarea['texto']}' (Prioridad: {tarea.get('prioridad', 'media')}, Carga: {tarea['carga']}/5)"}

    def obtener_etiquetas(self) -> list:
        return self.ETIQUETAS


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/organizador.py (v3.0 - Hiper-Evolución)")
    print("=" * 60)

    p_tests = 0
    f_tests = 0
    def t(c, d):
        nonlocal p_tests, f_tests
        if c:
            print(f"  ✅ {d}")
            p_tests += 1
        else:
            print(f"  ❌ {d}")
            f_tests += 1

    ARCHIVO = "datos/test_tareas_evolved.json"
    try:
        os.remove(ARCHIVO)
    except:
        pass

    org = Organizador(archivo=ARCHIVO)

    t(isinstance(org, Organizador), "Instancia creada")
    t(len(org.obtener_tareas()) == 0, "Lista vacía al inicio")
    t(len(org.ETIQUETAS) >= 10, f"{len(org.ETIQUETAS)} etiquetas disponibles")

    tarea = org.agregar_tarea("Estudiar matemáticas", 4, etiquetas=["escuela", "examen"])
    t(tarea["texto"] == "Estudiar matemáticas", "Texto guardado")
    t(tarea["carga"] == 4, "Carga guardada")
    t("escuela" in tarea["etiquetas"], "Etiquetas guardadas")
    t("prioridad" in tarea, "Prioridad calculada automáticamente")
    t(not tarea["completada"], "Inicia no completada")

    t2 = org.agregar_tarea("Carga inválida", 10)
    t(t2["carga"] == 5, "Carga >5 → 5")
    t3 = org.agregar_tarea("Carga negativa", -3)
    t(t3["carga"] == 1, "Carga <1 → 1")

    t(len(org.obtener_tareas()) == 3, "3 tareas totales")
    t(len(org.obtener_tareas(solo_pendientes=True)) == 3, "3 pendientes")
    t(len(org.obtener_tareas(etiqueta="escuela")) >= 1, "Filtro por etiqueta funciona")

    resultado = org.completar_tarea(1)
    t(resultado["exito"], "Tarea completada con éxito")
    t(len(resultado["mensaje"]) > 10, "Mensaje empático al completar")
    t(len(org.obtener_tareas(solo_pendientes=True)) == 2, "2 pendientes tras completar")

    t(org.descompletar_tarea(1), "Tarea reabierta")
    t(not org.tareas[0]["completada"], "Ya no está completada")
    org.completar_tarea(1)
    t(org.tareas[0]["completada"], "Completada nuevamente")

    r = org.completar_tarea(999)
    t(not r["exito"], "ID inexistente retorna exito=False")

    t(org.eliminar_tarea(2), "Tarea 2 eliminada")
    t(len(org.obtener_tareas()) == 2, "2 tareas tras eliminar")
    t(not org.eliminar_tarea(999), "Eliminar ID inválido → False")

    t(org.editar_tarea(3, texto="Texto editado", carga=2), "Tarea editada")
    t(org.tareas[1]["texto"] == "Texto editado", "Texto actualizado")
    t(org.tareas[1]["carga"] == 2, "Carga actualizada")

    resultado = org.dividir_tarea(3, ["Paso 1", "Paso 2", "Paso 3"])
    t(resultado["exito"], "Tarea dividida")
    t("dividida_en" in org.tareas[1], "Campo dividida_en existe")
    t(org.tareas[1]["carga"] == 1, "Carga reducida tras dividir")

    t(org.agregar_nota(3, "Nota de prueba"), "Nota agregada")
    t(org.tareas[1]["notas"] == "Nota de prueba", "Nota guardada")

    t(org.incrementar_pomodoro(3), "Pomodoro incrementado")
    t(org.tareas[1]["pomodoro_count"] == 1, "Contador en 1")

    t(org.obtener_carga_promedio() >= 0, "Carga promedio calculada")

    rec = org.obtener_recomendacion()
    t(len(rec) > 20, "Recomendación sustancial")

    resumen = org.resumen()
    t("RESUMEN" in resumen, "Resumen tiene título")
    t("Racha" in resumen, "Resumen incluye racha")

    stats = org.obtener_estadisticas()
    t("total_tareas" in stats, "Estadísticas: total")
    t("pomodoros_totales" in stats, "Estadísticas: pomodoros")

    sugerencia = org.sugerir_tarea()
    t(sugerencia["exito"], "Sugerencia de tarea exitosa")

    org2 = Organizador(archivo="datos/test_vacio.json")
    sug = org2.sugerir_tarea()
    t(not sug["exito"], "Sin tareas → sugerencia exito=False")

    org3 = Organizador(archivo=ARCHIVO)
    t(len(org3.tareas) == 2, "Datos persisten tras recargar")

    for archivo in [ARCHIVO, "datos/test_vacio.json"]:
        try:
            os.remove(archivo)
        except:
            pass

    total = p_tests + f_tests
    print(f"\n  📊 {p_tests}/{total} tests pasados")
    if f_tests == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Organizador v3.0 validado\n")
    else:
        print(f"  ⚠️  {f_tests} test(s) fallaron\n")
    return f_tests == 0


if __name__ == "__main__":
    ejecutar_tests()