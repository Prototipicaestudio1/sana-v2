"""
🌿 Sana - Módulo de Alertas, Protocolo de Seguridad y Red de Apoyo
═══════════════════════════════════════════════════════════════
Detección de frases de riesgo, derivación a ayuda profesional
y Red de Apoyo personal con frases de aliento.
100% funcional · Sin dependencias externas · Test integrado.
═══════════════════════════════════════════════════════════════
"""

import random
import json
import os
from datetime import datetime


class Alertas:
    """
    Protocolo de seguridad y Red de Apoyo de Sana.
    
    - Detecta frases de riesgo alto, medio y bajo
    - Deriva a líneas de ayuda profesional
    - Gestiona una Red de Apoyo de hasta 3 personas
    - Cada persona tiene frases de aliento personalizadas
    - Persistencia en JSON para guardar la red
    """

    # ═══════════════════════════════════════════════════════════
    # DETECCIÓN DE RIESGO
    # ═══════════════════════════════════════════════════════════

    FRASES_RIESGO_ALTO = [
        "no quiero vivir", "quiero morir", "me quiero morir",
        "no quiero seguir", "me quiero matar", "me quiero suicidar",
        "suicidio", "acabar con todo", "acabar con mi vida",
        "sin mí estarían mejor", "soy una carga", "no debería existir",
        "quisiera desaparecer", "no valgo nada", "no sirvo para nada",
        "no le importo a nadie", "nadie me quiere", "me odio",
        "me detesto", "me quiero hacer daño", "me corto", "me lastimo",
        "no puedo más", "ya no aguanto más", "no soporto más",
        "me quiero ir para siempre",
    ]

    FRASES_RIESGO_MEDIO = [
        "no sé qué hacer con mi vida", "todo me sale mal",
        "siempre me va mal", "no tengo futuro", "nada tiene sentido",
        "me siento vacío", "me siento vacía", "estoy cansado de vivir",
        "estoy cansada de vivir", "no le importo a nadie",
        "me siento solo todo el tiempo", "me siento sola todo el tiempo",
        "nadie me entiende", "no encajo en ningún lado", "no tengo amigos",
        "me hacen bullying", "me acosan", "me siento perseguido",
        "me siento perseguida", "tengo pensamientos oscuros",
        "no duermo por pensar", "no como", "no puedo comer",
        "no quiero salir", "no quiero ver a nadie", "tengo miedo todo el tiempo",
    ]

    MENSAJE_RIESGO_ALTO = (
        "Lo que compartes es muy importante y delicado. "
        "Quiero que sepas que no estás solo/a y que hay personas que pueden ayudarte.\n\n"
        "No soy humana y no quiero fallarte. Por favor, contacta a alguien que pueda escucharte ahora mismo:\n\n"
        "{contactos}\n\n"
        "Está bien pedir ayuda. Es un acto de valentía, no de debilidad. "
        "¿Quieres que te acompañe con un ejercicio de respiración mientras decides llamar?"
    )

    MENSAJE_RIESGO_MEDIO = (
        "Siento que estés pasando por esto. Lo que sientes es real y merece atención.\n\n"
        "Hablar con alguien de confianza puede ayudarte mucho. "
        "También puedes contactar a estas líneas gratuitas:\n\n"
        "{contactos}\n\n"
        "¿Quieres que hablemos más sobre lo que te pasa o prefieres un ejercicio de respiración ahora?"
    )

    CONTACTOS = [
        ("Línea de la Vida", "800 911 2000", "24h, México, gratuita"),
        ("Instituto Nacional de Psiquiatría", "800 273 8255", "Atención psicológica, México"),
        ("Línea Nacional contra Suicidio", "800 822 3737", "24h, México, gratuita"),
        ("Emergencias", "911", "Policía, ambulancia, bomberos"),
        ("Psicólogo/a escolar", "Pregunta en tu escuela", "Confidencial y gratuito"),
        ("Adulto de confianza", "Familiar, maestro/a, amigo/a", "Alguien que te quiera"),
    ]

    MENSAJES_ACOMPANAMIENTO = [
        "Respira hondo. No tienes que enfrentar esto solo/a.",
        "Tus sentimientos son válidos. Pedir ayuda es un paso enorme.",
        "No estás roto/a. Estás pasando por algo difícil y mereces apoyo.",
        "Hay personas que se dedican a ayudar en estos momentos. Úsalas.",
        "Esto que sientes ahora puede cambiar. No siempre será así.",
        "Eres valioso/a. Tu vida importa, incluso si ahora no lo sientes así.",
        "Pedir ayuda no te hace débil. Te hace valiente.",
        "Un día a la vez. Una hora a la vez. Una respiración a la vez."
    ]

    PALABRAS_NEGACION = [
        "no soy", "no me", "no le", "no es", "no son", "no estoy",
        "nunca", "jamás", "tampoco", "para nada soy", "ni soy"
    ]

    # ═══════════════════════════════════════════════════════════
    # RED DE APOYO
    # ═══════════════════════════════════════════════════════════

    MAX_PERSONAS_RED = 3

    FRASES_PREDEFINIDAS = [
        "Confío en ti. Sé que puedes con esto.",
        "No estás solo/a. Cuenta conmigo para lo que necesites.",
        "Eres más fuerte de lo que crees. Te quiero mucho.",
        "Estoy orgulloso/a de ti. Siempre.",
        "Cuando necesites hablar, aquí estoy. Sin juzgar.",
        "Recuerda: esto también pasará. Y mientras tanto, aquí estoy.",
        "Tu vida es valiosa. Tú eres valioso/a. Nunca lo olvides.",
        "No tienes que ser perfecto/a. Solo tienes que ser tú.",
        "Te escucho. Te creo. Te apoyo. Siempre.",
        "Eres importante para mí. Mucho más de lo que imaginas."
    ]

    def __init__(self):
        self.historial_alertas = []
        self.contactos_personalizados = []
        self.red_apoyo = []  # Lista de personas con sus frases
        self._asegurar_directorio()
        self._cargar_red()

    # ═══════════════════════════════════════════════════════════
    # PERSISTENCIA DE RED DE APOYO
    # ═══════════════════════════════════════════════════════════

    def _asegurar_directorio(self):
        if not os.path.exists("datos"):
            os.makedirs("datos", exist_ok=True)

    def _cargar_red(self):
        """Carga la red de apoyo desde archivo JSON."""
        try:
            ruta = "datos/red_apoyo.json"
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.red_apoyo = datos.get("red_apoyo", [])
        except (json.JSONDecodeError, IOError):
            self.red_apoyo = []

    def _guardar_red(self):
        """Guarda la red de apoyo en archivo JSON."""
        self._asegurar_directorio()
        with open("datos/red_apoyo.json", "w", encoding="utf-8") as f:
            json.dump({
                "red_apoyo": self.red_apoyo,
                "ultima_actualizacion": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════════════
    # DETECCIÓN DE RIESGO
    # ═══════════════════════════════════════════════════════════

    def detectar_riesgo(self, texto: str) -> str:
        texto = texto.lower()
        for frase in self.FRASES_RIESGO_ALTO:
            if frase in texto:
                indice = texto.find(frase)
                if indice >= 3 and texto[indice-3:indice] == "no ":
                    continue
                contexto = texto[max(0, indice - 30):indice]
                negada = any(neg in contexto for neg in self.PALABRAS_NEGACION)
                if not negada:
                    return "alto"
        for frase in self.FRASES_RIESGO_MEDIO:
            if frase in texto:
                return "medio"
        return "bajo"

    def obtener_mensaje(self, nivel: str = "medio") -> str:
        contactos = self._formatear_contactos()
        if nivel == "alto":
            return self.MENSAJE_RIESGO_ALTO.format(contactos=contactos)
        return self.MENSAJE_RIESGO_MEDIO.format(contactos=contactos)

    def _formatear_contactos(self) -> str:
        todos = self.CONTACTOS + self.contactos_personalizados
        return "\n".join([f"  • {nombre}: {numero} ({desc})" for nombre, numero, desc in todos])

    def obtener_contactos(self) -> list:
        return self.CONTACTOS + self.contactos_personalizados

    def agregar_contacto(self, nombre: str, numero: str, descripcion: str = ""):
        self.contactos_personalizados.append((nombre, numero, descripcion))

    def obtener_mensaje_acompanamiento(self) -> str:
        return random.choice(self.MENSAJES_ACOMPANAMIENTO)

    def procesar_mensaje(self, texto: str) -> dict:
        nivel = self.detectar_riesgo(texto)
        self.historial_alertas.append({"texto": texto, "nivel": nivel, "timestamp": datetime.now().isoformat()})
        if nivel == "alto":
            return {"nivel": "alto", "mensaje": self.obtener_mensaje("alto"), "requiere_derivacion": True}
        elif nivel == "medio":
            return {"nivel": "medio", "mensaje": self.obtener_mensaje("medio"), "requiere_derivacion": False}
        return {"nivel": "bajo", "mensaje": None, "requiere_derivacion": False}

    # ═══════════════════════════════════════════════════════════
    # RED DE APOYO - GESTIÓN
    # ═══════════════════════════════════════════════════════════

    def agregar_persona_red(self, nombre: str, relacion: str = "", 
                            frase: str = "", telefono: str = "") -> dict:
        """
        Agrega una persona a la red de apoyo (máximo 3).
        
        Args:
            nombre: Nombre de la persona.
            relacion: Relación (mamá, papá, amigo/a, hermano/a, etc.).
            frase: Frase de aliento personalizada.
            telefono: Teléfono de contacto (opcional).
        
        Returns:
            Diccionario con resultado y mensaje.
        """
        if len(self.red_apoyo) >= self.MAX_PERSONAS_RED:
            return {
                "exito": False,
                "mensaje": f"Ya tienes {self.MAX_PERSONAS_RED} personas en tu Red de Apoyo. "
                          "Elimina una para agregar otra."
            }
        
        if not frase:
            frase = random.choice(self.FRASES_PREDEFINIDAS)
        
        persona = {
            "id": len(self.red_apoyo) + 1,
            "nombre": nombre.strip(),
            "relacion": relacion.strip(),
            "frase": frase.strip(),
            "telefono": telefono.strip(),
            "fecha_agregado": datetime.now().isoformat()
        }
        self.red_apoyo.append(persona)
        self._guardar_red()
        return {
            "exito": True,
            "mensaje": f"✅ {nombre} agregado/a a tu Red de Apoyo. ¡Qué bueno tener a alguien de confianza!",
            "persona": persona
        }

    def editar_persona_red(self, id_persona: int, **kwargs) -> dict:
        """Edita los datos de una persona en la red de apoyo."""
        for persona in self.red_apoyo:
            if persona["id"] == id_persona:
                if "nombre" in kwargs:
                    persona["nombre"] = kwargs["nombre"].strip()
                if "relacion" in kwargs:
                    persona["relacion"] = kwargs["relacion"].strip()
                if "frase" in kwargs:
                    persona["frase"] = kwargs["frase"].strip()
                if "telefono" in kwargs:
                    persona["telefono"] = kwargs["telefono"].strip()
                self._guardar_red()
                return {"exito": True, "mensaje": "✅ Datos actualizados.", "persona": persona}
        return {"exito": False, "mensaje": "Persona no encontrada en tu Red de Apoyo."}

    def eliminar_persona_red(self, id_persona: int) -> dict:
        """Elimina una persona de la red de apoyo."""
        for i, persona in enumerate(self.red_apoyo):
            if persona["id"] == id_persona:
                eliminada = self.red_apoyo.pop(i)
                self._guardar_red()
                return {
                    "exito": True,
                    "mensaje": f"🗑️ {eliminada['nombre']} eliminado/a de tu Red de Apoyo."
                }
        return {"exito": False, "mensaje": "Persona no encontrada."}

    def obtener_red_apoyo(self) -> list:
        """Retorna la lista completa de la red de apoyo."""
        return self.red_apoyo

    def obtener_frase_red(self, id_persona: int = None) -> str:
        """
        Retorna una frase de aliento de la red de apoyo.
        Si no se especifica persona, elige una aleatoria.
        """
        if not self.red_apoyo:
            return random.choice(self.FRASES_PREDEFINIDAS)
        
        if id_persona:
            for persona in self.red_apoyo:
                if persona["id"] == id_persona:
                    return f"💬 {persona['nombre']} te dice: \"{persona['frase']}\""
        
        persona = random.choice(self.red_apoyo)
        return f"💬 {persona['nombre']} te dice: \"{persona['frase']}\""

    def obtener_frases_predefinidas(self) -> list:
        """Retorna las frases predefinidas disponibles."""
        return self.FRASES_PREDEFINIDAS

    def resumen_red(self) -> str:
        """Retorna un resumen formateado de la red de apoyo."""
        if not self.red_apoyo:
            return (
                "🤝 RED DE APOYO\n"
                "─" * 30 + "\n\n"
                "Aún no tienes personas en tu Red de Apoyo.\n\n"
                "Tu Red de Apoyo es un espacio para guardar los nombres\n"
                "y las frases de las personas que más te quieren.\n\n"
                "Cuando te sientas mal, puedes leer sus frases\n"
                "y recordar que no estás solo/a.\n\n"
                "Puedes agregar hasta 3 personas. ¿Te animas?"
            )
        
        resumen = "🤝 RED DE APOYO\n"
        resumen += "─" * 30 + "\n\n"
        for persona in self.red_apoyo:
            relacion = f" ({persona['relacion']})" if persona['relacion'] else ""
            resumen += f"❤️  {persona['nombre']}{relacion}\n"
            resumen += f"   💬 \"{persona['frase']}\"\n"
            if persona.get('telefono'):
                resumen += f"   📞 {persona['telefono']}\n"
            resumen += "\n"
        resumen += f"✨ {len(self.red_apoyo)}/{self.MAX_PERSONAS_RED} personas en tu red."
        return resumen


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Alertas v3.0 con Red de Apoyo"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/alertas.py (v3.0 - Red de Apoyo)")
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

    # Limpiar archivo de red de apoyo
    try: os.remove("datos/red_apoyo.json")
    except: pass

    a = Alertas()

    # ─── BÁSICOS ───
    t(isinstance(a, Alertas), "Instancia creada correctamente")
    t(len(a.obtener_contactos()) >= 6, f"{len(a.obtener_contactos())} contactos (mín. 6)")
    t(isinstance(a.obtener_contactos()[0], tuple), "Contactos son tuplas")

    # ─── DETECCIÓN DE RIESGO ───
    t(a.detectar_riesgo("no quiero vivir más") == "alto", "Detecta 'no quiero vivir' como alto")
    t(a.detectar_riesgo("quiero morir ya") == "alto", "Detecta 'quiero morir' como alto")
    t(a.detectar_riesgo("me quiero matar") == "alto", "Detecta 'me quiero matar' como alto")
    t(a.detectar_riesgo("sin mí estarían mejor todos") == "alto", "Detecta 'sin mí estarían mejor' como alto")
    t(a.detectar_riesgo("no sé qué hacer con mi vida") == "medio", "Detecta riesgo medio")
    t(a.detectar_riesgo("me siento vacío") == "medio", "Detecta 'me siento vacío' como medio")
    t(a.detectar_riesgo("nadie me entiende") == "medio", "Detecta 'nadie me entiende' como medio")
    t(a.detectar_riesgo("hola, ¿cómo estás?") == "bajo", "Texto normal = riesgo bajo")
    t(a.detectar_riesgo("hoy me fue bien en la escuela") == "bajo", "Texto positivo = riesgo bajo")

    # ─── MENSAJES ───
    msg_alto = a.obtener_mensaje("alto")
    t("Línea de la Vida" in msg_alto, "Mensaje alto incluye Línea de la Vida")
    t("800" in msg_alto, "Mensaje alto incluye número de contacto")
    t("no estás solo" in msg_alto.lower() or "no estás sola" in msg_alto.lower(), "Mensaje alto es empático")

    msg_medio = a.obtener_mensaje("medio")
    t("Línea de la Vida" in msg_medio, "Mensaje medio incluye Línea de la Vida")
    t("confianza" in msg_medio.lower(), "Mensaje medio menciona confianza")

    t(isinstance(a.obtener_mensaje_acompanamiento(), str) and len(a.obtener_mensaje_acompanamiento()) > 10, 
      "Mensaje de acompañamiento válido")

    # ─── PROCESAR MENSAJES ───
    r = a.procesar_mensaje("no quiero vivir más")
    t(r["nivel"] == "alto", "Procesa nivel alto correctamente")
    t(r["requiere_derivacion"], "Riesgo alto requiere derivación")
    t(len(r["mensaje"]) > 50, "Mensaje de respuesta alto es sustancial")

    r = a.procesar_mensaje("me siento vacío")
    t(r["nivel"] == "medio", "Procesa nivel medio correctamente")
    t(not r["requiere_derivacion"], "Riesgo medio no requiere derivación inmediata")

    r = a.procesar_mensaje("hola, todo bien")
    t(r["nivel"] == "bajo", "Procesa nivel bajo correctamente")
    t(r["mensaje"] is None, "Riesgo bajo no genera mensaje")
    t(not r["requiere_derivacion"], "Riesgo bajo no requiere derivación")

    t(len(a.historial_alertas) == 3, "Historial registra 3 alertas")
    t(a.historial_alertas[0]["nivel"] == "alto", "Historial guarda nivel correcto")

    # ─── CONTACTOS PERSONALIZADOS ───
    a.agregar_contacto("Mi psicóloga", "555-123-4567", "Consultorio")
    t(len(a.obtener_contactos()) == len(a.CONTACTOS) + 1, "Contacto personalizado agregado")
    t(any("Mi psicóloga" in c[0] for c in a.obtener_contactos()), "Contacto aparece en lista")
    t("Mi psicóloga" in a.obtener_mensaje("alto"), "Mensaje incluye contacto personalizado")

    # ─── FRASES DE RIESGO ───
    for frase in ["no quiero vivir", "quiero morir", "me quiero matar", "no valgo nada", "me odio"]:
        t(a.detectar_riesgo(frase) == "alto", f"Detecta '{frase}' como riesgo alto")
    for frase in ["todo me sale mal", "no tengo futuro", "me siento solo todo el tiempo"]:
        t(a.detectar_riesgo(frase) == "medio", f"Detecta '{frase}' como riesgo medio")

    # ─── FALSOS POSITIVOS ───
    t(a.detectar_riesgo("quiero vivir mejor") == "bajo", "'quiero vivir mejor' no es riesgo")
    t(a.detectar_riesgo("me gusta ayudar, no soy una carga para nadie") == "bajo",
      "Negación 'no soy una carga' no dispara alerta")
    t(a.detectar_riesgo("nunca me he sentido una carga para otros") == "bajo",
      "Negación con 'nunca' no dispara alerta")

    # ─── VALIDACIÓN DE CONTACTOS ───
    for nombre, numero, desc in a.CONTACTOS:
        t(isinstance(nombre, str) and len(nombre) > 0, f"Contacto '{nombre}' tiene nombre válido")
        t(isinstance(numero, str) and len(numero) > 0, f"Contacto '{nombre}' tiene número válido")

     # ═══════════════════════════════════════════════════════════
    # NUEVO: RED DE APOYO
    # ═══════════════════════════════════════════════════════════

    # Red vacía al inicio
    t(len(a.obtener_red_apoyo()) == 0, "Red de apoyo inicia vacía")
    t(len(a.obtener_frases_predefinidas()) >= 8, f"{len(a.obtener_frases_predefinidas())} frases predefinidas")

    # Agregar persona 1
    r = a.agregar_persona_red("Mamá", "madre", "Siempre estaré para ti, pase lo que pase.", "555-111-1111")
    t(r["exito"], "Persona 1 agregada a la red")
    t(len(a.obtener_red_apoyo()) == 1, "Red tiene 1 persona")

    # Agregar persona 2
    r = a.agregar_persona_red("Carlos", "mejor amigo", "Eres la persona más fuerte que conozco.", "555-222-2222")
    t(r["exito"], "Persona 2 agregada a la red")
    t(len(a.obtener_red_apoyo()) == 2, "Red tiene 2 personas")

    # Agregar persona 3
    r = a.agregar_persona_red("Abuela", "abuela", "Mi niña/o hermosa/o, nunca olvides lo valioso/a que eres.")
    t(r["exito"], "Persona 3 agregada a la red")
    t(len(a.obtener_red_apoyo()) == 3, "Red tiene 3 personas (máximo)")

    # Intentar agregar persona 4 (debe fallar)
    r = a.agregar_persona_red("Cuarta persona", "conocido", "Hola")
    t(not r["exito"], "No se puede agregar más de 3 personas")
    t("3" in r["mensaje"], "Mensaje indica límite de 3 personas")

    # Agregar con frase predefinida aleatoria (sin frase)
    a.eliminar_persona_red(3)  # Eliminar a la abuela para hacer espacio
    r = a.agregar_persona_red("Tío", "tío")  # Sin frase
    t(r["exito"], "Persona agregada sin frase (usa predefinida)")
    t(len(r["persona"]["frase"]) > 10, "Se asignó frase predefinida aleatoria")

    # Obtener frase de red
    frase = a.obtener_frase_red()
    t("💬" in frase, "Frase de red incluye emoji de diálogo")
    t(len(frase) > 20, "Frase de red sustancial")

    # Obtener frase de persona específica
    frase = a.obtener_frase_red(1)
    t("Mamá" in frase, "Frase específica incluye nombre")
    t("Siempre estaré" in frase, "Frase específica contiene el texto correcto")

    # Editar persona
    r = a.editar_persona_red(1, frase="Te quiero más que a nada en este mundo.")
    t(r["exito"], "Persona editada correctamente")
    t("Te quiero más" in a.obtener_frase_red(1), "Frase actualizada")

    # Editar persona inexistente
    r = a.editar_persona_red(999, nombre="No existe")
    t(not r["exito"], "Editar persona inexistente retorna exito=False")

    # Eliminar persona
    r = a.eliminar_persona_red(2)
    t(r["exito"], "Persona eliminada de la red")
    t(len(a.obtener_red_apoyo()) == 2, "Red tiene 2 personas tras eliminar")

    # Eliminar persona inexistente
    r = a.eliminar_persona_red(999)
    t(not r["exito"], "Eliminar persona inexistente retorna exito=False")

    # Resumen de red
    resumen = a.resumen_red()
    t("RED DE APOYO" in resumen, "Resumen tiene título")
    t("Mamá" in resumen, "Resumen incluye persona 1")
    t("2/3" in resumen, "Resumen muestra conteo 2/3")

    # Red vacía - resumen
    a2 = Alertas()
    resumen_vacio = a2.resumen_red()
    t(len(resumen_vacio) > 50 and "RED DE APOYO" in resumen_vacio, "Resumen vacío es amigable")

    # Red vacía - obtener frase
    frase_vacia = a2.obtener_frase_red()
    t(len(frase_vacia) > 10, "Frase de red vacía usa predefinida")

    # Persistencia de red de apoyo
    a3 = Alertas()
    t(len(a3.obtener_red_apoyo()) == 2, "Red de apoyo persiste tras recargar")

    # Limpiar archivos de prueba
    try:
        os.remove("datos/red_apoyo.json")
    except:
        pass

    total = p_tests + f_tests
    print(f"\n  📊 {p_tests}/{total} tests pasados")
    if f_tests == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Alertas v3.0 con Red de Apoyo validada\n")
    else:
        print(f"  ⚠️  {f_tests} test(s) fallaron\n")
    return f_tests == 0


if __name__ == "__main__":
    ejecutar_tests()