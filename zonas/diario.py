"""
🌿 Sana - Módulo de Diario Emocional Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Registro de emociones diarias con notas personales extensas,
detección de patrones emocionales, rachas, logros, estadísticas
avanzadas y mensajes empáticos personalizados.
El adolescente puede escribir, guardar notas y hacer seguimiento
de su viaje emocional. Persistencia JSON · 100% funcional.
═══════════════════════════════════════════════════════════════
"""

import json
import os
import random
from datetime import datetime, timedelta
from collections import Counter


class Diario:
    """
    Diario emocional de Sana - El espejo del alma adolescente.
    
    Un espacio seguro donde registrar no solo emociones, sino también
    pensamientos profundos, notas personales, reflexiones y momentos
    importantes. Con seguimiento de patrones, rachas y estadísticas
    para que el usuario se conozca mejor a sí mismo.
    """

    # ═══════════════════════════════════════════════════════════
    # EMOCIONES DISPONIBLES
    # ═══════════════════════════════════════════════════════════

    EMOCIONES_BASE = [
        "😊 Feliz",
        "😢 Triste",
        "😠 Enojado/a",
        "😰 Ansioso/a",
        "😴 Cansado/a",
        "🤔 Confundido/a",
        "😌 En calma",
        "🥳 Motivado/a",
        "😞 Solitario/a",
        "😱 Asustado/a",
        "😤 Frustrado/a",
        "🤗 Agradecido/a",
        "💜 Enamorado/a",
        "😎 Seguro/a",
        "🤩 Emocionado/a",
        "😕 Inseguro/a"
    ]

    INTENSIDADES = ["Baja", "Media", "Alta", "Muy alta"]

    FACTORES = [
        "Escuela", "Familia", "Amigos", "Salud", "Sueño",
        "Redes sociales", "Deporte", "Alimentación", "Pareja",
        "Autoestima", "Futuro", "Pasatiempos", "Otro"
    ]

    # ═══════════════════════════════════════════════════════════
    # MENSAJES EMPÁTICOS
    # ═══════════════════════════════════════════════════════════

    MENSAJES_REGISTRO = [
        "📝 Gracias por registrar cómo te sientes. Cada entrada es un paso hacia conocerte mejor.",
        "💭 Has plasmado tu emoción. A veces solo ponerle nombre a lo que sentimos ya es sanador.",
        "🌟 ¡Registrado! Este diario es tu espacio seguro. Nadie más lo ve, solo tú y Sana.",
        "📔 Una entrada más en tu viaje emocional. Con el tiempo verás patrones que te ayudarán a entenderte.",
        "🖊️ Escribir sana. Literalmente. Gracias por confiar en este espacio."
    ]

    MENSAJES_RACHA = [
        "🔥 ¡{racha} días seguidos escribiendo! Eso es disciplina emocional. Sana está orgullosa de ti.",
        "⭐ ¡Racha de {racha} días! Conocerte a ti mismo/a es el mejor regalo que puedes hacerte.",
        "💪 {racha} días consecutivos. No cualquiera se toma el tiempo de mirar hacia adentro. Tú sí.",
        "🏆 ¡{racha} días! Eso es más que una racha, es un hábito. Y los hábitos cambian vidas."
    ]

    MENSAJES_VACIO = [
        "📖 Tu diario está vacío. ¿Qué tal si empiezas registrando cómo te sientes ahora mismo?",
        "🕊️ Aún no hay entradas. No hay prisa. Tu viaje emocional empieza cuando tú quieras.",
        "🌱 La primera página está en blanco, esperando tu primera emoción. ¿Te animas?",
        "✨ Este diario es como un jardín. Hoy puedes plantar la primera semilla. ¿Cómo te sientes?"
    ]

    MENSAJES_PATRON = [
        "🔍 He notado que esta semana has sentido mucho {emocion}. ¿Hay algo en particular que lo esté causando?",
        "📊 {emocion} ha sido tu emoción más frecuente. Observar patrones es el primer paso para cambiarlos.",
        "💡 Últimamente predomina {emocion}. ¿Qué crees que está influyendo en esto?",
        "🎯 Patrón detectado: {emocion}. La conciencia es poder. Ya diste el primer paso."
    ]

    MENSAJES_INTENSIDAD = [
        "📈 Tu intensidad emocional ha estado {nivel}. Recuerda respirar y tomarte pausas.",
        "⚠️ Intensidad {nivel} detectada. ¿Necesitas un ejercicio de respiración?",
        "💭 Tus emociones están a un volumen {nivel}. Está bien sentir intensamente, pero también descansar."
    ]

    def __init__(self, archivo="datos/diario.json"):
        self.archivo_diario = archivo
        self.entradas = []
        self.notas_libres = []  # Nuevo: notas libres del adolescente
        self._asegurar_directorio()
        self.cargar()

    def _asegurar_directorio(self):
        directorio = os.path.dirname(self.archivo_diario)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

    def cargar(self):
        try:
            if os.path.exists(self.archivo_diario):
                with open(self.archivo_diario, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.entradas = datos.get("entradas", [])
                    self.notas_libres = datos.get("notas_libres", [])
            else:
                self.entradas = []
                self.notas_libres = []
        except (json.JSONDecodeError, IOError):
            self.entradas = []
            self.notas_libres = []

    def guardar(self):
        self._asegurar_directorio()
        with open(self.archivo_diario, "w", encoding="utf-8") as f:
            json.dump({
                "entradas": self.entradas,
                "notas_libres": self.notas_libres,
                "ultima_actualizacion": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS BÁSICOS
    # ═══════════════════════════════════════════════════════════

    def obtener_emociones(self) -> list:
        return self.EMOCIONES_BASE

    def obtener_intensidades(self) -> list:
        return self.INTENSIDADES

    def obtener_factores(self) -> list:
        return self.FACTORES

    # ═══════════════════════════════════════════════════════════
    # ENTRADAS EMOCIONALES
    # ═══════════════════════════════════════════════════════════

    def agregar_entrada(self, emocion: str, nota: str = "",
                        intensidad: str = "Media", factores: list = None) -> dict:
        if factores is None:
            factores = []
        if intensidad not in self.INTENSIDADES:
            intensidad = "Media"

        entrada = {
            "id": self._generar_id_entrada(),
            "tipo": "emocion",
            "fecha": datetime.now().isoformat(),
            "emocion": emocion,
            "intensidad": intensidad,
            "nota": nota.strip(),
            "factores": factores
        }
        self.entradas.append(entrada)
        self.guardar()
        return entrada

    # ═══════════════════════════════════════════════════════════
    # NOTAS LIBRES (NUEVO - LO QUE PEDISTE)
    # ═══════════════════════════════════════════════════════════

    def agregar_nota_libre(self, titulo: str, contenido: str, etiquetas: list = None,
                           estado_animo: str = None) -> dict:
        """
        Agrega una nota libre al diario. El adolescente puede escribir
        lo que quiera: pensamientos, reflexiones, historias, desahogos.
        
        Args:
            titulo: Título de la nota.
            contenido: Texto completo de la nota.
            etiquetas: Etiquetas para categorizar (ej: ['escuela', 'amigos']).
            estado_animo: Estado de ánimo al escribir (opcional).
        
        Returns:
            Diccionario con la nota creada.
        """
        nota = {
            "id": self._generar_id_nota(),
            "tipo": "nota_libre",
            "fecha": datetime.now().isoformat(),
            "titulo": titulo.strip(),
            "contenido": contenido.strip(),
            "etiquetas": etiquetas or [],
            "estado_animo": estado_animo or "No especificado",
            "favorito": False
        }
        self.notas_libres.append(nota)
        self.guardar()
        return nota

    def editar_nota_libre(self, id_nota: int, **kwargs) -> bool:
        """Edita una nota libre existente."""
        for nota in self.notas_libres:
            if nota["id"] == id_nota:
                if "titulo" in kwargs:
                    nota["titulo"] = kwargs["titulo"].strip()
                if "contenido" in kwargs:
                    nota["contenido"] = kwargs["contenido"].strip()
                if "etiquetas" in kwargs:
                    nota["etiquetas"] = kwargs["etiquetas"]
                if "estado_animo" in kwargs:
                    nota["estado_animo"] = kwargs["estado_animo"]
                nota["fecha_modificacion"] = datetime.now().isoformat()
                self.guardar()
                return True
        return False

    def eliminar_nota_libre(self, id_nota: int) -> bool:
        """Elimina una nota libre."""
        for i, nota in enumerate(self.notas_libres):
            if nota["id"] == id_nota:
                self.notas_libres.pop(i)
                self.guardar()
                return True
        return False

    def marcar_favorito(self, id_nota: int) -> bool:
        """Marca/desmarca una nota como favorita."""
        for nota in self.notas_libres:
            if nota["id"] == id_nota:
                nota["favorito"] = not nota.get("favorito", False)
                self.guardar()
                return True
        return False

    def obtener_notas_libres(self, etiqueta: str = None, favoritos: bool = False,
                            busqueda: str = None) -> list:
        """
        Obtiene notas libres con filtros.
        
        Args:
            etiqueta: Filtrar por etiqueta.
            favoritos: Solo favoritas.
            busqueda: Texto a buscar en título o contenido.
        
        Returns:
            Lista de notas filtradas.
        """
        resultado = self.notas_libres.copy()
        if etiqueta:
            resultado = [n for n in resultado if etiqueta in n.get("etiquetas", [])]
        if favoritos:
            resultado = [n for n in resultado if n.get("favorito", False)]
        if busqueda:
            busqueda = busqueda.lower()
            resultado = [n for n in resultado 
                        if busqueda in n["titulo"].lower() or busqueda in n["contenido"].lower()]
        return sorted(resultado, key=lambda n: n.get("fecha", ""), reverse=True)

    def obtener_nota_por_id(self, id_nota: int) -> dict:
        """Obtiene una nota específica por ID."""
        for nota in self.notas_libres:
            if nota["id"] == id_nota:
                return nota
        return None

    def _generar_id_entrada(self) -> int:
        if not self.entradas:
            return 1
        return max(e.get("id", 0) for e in self.entradas) + 1

    def _generar_id_nota(self) -> int:
        if not self.notas_libres:
            return 1
        return max(n.get("id", 0) for n in self.notas_libres) + 1

    # ═══════════════════════════════════════════════════════════
    # CONSULTAS
    # ═══════════════════════════════════════════════════════════

    def obtener_entradas(self, dias: int = 7, tipo: str = None) -> list:
        """
        Retorna las entradas de los últimos N días.
        
        Args:
            dias: Número de días hacia atrás.
            tipo: 'emocion', 'nota_libre' o None para todas.
        """
        limite = datetime.now() - timedelta(days=dias)
        entradas_filtradas = []
        for e in self.entradas:
            try:
                if datetime.fromisoformat(e["fecha"]) >= limite:
                    if tipo is None or e.get("tipo") == tipo:
                        entradas_filtradas.append(e)
            except (ValueError, KeyError):
                pass
        return entradas_filtradas

    def emocion_predominante(self, dias: int = 7) -> str:
        recientes = self.obtener_entradas(dias, tipo="emocion")
        if not recientes:
            return "Sin datos suficientes"
        emociones = [e["emocion"] for e in recientes if e.get("tipo") == "emocion"]
        if not emociones:
            return "Sin datos suficientes"
        return Counter(emociones).most_common(1)[0][0]

    def intensidad_promedio(self, dias: int = 7) -> str:
        recientes = self.obtener_entradas(dias, tipo="emocion")
        recientes = [e for e in recientes if e.get("tipo") == "emocion"]
        if not recientes:
            return "Sin datos"
        valores = {"Baja": 1, "Media": 2, "Alta": 3, "Muy alta": 4}
        total = sum(valores.get(e.get("intensidad", "Media"), 2) for e in recientes)
        promedio = total / len(recientes)
        if promedio < 1.5: return "Baja"
        elif promedio < 2.5: return "Media"
        elif promedio < 3.5: return "Alta"
        return "Muy alta"

    def racha_actual(self) -> int:
        """Calcula la racha de días consecutivos con entradas o notas."""
        todas = list(self.entradas) + list(self.notas_libres)
        if not todas:
            return 0
        fechas = set()
        for item in todas:
            try:
                fechas.add(datetime.fromisoformat(item["fecha"]).date())
            except (ValueError, KeyError):
                pass
        hoy = datetime.now().date()
        racha = 0
        for i in range(365):
            dia = hoy - timedelta(days=i)
            if dia in fechas:
                racha += 1
            else:
                break
        return racha

    def factores_frecuentes(self, dias: int = 7) -> list:
        recientes = self.obtener_entradas(dias)
        todos_factores = []
        for entrada in recientes:
            todos_factores.extend(entrada.get("factores", []))
        return Counter(todos_factores).most_common(5)

    # ═══════════════════════════════════════════════════════════
    # ESTADÍSTICAS Y RESUMEN
    # ═══════════════════════════════════════════════════════════

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas completas del diario."""
        entradas_emocion = [e for e in self.entradas if e.get("tipo") == "emocion"]
        emociones_lista = [e["emocion"] for e in entradas_emocion]
        conteo = Counter(emociones_lista)
        
        return {
            "total_entradas_emocion": len(entradas_emocion),
            "total_notas_libres": len(self.notas_libres),
            "total_general": len(entradas_emocion) + len(self.notas_libres),
            "emocion_predominante": conteo.most_common(1)[0][0] if conteo else "Sin datos",
            "racha_actual": self.racha_actual(),
            "intensidad_promedio": self.intensidad_promedio(30),
            "emociones_distintas": len(conteo),
            "notas_favoritas": sum(1 for n in self.notas_libres if n.get("favorito")),
            "top_3_emociones": conteo.most_common(3),
            "factores_frecuentes": self.factores_frecuentes(30),
            "dias_con_registros": len(set(
                datetime.fromisoformat(e["fecha"]).date() 
                for e in self.entradas + self.notas_libres
                if "fecha" in e
            ))
        }

    def resumen_semanal(self) -> str:
        recientes = self.obtener_entradas(7)
        if not recientes:
            return random.choice(self.MENSAJES_VACIO)

        predominante = self.emocion_predominante(7)
        intensidad = self.intensidad_promedio(7)
        racha = self.racha_actual()
        total_entradas = len([e for e in recientes if e.get("tipo") == "emocion"])
        total_notas = len([e for e in recientes if e.get("tipo") == "nota_libre"])

        resumen = "📔 RESUMEN DE TU SEMANA\n"
        resumen += "─" * 35 + "\n\n"
        resumen += f"📊 Emociones registradas: {total_entradas}\n"
        resumen += f"📝 Notas escritas: {total_notas}\n"
        resumen += f"🎯 Emoción más frecuente: {predominante}\n"
        resumen += f"📈 Intensidad promedio: {intensidad}\n"
        resumen += f"🔥 Días seguidos escribiendo: {racha}\n\n"

        if racha >= 7:
            resumen += random.choice(self.MENSAJES_RACHA).format(racha=racha)
        elif racha >= 3:
            resumen += f"💛 Vas {racha} días seguidos. ¡Sigue así! Escribir sana."
        else:
            resumen += "🌱 Cada entrada cuenta. No hay prisa, esto es un viaje."

        if predominante != "Sin datos suficientes":
            resumen += "\n\n" + random.choice(self.MENSAJES_PATRON).format(emocion=predominante)

        if intensidad in ("Alta", "Muy alta"):
            resumen += "\n" + random.choice(self.MENSAJES_INTENSIDAD).format(nivel=intensidad.lower())

        return resumen

    def obtener_mensaje_registro(self) -> str:
        """Retorna un mensaje aleatorio de confirmación de registro."""
        return random.choice(self.MENSAJES_REGISTRO)

# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Diario v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/diario.py (v3.0 - Hiper-Evolución)")
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

    ARCHIVO = "datos/test_diario_evolved.json"
    try: os.remove(ARCHIVO)
    except: pass

    diario = Diario(archivo=ARCHIVO)

    # Básicos
    t(isinstance(diario, Diario), "Instancia creada")
    t(len(diario.obtener_emociones()) >= 12, f"{len(diario.obtener_emociones())} emociones")
    t(len(diario.obtener_intensidades()) == 4, "4 intensidades")
    t(len(diario.obtener_factores()) >= 10, f"{len(diario.obtener_factores())} factores")

    # Agregar entrada emocional
    entrada = diario.agregar_entrada("😊 Feliz", "Hoy fue un buen día", "Alta", ["Amigos", "Escuela"])
    t(entrada["emocion"] == "😊 Feliz", "Emoción guardada")
    t(entrada["nota"] == "Hoy fue un buen día", "Nota guardada")
    t(entrada["intensidad"] == "Alta", "Intensidad guardada")
    t("Amigos" in entrada["factores"], "Factores guardados")
    t(entrada["tipo"] == "emocion", "Tipo: emocion")

    # Valores por defecto
    e2 = diario.agregar_entrada("😢 Triste")
    t(e2["nota"] == "", "Nota vacía por defecto")
    t(e2["intensidad"] == "Media", "Intensidad Media por defecto")
    t(e2["factores"] == [], "Factores vacíos por defecto")

    # NOTAS LIBRES
    nota = diario.agregar_nota_libre("Mi día en la escuela", "Hoy tuve un examen difícil pero creo que me fue bien. "
                                      "Mis amigos me ayudaron a estudiar.", ["escuela", "amigos"], "Motivado/a")
    t(nota["titulo"] == "Mi día en la escuela", "Título guardado")
    t(len(nota["contenido"]) > 30, "Contenido guardado")
    t(nota["tipo"] == "nota_libre", "Tipo: nota_libre")
    t("escuela" in nota["etiquetas"], "Etiquetas guardadas")
    t(nota["estado_animo"] == "Motivado/a", "Estado de ánimo guardado")
    t(not nota["favorito"], "No favorito por defecto")

    # Búsqueda por texto (ANTES de editar - el contenido original tiene "examen")
    por_busqueda = diario.obtener_notas_libres(busqueda="examen")
    t(len(por_busqueda) == 1, "Búsqueda por texto 'examen' encuentra 1")

    # Editar nota
    t(diario.editar_nota_libre(1, titulo="Editado", contenido="Contenido editado"), "Nota editada")
    nota_editada = diario.obtener_nota_por_id(1)
    t(nota_editada["titulo"] == "Editado", "Título actualizado")
    t(nota_editada["contenido"] == "Contenido editado", "Contenido actualizado")

    # Favorito
    t(diario.marcar_favorito(1), "Marcado como favorito")
    t(diario.obtener_nota_por_id(1)["favorito"], "Es favorito")
    t(diario.marcar_favorito(1), "Desmarcado de favorito")
    t(not diario.obtener_nota_por_id(1)["favorito"], "Ya no es favorito")

    # Filtros
    favoritas = diario.obtener_notas_libres(favoritos=True)
    t(len(favoritas) == 0, "Filtro favoritos funciona (0 favoritas)")

    por_etiqueta = diario.obtener_notas_libres(etiqueta="escuela")
    t(len(por_etiqueta) == 1, "Filtro por etiqueta 'escuela' encuentra 1")

    # Eliminar nota
    t(diario.eliminar_nota_libre(1), "Nota eliminada correctamente")
    t(diario.obtener_nota_por_id(1) is None, "Nota ya no existe")
    t(len(diario.obtener_notas_libres(busqueda="editado")) == 0, "Búsqueda vacía tras eliminar nota")

    # Obtener entradas de emoción
    recientes = diario.obtener_entradas(7)
    t(len(recientes) == 2, "2 entradas de emoción en total")

    # Emoción predominante
    t(diario.emocion_predominante(7) in ["😊 Feliz", "😢 Triste"], "Predominante detectada")

    # Intensidad promedio
    t(diario.intensidad_promedio(7) in ["Baja", "Media", "Alta", "Muy alta"], "Intensidad válida")

    # Racha
    racha = diario.racha_actual()
    t(racha >= 1, f"Racha: {racha} día(s)")

    # Resumen semanal
    resumen = diario.resumen_semanal()
    t("RESUMEN" in resumen, "Resumen tiene título")
    t("Notas escritas" in resumen, "Resumen incluye conteo de notas")

    # Estadísticas completas
    stats = diario.obtener_estadisticas()
    t("total_entradas_emocion" in stats, "Stats: emociones")
    t("total_notas_libres" in stats, "Stats: notas libres")
    t("notas_favoritas" in stats, "Stats: favoritas")
    t("top_3_emociones" in stats, "Stats: top 3 emociones")
    t("dias_con_registros" in stats, "Stats: días con registros")

    # Mensaje de registro
    msg = diario.obtener_mensaje_registro()
    t(len(msg) > 15, "Mensaje de registro válido")

    # Diario vacío
    diario_vacio = Diario(archivo="datos/test_vacio.json")
    t(diario_vacio.emocion_predominante() == "Sin datos suficientes", "Vacío: sin datos")
    t(diario_vacio.racha_actual() == 0, "Vacío: racha 0")
    resumen_vacio = diario_vacio.resumen_semanal()
    t(len(resumen_vacio) > 20 and "error" not in resumen_vacio.lower(),
      f"Vacío: mensaje amigable ('{resumen_vacio[:40]}...')")

    # Persistencia
    diario2 = Diario(archivo=ARCHIVO)
    t(len(diario2.entradas) == 2, "Entradas persisten tras recargar")

    # Limpiar archivos de prueba
    for archivo in [ARCHIVO, "datos/test_vacio.json"]:
        try:
            os.remove(archivo)
        except:
            pass

    total = p_tests + f_tests
    print(f"\n  📊 {p_tests}/{total} tests pasados")
    if f_tests == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Diario v3.0 validado\n")
    else:
        print(f"  ⚠️  {f_tests} test(s) fallaron\n")
    return f_tests == 0


if __name__ == "__main__":
    ejecutar_tests()

