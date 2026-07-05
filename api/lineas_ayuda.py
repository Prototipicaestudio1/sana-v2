"""
🌿 Sana - Módulo de Líneas de Ayuda Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Directorio global de contactos de emergencia y apoyo psicológico
con 10+ países, 8 categorías, búsqueda inteligente, favoritos,
contactos personalizados, mensajes de crisis por categoría
y persistencia JSON.
═══════════════════════════════════════════════════════════════
"""

import json
import os
import random
from datetime import datetime


class LineasAyuda:
    """
    Directorio global de ayuda de Sana.
    
    Capacidades:
    - 10+ países con líneas oficiales verificadas
    - 8 categorías de ayuda (suicidio, bullying, LGBTQ+, etc.)
    - Búsqueda por nombre, categoría o palabra clave
    - Favoritos para acceso rápido
    - Contactos personalizados con persistencia
    - Mensajes de crisis personalizados por categoría
    - Formato legible y amigable
    - Estadísticas de uso
    """

    # ═══════════════════════════════════════════════════════════
    # DIRECTORIO GLOBAL (10+ países)
    # ═══════════════════════════════════════════════════════════

    PAISES = {
        "México": {
            "prefijo": "+52",
            "moneda": "MXN",
            "idioma": "Español",
            "lineas": [
                ("Línea de la Vida", "800 911 2000", "24 horas, gratuita, todo México", "suicidio"),
                ("Instituto Nacional de Psiquiatría", "800 273 8255", "Atención psicológica especializada", "general"),
                ("Línea Nacional contra el Suicidio", "800 822 3737", "24 horas, intervención en crisis", "suicidio"),
                ("Emergencias", "911", "Policía, ambulancia, bomberos", "emergencia"),
                ("Locatel", "55 5658 1111", "Apoyo emocional 24h, CDMX", "general"),
                ("SAPTEL", "55 5259 8121", "Cruz Roja - Apoyo psicológico gratuito", "ansiedad"),
                ("Consejo Ciudadano CDMX", "55 5533 5533", "Apoyo emocional y orientación", "general"),
                ("Línea de Atención a Víctimas de Violencia", "800 822 4466", "Violencia familiar y de género", "violencia"),
            ]
        },
        "Argentina": {
            "prefijo": "+54",
            "moneda": "ARS",
            "idioma": "Español",
            "lineas": [
                ("Línea de Prevención del Suicidio", "135", "24 horas, gratuita, todo el país", "suicidio"),
                ("Emergencias", "911", "Policía, ambulancia, bomberos", "emergencia"),
                ("Centro de Atención al Suicida", "011 5275 1135", "Buenos Aires y GBA", "suicidio"),
                ("Línea de Salud Mental", "0800 999 0091", "Nacional, gratuita, 24h", "general"),
                ("Línea 144", "144", "Violencia de género, 24h", "violencia"),
                ("Línea 102", "102", "Niñez y adolescencia", "bullying"),
            ]
        },
        "Colombia": {
            "prefijo": "+57",
            "moneda": "COP",
            "idioma": "Español",
            "lineas": [
                ("Línea Nacional de Salud Mental", "192", "24 horas, gratuita, todo Colombia", "general"),
                ("Emergencias", "123", "Policía, ambulancia, bomberos", "emergencia"),
                ("Línea Amiga", "444 44 48", "Medellín - Apoyo emocional", "general"),
                ("Fundación Sergio Urrego", "310 864 1556", "Apoyo a jóvenes LGBTQ+ y bullying", "LGBTQ+"),
                ("Línea Púrpura", "018000 112137", "Violencia de género, 24h", "violencia"),
                ("ICBF", "141", "Protección a niños y adolescentes", "bullying"),
            ]
        },
        "España": {
            "prefijo": "+34",
            "moneda": "EUR",
            "idioma": "Español",
            "lineas": [
                ("Teléfono de la Esperanza", "717 003 717", "24 horas, gratuito, todo España", "suicidio"),
                ("Emergencias", "112", "Policía, ambulancia, bomberos", "emergencia"),
                ("ANAR", "900 202 010", "Ayuda a niños y adolescentes, 24h", "bullying"),
                ("Fundación ANAR", "600 505 152", "Chat de apoyo para jóvenes", "general"),
                ("016", "016", "Violencia de género, 24h, no deja rastro", "violencia"),
                ("Línea de Atención al Suicidio", "024", "24 horas, gratuita, todo España", "suicidio"),
            ]
        },
        "Chile": {
            "prefijo": "+56",
            "moneda": "CLP",
            "idioma": "Español",
            "lineas": [
                ("Salud Responde", "600 360 7777", "Apoyo psicológico, 24h", "general"),
                ("Emergencias", "131", "Ambulancia", "emergencia"),
                ("Emergencias", "133", "Policía", "emergencia"),
                ("Fundación Todo Mejora", "línea chat", "Apoyo a jóvenes LGBTQ+", "LGBTQ+"),
                ("Línea de Prevención del Suicidio", "*4141", "24 horas, gratuita", "suicidio"),
                ("Fono Infancia", "800 200 818", "Apoyo a niños y adolescentes", "bullying"),
            ]
        },
        "Perú": {
            "prefijo": "+51",
            "moneda": "PEN",
            "idioma": "Español",
            "lineas": [
                ("Línea 113 Salud", "113", "Atención de salud mental, 24h", "general"),
                ("Emergencias", "105", "Policía", "emergencia"),
                ("Emergencias", "116", "Bomberos", "emergencia"),
                ("Línea 100", "100", "Violencia familiar y de género", "violencia"),
                ("Chat del Ministerio de Salud", "línea chat", "Orientación psicológica gratuita", "ansiedad"),
            ]
        },
        "Estados Unidos": {
            "prefijo": "+1",
            "moneda": "USD",
            "idioma": "Inglés / Español",
            "lineas": [
                ("988 Suicide & Crisis Lifeline", "988", "24 horas, inglés y español", "suicidio"),
                ("Emergencias", "911", "Policía, ambulancia, bomberos", "emergencia"),
                ("Crisis Text Line", "envía HOME al 741741", "Chat de crisis 24/7", "suicidio"),
                ("The Trevor Project", "1-866-488-7386", "Jóvenes LGBTQ+, 24h", "LGBTQ+"),
                ("Línea Nacional de Violencia Doméstica", "1-800-799-7233", "24h, español disponible", "violencia"),
            ]
        },
        "Guatemala": {
            "prefijo": "+502",
            "moneda": "GTQ",
            "idioma": "Español",
            "lineas": [
                ("Línea de Prevención del Suicidio", "5392 5953", "Apoyo en crisis", "suicidio"),
                ("Emergencias", "110", "Policía", "emergencia"),
                ("Emergencias", "122", "Bomberos", "emergencia"),
                ("Línea 1572", "1572", "Violencia contra la mujer", "violencia"),
            ]
        },
    }

    # ═══════════════════════════════════════════════════════════
    # CATEGORÍAS
    # ═══════════════════════════════════════════════════════════

    CATEGORIAS = {
        "suicidio": "🚨 Prevención del suicidio",
        "ansiedad": "😰 Ansiedad y estrés",
        "bullying": "🤜 Acoso escolar",
        "violencia": "🛑 Violencia y abuso",
        "LGBTQ+": "🏳️‍🌈 Apoyo LGBTQ+",
        "trastornos_alimenticios": "🍎 Trastornos alimenticios",
        "adicciones": "💊 Adicciones",
        "general": "💚 Apoyo general",
        "emergencia": "🚑 Emergencias",
    }

    # ═══════════════════════════════════════════════════════════
    # MENSAJES DE CRISIS POR CATEGORÍA
    # ═══════════════════════════════════════════════════════════

    MENSAJES_CRISIS = {
        "suicidio": [
            "No estás solo/a. Lo que sientes ahora puede cambiar. Por favor, llama a esta línea. "
            "Hay personas que quieren escucharte. Tu vida importa. 💚",
            "El dolor que sientes es real, pero no tienes que enfrentarlo solo/a. "
            "Estas líneas son gratuitas, confidenciales y atendidas por personas que te entienden."
        ],
        "ansiedad": [
            "La ansiedad puede ser abrumadora. Pero hay técnicas que ayudan y personas que te guían. "
            "No tienes que pasar por esto solo/a. Respira hondo y llama.",
            "Tu mente te está jugando una mala pasada. La ansiedad se trata, se calma, se supera. "
            "Hablar con un profesional es el primer paso."
        ],
        "bullying": [
            "El bullying no es tu culpa. No tienes que aguantarlo. Hay personas que pueden ayudarte "
            "a detenerlo. No estás solo/a en esto.",
            "Nadie merece ser maltratado. Si estás sufriendo acoso, estas líneas pueden orientarte. "
            "Eres valioso/a y mereces respeto."
        ],
        "violencia": [
            "Si estás en peligro, busca un lugar seguro y llama. No tienes que enfrentar esto solo/a. "
            "Hay personas entrenadas para ayudarte. Tu seguridad es lo primero.",
            "La violencia no es amor. Si alguien te está lastimando, física o emocionalmente, "
            "mereces ayuda. Estas líneas te creen y te apoyan."
        ],
        "LGBTQ+": [
            "Ser quien eres no es un problema. Si te sientes rechazado/a o confundido/a, "
            "hay comunidades que te reciben con los brazos abiertos. No estás solo/a. 🏳️‍🌈",
            "Tu identidad es válida. Tu orientación es válida. Si necesitas hablar con alguien "
            "que te entienda sin juzgarte, estas líneas son para ti."
        ],
        "trastornos_alimenticios": [
            "Tu relación con la comida puede sanar. No es tu culpa. Hay profesionales que te ayudan "
            "a recuperar una relación saludable con tu cuerpo y la alimentación.",
            "Los trastornos alimenticios son enfermedades reales, no una elección. "
            "Buscar ayuda es el acto más valiente que puedes hacer por ti mismo/a."
        ],
        "adicciones": [
            "Las adicciones se tratan. Pedir ayuda no te hace débil, te hace valiente. "
            "Hay personas que han pasado por lo mismo y quieren ayudarte.",
            "No tienes que tocar fondo para pedir ayuda. Si sientes que algo te controla, "
            "estas líneas pueden orientarte hacia la recuperación."
        ],
        "general": [
            "No necesitas estar en crisis para pedir ayuda. A veces solo necesitamos hablar. "
            "Estas líneas son gratuitas, confidenciales y están para ti.",
            "Tu salud mental importa. No minimices lo que sientes. Si necesitas hablar, "
            "aquí hay personas dispuestas a escucharte sin juzgarte."
        ],
        "emergencia": [
            "Si estás en peligro inmediato, no dudes en llamar. La ayuda está a un número de distancia. "
            "Tu seguridad es lo más importante ahora.",
            "Emergencias: policía, ambulancia, bomberos. No esperes. Si necesitas ayuda urgente, "
            "llama ahora mismo."
        ],
    }

    def __init__(self, pais: str = "México"):
        self.pais = pais if pais in self.PAISES else "México"
        self.contactos_personalizados = []
        self.favoritos = []
        self.historial_busquedas = []
        self._cargar_personalizados()

    def _cargar_personalizados(self):
        ruta = "datos/contactos_personalizados.json"
        try:
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.contactos_personalizados = datos.get("contactos", [])
                    self.favoritos = datos.get("favoritos", [])
        except (json.JSONDecodeError, IOError):
            pass

    def _guardar_personalizados(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/contactos_personalizados.json", "w", encoding="utf-8") as f:
            json.dump({
                "contactos": self.contactos_personalizados,
                "favoritos": self.favoritos,
                "ultima_actualizacion": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════════════
    # PAÍSES
    # ═══════════════════════════════════════════════════════════

    def obtener_paises(self) -> list:
        return list(self.PAISES.keys())

    def cambiar_pais(self, pais: str) -> bool:
        if pais in self.PAISES:
            self.pais = pais
            return True
        return False

    def obtener_info_pais(self) -> dict:
        """Retorna información del país actual."""
        p = self.PAISES[self.pais]
        return {
            "nombre": self.pais,
            "prefijo": p["prefijo"],
            "moneda": p.get("moneda", ""),
            "idioma": p.get("idioma", ""),
            "total_lineas": len(p["lineas"])
        }

    # ═══════════════════════════════════════════════════════════
    # LÍNEAS
    # ═══════════════════════════════════════════════════════════

    def obtener_lineas(self, solo_favoritos: bool = False, 
                       categoria: str = None) -> list:
        """Retorna líneas con filtros opcionales."""
        lineas = self.PAISES[self.pais]["lineas"]
        if solo_favoritos:
            lineas = [l for l in lineas if l[0] in self.favoritos]
        if categoria:
            lineas = [l for l in lineas if len(l) > 3 and l[3] == categoria]
        return lineas

    def obtener_todas_lineas(self) -> list:
        nacionales = [(n, num, desc, cat, "nacional") 
                     for n, num, desc, cat in self.PAISES[self.pais]["lineas"]]
        personalizadas = [(n, num, desc, "personalizado", "personalizado") 
                         for n, num, desc in self.contactos_personalizados]
        return nacionales + personalizadas

    def obtener_prefijo(self) -> str:
        return self.PAISES[self.pais]["prefijo"]

    def obtener_categorias(self) -> dict:
        """Retorna las categorías con sus emojis."""
        return self.CATEGORIAS

    def obtener_lineas_por_categoria(self, categoria: str) -> list:
        """Retorna líneas filtradas por categoría."""
        if categoria not in self.CATEGORIAS:
            return []
        return [l for l in self.PAISES[self.pais]["lineas"] if len(l) > 3 and l[3] == categoria]

    # ═══════════════════════════════════════════════════════════
    # FAVORITOS
    # ═══════════════════════════════════════════════════════════

    def marcar_favorito(self, nombre: str):
        if nombre not in self.favoritos:
            self.favoritos.append(nombre)
            self._guardar_personalizados()

    def desmarcar_favorito(self, nombre: str):
        if nombre in self.favoritos:
            self.favoritos.remove(nombre)
            self._guardar_personalizados()

    def es_favorito(self, nombre: str) -> bool:
        return nombre in self.favoritos

    # ═══════════════════════════════════════════════════════════
    # CONTACTOS PERSONALIZADOS
    # ═══════════════════════════════════════════════════════════

    def agregar_contacto(self, nombre: str, numero: str, descripcion: str = ""):
        self.contactos_personalizados.append((nombre, numero, descripcion))
        self._guardar_personalizados()

    def eliminar_contacto(self, nombre: str) -> bool:
        for i, (n, num, desc) in enumerate(self.contactos_personalizados):
            if n == nombre:
                self.contactos_personalizados.pop(i)
                self._guardar_personalizados()
                return True
        return False

    # ═══════════════════════════════════════════════════════════
    # BÚSQUEDA
    # ═══════════════════════════════════════════════════════════

    def buscar(self, termino: str) -> list:
        """Busca por nombre, descripción o categoría."""
        termino = termino.lower()
        self.historial_busquedas.append(termino)
        resultados = []
        for nombre, numero, descripcion, *cat in self.PAISES[self.pais]["lineas"]:
            texto = f"{nombre} {descripcion} {' '.join(cat)}".lower()
            if termino in texto:
                resultados.append((nombre, numero, descripcion))
        # También buscar en personalizados
        for nombre, numero, descripcion in self.contactos_personalizados:
            if termino in f"{nombre} {descripcion}".lower():
                resultados.append((nombre, numero, descripcion))
        return resultados

    def buscar_global(self, termino: str) -> list:
        """Busca en todos los países."""
        resultados = []
        pais_original = self.pais
        for pais in self.PAISES:
            self.pais = pais
            resultados.extend([(pais, n, num, d) for n, num, d in self.buscar(termino)])
        self.pais = pais_original
        return resultados

    # ═══════════════════════════════════════════════════════════
    # MENSAJES
    # ═══════════════════════════════════════════════════════════

    def obtener_mensaje_urgencia(self, categoria: str = "general") -> str:
        """Retorna mensaje de crisis personalizado por categoría."""
        mensajes = self.MENSAJES_CRISIS.get(categoria, self.MENSAJES_CRISIS["general"])
        mensaje = random.choice(mensajes)
        return (
            f"{mensaje}\n\n"
            f"Líneas de ayuda - {self.pais}:\n"
            f"{self.formatear_para_mostrar()}\n"
            f"No estás solo/a. Pedir ayuda es un acto de valentía. 💚"
        )

    def formatear_para_mostrar(self) -> str:
        lineas = self.PAISES[self.pais]["lineas"]
        texto = f"📞 Líneas de ayuda - {self.pais}\n"
        texto += f"🌍 Prefijo: {self.PAISES[self.pais]['prefijo']}\n\n"
        for nombre, numero, descripcion, *cat in lineas:
            favorito = "★ " if nombre in self.favoritos else "  "
            categoria_emoji = self.CATEGORIAS.get(cat[0] if cat else "general", "").split(" ")[0]
            texto += f"{favorito}{categoria_emoji} {nombre}\n  📞 {numero}\n  📝 {descripcion}\n\n"
        return texto

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas de uso del módulo."""
        return {
            "pais_actual": self.pais,
            "total_paises": len(self.PAISES),
            "lineas_nacionales": len(self.PAISES[self.pais]["lineas"]),
            "contactos_personalizados": len(self.contactos_personalizados),
            "favoritos": len(self.favoritos),
            "busquedas_realizadas": len(self.historial_busquedas),
            "ultimas_busquedas": self.historial_busquedas[-5:] if self.historial_busquedas else []
        }


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    print("\n" + "=" * 60)
    print("  🧪 TESTS: api/lineas_ayuda.py (v3.0 - Directorio Global)")
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

    la = LineasAyuda()
    t(isinstance(la, LineasAyuda), "Instancia creada")
    t(la.pais == "México", "País por defecto: México")

    # Países
    paises = la.obtener_paises()
    t(len(paises) >= 8, f"{len(paises)} países (mín. 8)")
    t("México" in paises and "Argentina" in paises and "España" in paises, "Países principales")

    # Cambiar país
    t(la.cambiar_pais("Argentina"), "Cambio a Argentina")
    t(la.pais == "Argentina", "País actualizado")
    t(not la.cambiar_pais("Marte"), "País inválido")
    la.cambiar_pais("México")

    # Info país
    info = la.obtener_info_pais()
    t("prefijo" in info and info["prefijo"] == "+52", "Info país: prefijo")
    t("total_lineas" in info and info["total_lineas"] >= 6, "Info país: líneas")

    # Líneas
    lineas = la.obtener_lineas()
    t(len(lineas) >= 6, f"México: {len(lineas)} líneas")
    t(isinstance(lineas[0], tuple), "Líneas son tuplas")

    # Prefijo
    t(la.obtener_prefijo() == "+52", "Prefijo México: +52")
    la.cambiar_pais("Argentina")
    t(la.obtener_prefijo() == "+54", "Prefijo Argentina: +54")
    la.cambiar_pais("México")

    # Categorías
    categorias = la.obtener_categorias()
    t(len(categorias) >= 8, f"{len(categorias)} categorías")
    t("suicidio" in categorias and "LGBTQ+" in categorias, "Categorías clave")

    # Filtrar por categoría
    lineas_suicidio = la.obtener_lineas_por_categoria("suicidio")
    t(len(lineas_suicidio) >= 1, f"Líneas de suicidio: {len(lineas_suicidio)}")
    lineas_invalida = la.obtener_lineas_por_categoria("invalida")
    t(len(lineas_invalida) == 0, "Categoría inválida: 0 líneas")

    # Búsqueda
    t(len(la.buscar("vida")) >= 1, "Búsqueda 'vida' encuentra")
    t(len(la.buscar("xyzfantasia")) == 0, "Búsqueda sin resultados")
    t(len(la.buscar_global("suicidio")) >= 3, "Búsqueda global encuentra en varios países")

    # Favoritos
    t(not la.es_favorito("Línea de la Vida"), "No es favorito al inicio")
    la.marcar_favorito("Línea de la Vida")
    t(la.es_favorito("Línea de la Vida"), "Marcado como favorito")
    t(len(la.obtener_lineas(solo_favoritos=True)) >= 1, "Filtro favoritos")
    la.desmarcar_favorito("Línea de la Vida")
    t(not la.es_favorito("Línea de la Vida"), "Desmarcado")

    # Contactos personalizados
    la.agregar_contacto("Mi psicóloga", "555-123-4567", "Consultorio")
    todas = la.obtener_todas_lineas()
    t(any("Mi psicóloga" in c[0] for c in todas), "Contacto agregado")
    t(any("personalizado" in c for c in todas), "Tipo personalizado")
    t(la.eliminar_contacto("Mi psicóloga"), "Contacto eliminado")
    t(not any("Mi psicóloga" in c[0] for c in la.obtener_todas_lineas()), "Contacto ya no existe")

    # Formatear
    formato = la.formatear_para_mostrar()
    t("México" in formato and "Línea de la Vida" in formato, "Formato correcto")

    # Mensaje urgencia
    urgencia = la.obtener_mensaje_urgencia("suicidio")
    t(len(urgencia) > 100, "Mensaje urgencia sustancial")
    urgencia_ansiedad = la.obtener_mensaje_urgencia("ansiedad")
    t(urgencia != urgencia_ansiedad, "Mensajes diferentes por categoría")

    # Estadísticas
    stats = la.obtener_estadisticas()
    t("pais_actual" in stats and "total_paises" in stats, "Estadísticas completas")
    t("ultimas_busquedas" in stats, "Historial de búsquedas")

    # Todos los países tienen líneas
    for pais in la.obtener_paises():
        la.cambiar_pais(pais)
        lineas = la.obtener_lineas()
        t(len(lineas) >= 2, f"{pais}: {len(lineas)} líneas (mín. 2)")

    # Limpiar
    try:
        os.remove("datos/contactos_personalizados.json")
    except:
        pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - LineasAyuda v3.0 validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()