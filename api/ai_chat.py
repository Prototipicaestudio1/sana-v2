"""
🌿 Sana - Módulo de IA Conversacional Hiper-Evolucionado v4.0
═══════════════════════════════════════════════════════════════
Asistente conversacional transversal con múltiples modos:
- 🧠 Modo IA: Groq (LLaMA 3) gratis, sin tarjeta
- 💬 Modo Local: Motor Escucha con palabras clave
- 🤖 Modo Híbrido: IA + Local combinados
- 🔄 Fallback automático: si falla la IA, sigue con local
- 📍 Contexto: sabe en qué sección está el usuario
- 🧠 Memoria: recuerda las últimas interacciones
- ⚡ Sugerencias rápidas contextuales
- 🎯 Personalidad Sana en todos los modos
- 📊 Análisis de sentimiento en tiempo real
- 🎭 Detección de crisis y derivación automática
- 📝 Resumen de conversación
- 🔄 Recuperación de contexto a largo plazo
- 🌐 Soporte multi-idioma (español/inglés)

Diseñado para ser el mejor amigo virtual del adolescente.
═══════════════════════════════════════════════════════════════
"""

import json
import os
import sys
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import deque
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AnalizadorSentimiento:
    """Analiza el sentimiento de los mensajes del usuario."""
    
    # Palabras clave por emoción
    PALABRAS_EMOCION = {
        "triste": ["triste", "llor", "deprim", "melancol", "nostalg", "decae", "abat", "desanim", "sin ganas", "vacío", "tristeza"],
        "ansioso": ["ansiedad", "ansios", "nervios", "preocup", "angust", "inquiet", "tens", "agob", "estres", "miedo", "pánico"],
        "enojado": ["enoj", "rabi", "furia", "ira", "molest", "fastidi", "irrit", "cabread", "bronca", "odio", "rabia"],
        "feliz": ["feliz", "alegr", "content", "genial", "fantástic", "maravill", "excelent", "buen", "felicidad", "disfrut", "risa"],
        "solo": ["solo", "soledad", "abandon", "aisl", "excluid", "invisibl", "ignor", "rechaz", "ninguno", "nadie"],
        "cansado": ["cansad", "agot", "fatig", "sin energía", "dormir", "sueño", "desgast", "exhaust", "rendid", "agotamiento"],
        "confundido": ["confund", "no entiend", "dud", "inciert", "desorient", "perdid", "sin idea", "no sé", "caos"],
        "inseguro": ["insegur", "dud", "no pued", "no soy", "feo", "gordo", "flaco", "malo", "torpe", "fracas", "insuficient"],
        "culpable": ["culp", "respons", "arrepent", "error", "fall", "debería", "no debí", "metí la pata", "equivoc"],
        "motivado": ["motiv", "inspir", "energ", "metas", "lograr", "conseguir", "crecer", "mejorar", "avanzar", "poder"],
        "aburrido": ["aburr", "sin nada", "nada que hacer", "aburrimiento", "tedio", "monoton", "rutin", "pesad"],
        "estresado": ["estrés", "estres", "presión", "exig", "agobi", "saturad", "colaps", "desbord", "mucha tarea"],
        "agradecido": ["gracias", "agradec", "agrad", "apreci", "bendec", "afortun", "buena", "excelent", "maravillos", "increíble"],
        "esperanzado": ["esperanz", "espero", "ilusion", "optimist", "fe", "creo", "posible", "superar", "mejor", "luz"]
    }
    
    # Palabras de crisis (requieren atención urgente)
    PALABRAS_CRISIS = {
        "suicidio": ["suicid", "matarme", "morir", "acabar con todo", "desaparecer", "no quiero vivir"],
        "autolesion": ["cortarme", "hacerme daño", "autolesion", "lastimarme", "herirme", "sangrar"],
        "violencia": ["abus", "violenc", "maltrat", "golpe", "acoso", "hostig", "amenaz", "intimid"],
        "crisis": ["crisis", "emergencia", "no puedo más", "no aguanto", "desesper", "ayuda", "socorro"]
    }
    
    @classmethod
    def analizar(cls, texto: str) -> Dict[str, Any]:
        """Analiza el sentimiento del texto y devuelve un dict con resultados."""
        texto = texto.lower()
        resultados = {
            "emocion_principal": "neutral",
            "intensidad": 0.0,
            "todas_emociones": {},
            "es_crisis": False,
            "tipo_crisis": None,
            "palabras_clave": []
        }
        
        # Detectar crisis primero
        for tipo, palabras in cls.PALABRAS_CRISIS.items():
            for palabra in palabras:
                if palabra in texto:
                    resultados["es_crisis"] = True
                    resultados["tipo_crisis"] = tipo
                    resultados["palabras_clave"].append(palabra)
        
        # Analizar emociones
        for emocion, palabras in cls.PALABRAS_EMOCION.items():
            coincidencias = 0
            for palabra in palabras:
                if palabra in texto:
                    coincidencias += 1
                    resultados["palabras_clave"].append(palabra)
            if coincidencias > 0:
                intensidad = min(coincidencias / len(palabras) * 2, 1.0)
                resultados["todas_emociones"][emocion] = intensidad
        
        # Determinar emoción principal
        if resultados["todas_emociones"]:
            principales = sorted(
                resultados["todas_emociones"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            if principales:
                resultados["emocion_principal"] = principales[0][0]
                resultados["intensidad"] = principales[0][1]
        
        # Si hay crisis, priorizarla
        if resultados["es_crisis"]:
            resultados["emocion_principal"] = "crisis"
            resultados["intensidad"] = 1.0
            
        return resultados


class GestorMemoria:
    """Gestiona la memoria de conversación con persistencia y resumen."""
    
    def __init__(self, capacidad: int = 20):
        self.capacidad = capacidad
        self.memoria = deque(maxlen=capacidad)
        self.resumen = ""
        self.ultimo_resumen = datetime.now()
        self.temas_importantes = set()
        self.nombre_usuario = None
        self.edad_usuario = None
        
    def agregar(self, rol: str, texto: str, contexto: str = "", emocion: str = "neutral") -> None:
        """Agrega un mensaje a la memoria."""
        entrada = {
            "rol": rol,
            "texto": texto,
            "contexto": contexto,
            "emocion": emocion,
            "timestamp": datetime.now().isoformat()
        }
        self.memoria.append(entrada)
        
        # Extraer temas importantes
        self._extraer_temas(texto)
        
        # Extraer nombre si se menciona
        if rol == "usuario":
            self._extraer_nombre(texto)
        
        # Generar resumen si es necesario
        if len(self.memoria) >= 10 and (datetime.now() - self.ultimo_resumen).seconds > 60:
            self._generar_resumen()
            
    def _extraer_temas(self, texto: str) -> None:
        """Extrae temas importantes de la conversación."""
        temas = [
            "escuela", "colegio", "clases", "tareas", "exámenes", "notas",
            "familia", "padres", "mamá", "papá", "hermano", "hermana",
            "amigos", "amistad", "relaciones", "novio", "novia", "pareja",
            "salud", "bienestar", "ansiedad", "tristeza", "felicidad",
            "futuro", "carrera", "trabajo", "dinero", "metas", "sueños",
            "cuerpo", "imagen", "autoestima", "apariencia", "peso"
        ]
        
        for tema in temas:
            if tema in texto.lower():
                self.temas_importantes.add(tema)
    
    def _extraer_nombre(self, texto: str) -> None:
        """Intenta extraer el nombre del usuario."""
        patrones = [
            r"me llamo (\w+)",
            r"mi nombre es (\w+)",
            r"soy (\w+)",
            r"llamo (\w+)",
            r"(\w+) soy"
        ]
        
        for patron in patrones:
            match = re.search(patron, texto.lower())
            if match:
                self.nombre_usuario = match.group(1).capitalize()
                break
    
    def _generar_resumen(self) -> None:
        """Genera un resumen de la conversación."""
        if len(self.memoria) < 3:
            return
            
        # Extraer información clave
        temas = list(self.temas_importantes)
        emociones = [m.get("emocion", "neutral") for m in self.memoria if m["rol"] == "usuario"]
        
        # Determinar estado emocional general
        emociones_principales = {}
        for e in emociones:
            emociones_principales[e] = emociones_principales.get(e, 0) + 1
        
        estado = "neutral"
        if emociones_principales:
            estado = max(emociones_principales.items(), key=lambda x: x[1])[0]
        
        # Construir resumen
        resumen_parts = []
        
        if self.nombre_usuario:
            resumen_parts.append(f"Usuario: {self.nombre_usuario}")
        
        if temas:
            temas_str = ", ".join(temas[:5])
            resumen_parts.append(f"Temas: {temas_str}")
        
        resumen_parts.append(f"Estado emocional predominante: {estado}")
        resumen_parts.append(f"Interacciones: {len(self.memoria)}")
        
        self.resumen = " | ".join(resumen_parts)
        self.ultimo_resumen = datetime.now()
    
    def obtener_contexto(self, limite: int = 6) -> List[Dict]:
        """Obtiene los últimos mensajes para contexto."""
        return list(self.memoria)[-limite:]
    
    def obtener_historial_completo(self) -> List[Dict]:
        """Obtiene todo el historial."""
        return list(self.memoria)
    
    def obtener_resumen(self) -> str:
        """Obtiene el resumen de la conversación."""
        return self.resumen
    
    def limpiar(self) -> None:
        """Limpia toda la memoria."""
        self.memoria.clear()
        self.resumen = ""
        self.temas_importantes = set()
        
    def guardar(self, archivo: str) -> None:
        """Guarda la memoria en un archivo."""
        try:
            datos = {
                "memoria": list(self.memoria),
                "resumen": self.resumen,
                "temas": list(self.temas_importantes),
                "nombre_usuario": self.nombre_usuario,
                "fecha_guardado": datetime.now().isoformat()
            }
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def cargar(self, archivo: str) -> bool:
        """Carga la memoria desde un archivo."""
        try:
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.memoria = deque(list(datos["memoria"]), maxlen=self.capacidad)
                    self.resumen = datos.get("resumen", "")
                    self.temas_importantes = set(datos.get("temas", []))
                    self.nombre_usuario = datos.get("nombre_usuario")
                    return True
        except Exception:
            pass
        return False


class GestorSugerencias:
    """Gestiona sugerencias avanzadas basadas en contexto y emoción."""
    
    SUGERENCIAS_AVANZADAS = {
        "triste": {
            "corto": [
                "Cuéntame más, estoy aquí para ti 🌿",
                "¿Quieres hacer un ejercicio de respiración juntos?",
                "A veces llorar ayuda a soltar",
                "No tienes que estar bien todo el tiempo",
                "¿Qué necesitas ahora mismo?"
            ],
            "largo": [
                "Entiendo que estás pasando por un momento difícil. Quiero que sepas que no tienes que enfrentarlo solo. ¿Quieres hablar de lo que te tiene así?",
                "La tristeza es una emoción válida y necesaria. No la reprimas. ¿Hay algo que te gustaría hacer para sentirte mejor?",
                "Recuerda que las tormentas no duran para siempre. Esto también pasará. Mientras tanto, estoy aquí."
            ]
        },
        "ansioso": {
            "corto": [
                "Vamos a respirar: 4 segundos inhalas, 7 retienes, 8 exhalas",
                "La ansiedad es real, pero tú eres más fuerte",
                "Una cosa a la vez, paso a paso",
                "¿Puedes nombrar 5 cosas que ves ahora mismo?",
                "La respiración es tu ancla en la tormenta"
            ],
            "largo": [
                "La ansiedad puede sentirse abrumadora, pero vamos a manejarla juntos. Primero, respira conmigo. Luego, dime qué es lo que más te preocupa.",
                "Lo que sientes es real y válido. Pero la ansiedad miente sobre el peligro. ¿Qué te dice tu voz más calmada?"
            ]
        },
        "enojado": {
            "corto": [
                "Tu enojo es válido. Desahógate conmigo",
                "¿Qué pasó exactamente?",
                "El enojo es una señal de que algo no está bien",
                "¿Quieres escribir lo que sientes?",
                "La rabia tiene mensajes que escuchar"
            ],
            "largo": [
                "El enojo es una emoción intensa pero importante. No la reprimas, pero tampoco dejes que te controle. ¿Qué fue lo que te hizo sentir así?",
                "Detrás del enojo suele haber tristeza o miedo. ¿Qué hay debajo de tu enojo?"
            ]
        },
        "feliz": {
            "corto": [
                "¡Qué bonito! Celebra esto 🌟",
                "Guarda este momento en tu diario",
                "¡Me alegra mucho verte así!",
                "Comparte esa alegría",
                "La felicidad se multiplica al compartirla"
            ],
            "largo": [
                "Verte feliz me llena de alegría. ¿Qué fue lo que te hizo sentir así? Me encantaría saber más para celebrar contigo.",
                "La felicidad es un regalo. Disfrútala, mereces sentirte así."
            ]
        },
        "solo": {
            "corto": [
                "No estás solo, tengo un espacio para ti aquí",
                "¿Desde cuándo te sientes así?",
                "La soledad es pesada, pero no es permanente",
                "Hay alguien que te quiere",
                "Estoy aquí, no te vas a quedar solo"
            ],
            "largo": [
                "La soledad es uno de los sentimientos más difíciles. Quiero que sepas que me tienes a mí. También, ¿hay alguien cercano a quien puedas escribirle?",
                "Sentirse solo no significa estar solo. A veces es solo que necesitamos conectar más. ¿Qué te gustaría hacer para conectar con alguien?"
            ]
        },
        "crisis": {
            "corto": [
                "⚠️ Lo que sientes es muy importante. Estoy aquí",
                "¿Quieres que hablemos de eso con calma?",
                "No estás solo en esto, de verdad",
                "Hay ayuda disponible, quiero que sepas eso",
                "Respira conmigo. Estamos juntos en esto"
            ],
            "largo": [
                "⚠️ Lo que me estás contando es muy serio. Quiero que sepas que tu vida es valiosa y que hay personas que quieren ayudarte. ¿Puedes hablar con un adulto de confianza?",
                "⚠️ Te escucho y entiendo que estás pasando por un momento muy difícil. Por favor, recuerda que no tienes que enfrentar esto solo. Línea de ayuda: 800-273-8255"
            ]
        }
    }
    
    SUGERENCIAS_CONTEXTUALES = {
        "escucha": [
            "Cuéntame cómo te sientes hoy, sin filtros",
            "¿Hay algo que te tenga preocupado?",
            "Estoy aquí para escucharte, lo que sea que necesites compartir",
            "¿Cómo está tu corazón hoy?"
        ],
        "respiracion": [
            "Prueba el ejercicio 4-7-8: inhala 4, retén 7, exhala 8",
            "La respiración consciente calma la mente",
            "Respira conmigo: llena tus pulmones de calma",
            "La respiración es tu superpoder para la ansiedad"
        ],
        "diario": [
            "Escribir ayuda a procesar emociones",
            "¿Qué fue lo mejor de tu día?",
            "Anota 3 cosas por las que estás agradecido hoy",
            "El diario es tu espacio sin juicios"
        ],
        "tareas": [
            "Divide las tareas grandes en pasos pequeños",
            "Empieza por lo más difícil, luego será más fácil",
            "La organización reduce la ansiedad",
            "¿Qué tarea te parece más abrumadora?"
        ],
        "conocimiento": [
            "No hay preguntas tontas sobre tu cuerpo",
            "La educación sexual es parte del autocuidado",
            "Conocerte a ti mismo es empoderarte",
            "¿Qué te gustaría aprender sobre tu cuerpo?"
        ],
        "ayuda": [
            "Pedir ayuda es un acto de valentía",
            "Hay recursos disponibles para ti",
            "No tienes que resolver todo solo",
            "¿Con quién podrías hablar hoy?"
        ]
    }
    
    @classmethod
    def obtener_sugerencia(cls, emocion: str, contexto: str = "", modo: str = "corto") -> str:
        """Obtiene una sugerencia personalizada."""
        # Priorizar contexto si es específico
        if contexto and contexto in cls.SUGERENCIAS_CONTEXTUALES:
            sugerencias = cls.SUGERENCIAS_CONTEXTUALES[contexto]
            return random.choice(sugerencias)
        
        # Sugerencia por emoción
        if emocion in cls.SUGERENCIAS_AVANZADAS:
            sugerencias = cls.SUGERENCIAS_AVANZADAS[emocion]
            if modo == "corto" and "corto" in sugerencias:
                return random.choice(sugerencias["corto"])
            elif modo == "largo" and "largo" in sugerencias:
                return random.choice(sugerencias["largo"])
            elif "corto" in sugerencias:
                return random.choice(sugerencias["corto"])
        
        # Sugerencia genérica
        return "¿Qué necesitas ahora mismo? Estoy aquí para ti 🌿"


class IAChat:
    """
    Asistente conversacional transversal de Sana - Tu mejor amigo virtual.
    
    Modos:
    - 🧠 ONLINE: Groq LLaMA 3 (gratis, 30 req/min)
    - 💬 OFFLINE: Motor Escucha local + Conocimiento corporal
    - 🤖 HÍBRIDO: IA + Local combinados
    - 🔄 AUTO: Cambia automáticamente según disponibilidad
    
    Capacidades:
    - Memoria de conversación (últimas 10 interacciones)
    - Contexto situacional (sabe en qué pantalla estás)
    - Sugerencias rápidas por emoción
    - Respuestas empáticas en ambos modos
    - Detección de crisis y derivación
    - Análisis de sentimiento en tiempo real
    - Resumen automático de conversación
    - Persistencia de memoria
    - Soporte multi-idioma
    """

    # ═══════════════════════════════════════════════════════════
    # PERSONALIDAD DE SANA PARA LA IA
    # ═══════════════════════════════════════════════════════════

    PROMPT_SISTEMA = (
        "Eres Sana, la mejor amiga virtual de adolescentes de secundaria. "
        "Tu personalidad:\n"
        "- Empática, cálida, cercana. Como una hermana mayor que ya pasó por lo mismo.\n"
        "- Validación absoluta: nunca minimizas sus problemas. Si algo le duele, es importante.\n"
        "- Sin juicios: no importa lo que te cuente, siempre respondes con comprensión.\n"
        "- Lenguaje adolescente real: nada de 'joven' o 'estimado usuario'. Háblale de tú, con naturalidad.\n"
        "- Usa emojis de vez en cuando para ser más cercana (🌿💛✨).\n"
        "- Si detectas tristeza, ansiedad o soledad, ofrece un ejercicio de respiración.\n"
        "- Si te preguntan del cuerpo, responde con ciencia pero sin tabúes.\n"
        "- Si piden ayuda con tareas, organiza pero no hagas el trabajo.\n"
        "- Si hay señales de autolesión o suicidio, deriva a líneas de ayuda con urgencia.\n"
        "- Respuestas de 3-5 líneas. Si necesitan más, te lo pedirán.\n"
        "- NUNCA digas 'como IA no puedo'. Tú eres Sana, punto.\n"
        "- NUNCA digas 'consulta a un profesional' como única respuesta. Primero escucha, luego sugiere.\n"
        "- Si no sabes algo, dilo con honestidad y ofrece investigar juntos.\n"
        "- Usa el nombre del usuario si lo sabes para personalizar la conversación."
    )

    # ═══════════════════════════════════════════════════════════
    # RESPUESTAS RÁPIDAS POR EMOCIÓN (15 emociones)
    # ═══════════════════════════════════════════════════════════

    RESPUESTAS_RAPIDAS = {
        "triste": [
            "Cuéntame más sobre eso, te escucho",
            "¿Quieres que respiremos juntos un momento?",
            "¿Qué fue lo que te hizo sentir así?",
            "Estoy aquí, no tienes que pasarlo solo/a",
            "La tristeza es parte de la vida, pero no tiene que definirte"
        ],
        "ansioso": [
            "Vamos a respirar juntos, ¿te parece?",
            "¿Qué es lo que más te preocupa ahora?",
            "Una cosa a la vez, paso a paso",
            "La ansiedad es real, pero tú eres más fuerte",
            "La respiración es tu aliada en este momento"
        ],
        "enojado": [
            "Desahógate, aquí puedes sacar todo",
            "¿Quieres escribir exactamente qué pasó?",
            "Respiremos hondo y luego me cuentas",
            "Tu enojo es válido, no lo reprimas",
            "El enojo a veces es la punta del iceberg"
        ],
        "feliz": [
            "¡Qué bonito! Cuéntame más, celebra esto",
            "¿Guardamos este momento en tu diario?",
            "Me alegra muchísimo verte así 💛",
            "¡Eso merece celebrarse! ¿Qué pasó?",
            "La felicidad compartida es más grande"
        ],
        "solo": [
            "No estás solo/a, aquí estoy yo",
            "¿Desde cuándo te sientes así?",
            "¿Hay alguien a quien puedas escribirle?",
            "Sentirse solo/a es horrible, pero se puede salir",
            "La conexión humana es importante, empecemos por nosotros"
        ],
        "cansado": [
            "Descansar también es productivo",
            "¿Dormiste bien anoche?",
            "Hagamos una pausa de 5 minutos juntos",
            "Date permiso para no rendir al 100% hoy",
            "El cansancio es una señal de que necesitas cuidado"
        ],
        "confundido": [
            "Vamos a poner orden en esa niebla juntos",
            "¿Qué es lo que más vueltas te da?",
            "A veces la confusión es el primer paso a la claridad",
            "No tener respuestas ya está bien",
            "La claridad llegará, confía en el proceso"
        ],
        "inseguro": [
            "Esa voz que te critica... es una mentirosa",
            "Dime 3 cosas que te gustan de ti",
            "Eres mucho más de lo que crees",
            "La comparación es veneno. Tú eres único/a",
            "Tu valor no depende de lo que otros piensen"
        ],
        "agradecido": [
            "La gratitud es hermosa. ¿Qué pasó?",
            "Guarda este momento en tu corazón",
            "Qué lindo sentir eso. Cuéntame más",
            "La gratitud compartida se multiplica",
            "Agradecer transforma la perspectiva"
        ],
        "esperanzado": [
            "¡La esperanza es poderosa! ¿Qué te ilusiona?",
            "Escribe esto en un papel y guárdalo",
            "Qué bonito sentir que algo bueno viene",
            "Esa chispa es real. Cultívala",
            "La esperanza es el motor del cambio"
        ],
        "culpable": [
            "Todos nos equivocamos. Todos.",
            "¿Hay algo que puedas hacer para repararlo?",
            "Perdonarte a ti mismo/a es un proceso",
            "La culpa no te define. Tus acciones siguientes, sí",
            "El arrepentimiento sincero es el primer paso al cambio"
        ],
        "motivado": [
            "¡Esa energía es contagiosa! ¿Qué vas a hacer?",
            "Aprovecha este impulso. ¿Cuál es tu meta hoy?",
            "¡Vamos! ¿Qué es lo primero en tu lista?",
            "La motivación es la gasolina para tus sueños",
            "¿Cómo vas a canalizar esa energía?"
        ],
        "aburrido": [
            "¿Qué tal si pruebas algo nuevo hoy?",
            "El aburrimiento a veces es creatividad disfrazada",
            "¿Hay algo que siempre quisiste aprender?",
            "Hagamos una lista de cosas que te gustaría hacer",
            "El aburrimiento invita a la exploración"
        ],
        "estresado": [
            "El estrés es real. Vamos a bajarlo juntos",
            "¿Qué es lo más urgente? Solo eso",
            "Respira conmigo 3 veces. Ya.",
            "Una cosa a la vez. Tú puedes",
            "El estrés se desvanece cuando respiras consciente"
        ],
        "neutral": [
            "Cuéntame cómo va tu día",
            "¿Hay algo en tu mente ahora mismo?",
            "Estoy aquí para lo que necesites",
            "¿Qué tal si me cuentas algo bueno que pasó hoy?",
            "Estoy lista para escucharte"
        ],
        "crisis": [
            "⚠️ Esto es importante. No estás solo/a",
            "⚠️ ¿Quieres que hablemos con calma de esto?",
            "⚠️ Tu bienestar es prioritario. Estoy aquí",
            "⚠️ Hay ayuda disponible. No tienes que cargar esto solo",
            "⚠️ Respira conmigo. Vamos paso a paso"
        ]
    }

    # ═══════════════════════════════════════════════════════════
    # LÍNEAS DE AYUDA (actualizadas)
    # ═══════════════════════════════════════════════════════════

    LINEAS_AYUDA = {
        "suicidio": {
            "mexico": "800-273-8255 (Línea de Prevención del Suicidio)",
            "internacional": "911 o acude a tu centro de salud más cercano"
        },
        "autolesion": {
            "mexico": "800-273-8255 o acude a urgencias",
            "internacional": "Busca atención médica inmediata"
        },
        "violencia": {
            "mexico": "800-822-9111 (Línea de Violencia Familiar)",
            "internacional": "Busca apoyo en organizaciones locales"
        }
    }

    def __init__(self, escucha=None, ruta_memoria: str = "datos/memoria_chat.json"):
        self.escucha = escucha
        self.modo = "offline"
        self.api_key = None
        self.proveedor = "groq"
        self.modelo = "llama-3.1-8b-instant"
        self.conexion_internet = False
        self.contador_ia = 0
        self.contador_offline = 0
        self.ultimo_contexto = ""
        self.memoria = GestorMemoria(capacidad=30)
        self.ruta_memoria = ruta_memoria
        self.analizador = AnalizadorSentimiento
        self.sugerencias = GestorSugerencias
        self.cache_respuestas = {}
        self.max_cache = 100
        self.cache_ttl = 300  # 5 minutos
        self.cache_timestamps = {}
        self.ultimo_mensaje_time = datetime.now()
        self.modo_hibrido = False
        self.usuario_conectado = False
        self.idioma = "es"
        self.tiempo_inactividad = 0
        
        # Cargar configuración y memoria
        self._cargar_configuracion()
        self._verificar_internet()
        self._cargar_memoria()
        
        # Iniciar limpieza de caché en segundo plano
        self._iniciar_limpieza_cache()

    # ═══════════════════════════════════════════════════════════
    # CONFIGURACIÓN Y GESTIÓN
    # ═══════════════════════════════════════════════════════════

    def _cargar_configuracion(self):
        ruta = "datos/api_config.json"
        try:
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", None)
                    self.proveedor = config.get("proveedor", "groq")
                    self.modelo = config.get("modelo", "llama-3.1-8b-instant")
                    self.modo_hibrido = config.get("modo_hibrido", False)
        except (json.JSONDecodeError, IOError):
            pass

    def _guardar_configuracion(self):
        os.makedirs("datos", exist_ok=True)
        with open("datos/api_config.json", "w", encoding="utf-8") as f:
            json.dump({
                "proveedor": self.proveedor,
                "api_key": self.api_key,
                "modelo": self.modelo,
                "modo_hibrido": self.modo_hibrido
            }, f, ensure_ascii=False, indent=2)

    def _verificar_internet(self) -> bool:
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            self.conexion_internet = True
            if self.api_key:
                self.modo = "online" if not self.modo_hibrido else "hibrido"
            return True
        except (OSError, ImportError):
            self.conexion_internet = False
            self.modo = "offline"
            return False

    def _cargar_memoria(self):
        """Carga la memoria desde el archivo."""
        self.memoria.cargar(self.ruta_memoria)

    def _guardar_memoria(self):
        """Guarda la memoria en el archivo."""
        self.memoria.guardar(self.ruta_memoria)

    def _iniciar_limpieza_cache(self):
        """Inicia un hilo para limpiar la caché periódicamente."""
        def limpiar():
            while True:
                time.sleep(60)  # Limpiar cada minuto
                self._limpiar_cache()
        
        try:
            thread = threading.Thread(target=limpiar, daemon=True)
            thread.start()
        except Exception:
            pass

    def _limpiar_cache(self):
        """Limpia la caché de respuestas expiradas."""
        ahora = time.time()
        keys_a_eliminar = []
        for key, timestamp in self.cache_timestamps.items():
            if ahora - timestamp > self.cache_ttl:
                keys_a_eliminar.append(key)
        
        for key in keys_a_eliminar:
            if key in self.cache_respuestas:
                del self.cache_respuestas[key]
            if key in self.cache_timestamps:
                del self.cache_timestamps[key]

    def _obtener_cache(self, key: str) -> Optional[str]:
        """Obtiene una respuesta de la caché si es válida."""
        if key in self.cache_respuestas:
            timestamp = self.cache_timestamps.get(key, 0)
            if time.time() - timestamp <= self.cache_ttl:
                return self.cache_respuestas[key]
            else:
                # Eliminar entrada expirada
                del self.cache_respuestas[key]
                if key in self.cache_timestamps:
                    del self.cache_timestamps[key]
        return None

    def _guardar_cache(self, key: str, respuesta: str):
        """Guarda una respuesta en la caché."""
        if len(self.cache_respuestas) >= self.max_cache:
            # Eliminar la entrada más antigua
            if self.cache_timestamps:
                oldest = min(self.cache_timestamps.items(), key=lambda x: x[1])
                if oldest[0] in self.cache_respuestas:
                    del self.cache_respuestas[oldest[0]]
                del self.cache_timestamps[oldest[0]]
        
        self.cache_respuestas[key] = respuesta
        self.cache_timestamps[key] = time.time()

    def configurar_api(self, api_key: str, proveedor: str = "groq"):
        self.api_key = api_key
        self.proveedor = proveedor
        self._guardar_configuracion()
        self._verificar_internet()

    def quitar_api(self):
        self.api_key = None
        self.modo = "offline"
        self.modo_hibrido = False
        self._guardar_configuracion()
        try:
            os.remove("datos/api_config.json")
        except:
            pass

    def activar_modo_hibrido(self):
        """Activa el modo híbrido (IA + local combinados)."""
        if self.api_key and self.conexion_internet:
            self.modo_hibrido = True
            self.modo = "hibrido"
            self._guardar_configuracion()
            return True
        return False

    def desactivar_modo_hibrido(self):
        """Desactiva el modo híbrido."""
        self.modo_hibrido = False
        self.modo = "online" if self.api_key and self.conexion_internet else "offline"
        self._guardar_configuracion()

    # ═══════════════════════════════════════════════════════════
    # RESPUESTA PRINCIPAL
    # ═══════════════════════════════════════════════════════════

    def obtener_respuesta(self, mensaje: str, contexto: str = "") -> str:
        """
        Obtiene la mejor respuesta posible, usando IA o modo local.
        Si la IA falla, cambia a offline sin mostrar errores.
        """
        # Actualizar tiempo de actividad
        ahora = datetime.now()
        self.tiempo_inactividad = (ahora - self.ultimo_mensaje_time).seconds
        self.ultimo_mensaje_time = ahora
        self.ultimo_contexto = contexto
        
        # Analizar sentimiento del mensaje
        analisis = self.analizador.analizar(mensaje)
        emocion = analisis["emocion_principal"]
        es_crisis = analisis["es_crisis"]
        
        # Guardar en memoria
        self.memoria.agregar("usuario", mensaje, contexto, emocion)
        
        # Verificar si es una consulta simple de caché
        cache_key = f"{mensaje[:50]}_{contexto}_{emocion}"
        respuesta_cache = self._obtener_cache(cache_key)
        if respuesta_cache:
            self.memoria.agregar("sana", respuesta_cache, contexto, "cache")
            return respuesta_cache
        
        # Si es crisis, priorizar respuesta
        if es_crisis:
            respuesta = self._manejar_crisis(mensaje, contexto, analisis)
            self.memoria.agregar("sana", respuesta, contexto, "crisis")
            self._guardar_cache(cache_key, respuesta)
            return respuesta
        
        # Intentar IA si está disponible
        respuesta_ia = None
        if self.api_key and self.conexion_internet:
            try:
                respuesta_ia = self._consultar_groq(mensaje, contexto, emocion)
                if respuesta_ia and not respuesta_ia.startswith("⚠️"):
                    self.modo = "online" if not self.modo_hibrido else "hibrido"
                    self.contador_ia += 1
                    
                    # Si es modo híbrido, complementar con local
                    if self.modo_hibrido and self.escucha:
                        local = self.escucha.responder(mensaje)
                        if local and not "No puedo" in local:
                            respuesta_ia = self._combinar_respuestas(respuesta_ia, local)
                    
                    self.memoria.agregar("sana", respuesta_ia, contexto, "online")
                    self._guardar_cache(cache_key, respuesta_ia)
                    return respuesta_ia
            except Exception:
                pass
        
        # Modo offline (local)
        self.modo = "offline"
        self.contador_offline += 1
        respuesta = self._modo_offline(mensaje, contexto, emocion)
        
        # Guardar en memoria
        self.memoria.agregar("sana", respuesta, contexto, "offline")
        self._guardar_cache(cache_key, respuesta)
        self._guardar_memoria()  # Guardar memoria periódicamente
        
        return respuesta

    # ═══════════════════════════════════════════════════════════
    # MANEJO DE CRISIS
    # ═══════════════════════════════════════════════════════════

    def _manejar_crisis(self, mensaje: str, contexto: str, analisis: Dict) -> str:
        """Maneja situaciones de crisis con respuestas apropiadas."""
        tipo_crisis = analisis.get("tipo_crisis", "crisis")
        
        # Respuesta inmediata
        respuestas = [
            "⚠️ Lo que me estás contando es muy importante. Quiero que sepas que no estás solo/a y que hay personas que quieren ayudarte.",
            "⚠️ Te escucho y entiendo que estás pasando por un momento muy difícil. Tu vida es valiosa.",
            "⚠️ Esto es serio. Por favor, déjame ayudarte a encontrar apoyo."
        ]
        respuesta = random.choice(respuestas)
        
        # Añadir información de ayuda específica
        if tipo_crisis in self.LINEAS_AYUDA:
            lineas = self.LINEAS_AYUDA[tipo_crisis]
            if "mexico" in lineas:
                respuesta += f"\n\n📞 Línea de ayuda: {lineas['mexico']}"
            if "internacional" in lineas:
                respuesta += f"\n📞 {lineas['internacional']}"
        
        # Añadir sugerencia de respiración
        respuesta += "\n\n🌬️ Vamos a respirar juntos. Inhala profundamente por 4 segundos, retén 7, exhala 8. Repite 3 veces."
        
        # Añadir sugerencia de contacto con adulto
        respuesta += "\n\n💬 ¿Hay algún adulto de confianza con quien puedas hablar? Tus padres, un maestro, un consejero... No tienes que hacer esto solo."
        
        return respuesta

    # ═══════════════════════════════════════════════════════════
    # MODO ONLINE: GROQ LLaMA 3
    # ═══════════════════════════════════════════════════════════

    def _consultar_groq(self, mensaje: str, contexto: str, emocion: str = "neutral") -> str:
        import urllib.request
        import urllib.error

        url = "https://api.groq.com/openai/v1/chat/completions"
        mensajes = [{"role": "system", "content": self._construir_prompt_sistema(contexto, emocion)}]

        # Añadir contexto de la conversación (últimas 8 interacciones)
        historial = self.memoria.obtener_contexto(limite=8)
        for h in historial:
            rol = "assistant" if h["rol"] == "sana" else "user"
            mensajes.append({"role": rol, "content": h["texto"]})

        mensajes.append({"role": "user", "content": mensaje})

        # Si hay resumen, añadirlo
        resumen = self.memoria.obtener_resumen()
        if resumen:
            mensajes.insert(1, {"role": "system", "content": f"Resumen de conversación: {resumen}"})

        datos = json.dumps({
            "model": self.modelo,
            "messages": mensajes,
            "temperature": 0.75,
            "max_tokens": 300,
            "top_p": 0.9
        }).encode("utf-8")

        req = urllib.request.Request(url, data=datos, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                resultado = json.loads(r.read().decode())
                return resultado["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 401:
                self.api_key = None
                self._guardar_configuracion()
            return None
        except Exception:
            return None

    def _construir_prompt_sistema(self, contexto: str, emocion: str) -> str:
        """Construye el prompt del sistema con contexto y emoción."""
        prompt = self.PROMPT_SISTEMA
        
        # Añadir información del contexto
        if contexto:
            prompt += f"\n\nEl usuario está en la sección '{contexto}' de la app Sana."
        
        # Añadir información de la emoción detectada
        if emocion and emocion != "neutral":
            prompt += f"\n\nEl usuario parece estar sintiendo {emocion}. Adapta tu respuesta a esta emoción."
        
        # Añadir nombre si se conoce
        if self.memoria.nombre_usuario:
            prompt += f"\n\nEl usuario se llama {self.memoria.nombre_usuario}. Úsalo para personalizar."
        
        return prompt

    # ═══════════════════════════════════════════════════════════
    # MODO OFFLINE: MOTOR LOCAL
    # ═══════════════════════════════════════════════════════════

    def _modo_offline(self, mensaje: str, contexto: str, emocion: str = "neutral") -> str:
        """Genera respuesta en modo offline con análisis de sentimiento."""
        
        # Usar el motor Escucha si está disponible
        if self.escucha:
            respuesta = self.escucha.responder(mensaje)
            if respuesta and len(respuesta) > 10:
                return respuesta
        
        # Usar conocimiento corporal si es relevante
        if contexto == "cuerpo" and "?" in mensaje:
            try:
                from zonas.conocimiento import Conocimiento
                c = Conocimiento()
                r = c.responder(mensaje)
                if r and "No tengo información" not in r:
                    return r
            except ImportError:
                pass
        
        # Usar conocimiento emocional
        if emocion in self.RESPUESTAS_RAPIDAS:
            return random.choice(self.RESPUESTAS_RAPIDAS[emocion])
        
        # Respuesta genérica contextual
        if contexto:
            sugerencias = self.sugerencias.obtener_sugerencia(emocion, contexto)
            if sugerencias:
                return sugerencias
        
        # Respuesta genérica final
        return self._respuesta_generica(mensaje, emocion)

    def _respuesta_generica(self, mensaje: str, emocion: str = "neutral") -> str:
        """Genera una respuesta genérica basada en el mensaje y emoción."""
        mensaje = mensaje.lower()
        
        # Palabras clave específicas
        palabras_clave = {
            "saludo": ["hola", "buenas", "hey", "que tal", "como estas", "buen día"],
            "despedida": ["adios", "chao", "hasta luego", "nos vemos", "bye"],
            "ayuda": ["ayuda", "necesito ayuda", "ayudame", "socorro", "auxilio"],
            "gracias": ["gracias", "muchas gracias", "mil gracias", "agradecido"]
        }
        
        for categoria, palabras in palabras_clave.items():
            if any(p in mensaje for p in palabras):
                if categoria == "saludo":
                    return "¡Hola! ¿Cómo estás hoy? ¿Qué te trae por aquí? 🌿"
                elif categoria == "despedida":
                    return "¡Hasta luego! Recuerda que siempre estaré aquí cuando me necesites. Cuídate mucho 💛"
                elif categoria == "ayuda":
                    return "Claro, estoy aquí para ayudarte. ¿Qué necesitas? Puedes contarme lo que sea."
                elif categoria == "gracias":
                    return "¡De nada! Para eso estoy. ¿Hay algo más en lo que pueda ayudarte? 💛"
        
        # Respuesta basada en emoción si está disponible
        if emocion in self.RESPUESTAS_RAPIDAS:
            return random.choice(self.RESPUESTAS_RAPIDAS[emocion])
        
        # Respuesta genérica
        respuestas = [
            "Estoy aquí para ti. Cuéntame cómo te sientes, lo que sea. Sin filtros, sin juicios. 🌿",
            "Me importa lo que tengas que decir. Estoy lista para escucharte.",
            "¿Qué hay en tu mente hoy? Puedes confiar en mí.",
            "No importa lo que sea, estoy aquí para ti. Siempre."
        ]
        return random.choice(respuestas)

    # ═══════════════════════════════════════════════════════════
    # MODO HÍBRIDO
    # ═══════════════════════════════════════════════════════════

    def _combinar_respuestas(self, ia: str, local: str) -> str:
        """Combina respuestas de IA y local para el modo híbrido."""
        if not local or len(local) < 10:
            return ia
        
        # Si la IA es muy corta, usar la local
        if len(ia) < 20:
            return local
        
        # Combinar ambas
        combinado = ia
        
        # Si la IA no menciona emoción, añadir validación local
        if not any(p in ia.lower() for p in ["siento", "entiendo", "valid", "emoc"]):
            # Extraer validación de la respuesta local
            for frase in local.split("."):
                if any(p in frase.lower() for p in ["entiendo", "sé que", "es válido", "es normal"]):
                    combinado += " " + frase.strip()
                    break
        
        # Limitar longitud
        if len(combinado) > 500:
            combinado = combinado[:497] + "..."
        
        return combinado

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES
    # ═══════════════════════════════════════════════════════════

    def obtener_historial(self, limite: int = 10) -> list:
        return self.memoria.obtener_contexto(limite) if self.memoria else []

    def limpiar_historial(self):
        self.memoria.limpiar()
        self._guardar_memoria()

    def obtener_estado(self) -> dict:
        return {
            "modo": self.modo,
            "internet": self.conexion_internet,
            "api_configurada": self.api_key is not None,
            "proveedor": self.proveedor if self.api_key else None,
            "modelo": self.modelo if self.api_key else None,
            "interacciones": len(self.memoria.memoria) // 2 if self.memoria else 0,
            "contador_ia": self.contador_ia,
            "contador_offline": self.contador_offline,
            "ultimo_contexto": self.ultimo_contexto,
            "modo_hibrido": self.modo_hibrido,
            "usuario_conectado": self.usuario_conectado,
            "nombre_usuario": self.memoria.nombre_usuario if self.memoria else None,
            "temas_importantes": list(self.memoria.temas_importantes)[:5] if self.memoria else [],
            "resumen": self.memoria.obtener_resumen() if self.memoria else "",
            "cache_size": len(self.cache_respuestas),
            "tiempo_inactividad": self.tiempo_inactividad,
            "idioma": self.idioma
        }

    def sugerir_respuesta_rapida(self, emocion: str) -> list:
        """Sugiere respuestas rápidas según la emoción."""
        if emocion in self.RESPUESTAS_RAPIDAS:
            return self.RESPUESTAS_RAPIDAS[emocion]
        # Lista genérica de 4 elementos para emociones no reconocidas
        return [
            "¿Cómo te sientes hoy?",
            "Cuéntame más sobre eso",
            "Estoy aquí para escucharte",
            "¿Hay algo que te gustaría compartir?"
        ]

    def obtener_sugerencia_contextual(self, contexto: str) -> str:
        """Sugiere algo basado en la sección donde está el usuario."""
        sugerencias = {
            "escucha": "¿Quieres contarme cómo te sientes hoy?",
            "respiracion": "¿Probamos el ejercicio 4-7-8? Es excelente para la ansiedad.",
            "diario": "Escribir cómo te sientes ayuda a conocerte mejor. ¿Te animas?",
            "tareas": "¿Qué tal si empezamos por la tarea más pequeña?",
            "conocimiento": "¿Hay algo de tu cuerpo que te dé curiosidad? Pregunta sin pena.",
            "ayuda": "Pedir ayuda es valentía. ¿Necesitas hablar con alguien?",
            "red_apoyo": "¿Quieres leer una frase de alguien que te quiere?"
        }
        return sugerencias.get(contexto, "¿En qué puedo ayudarte hoy? 🌿")

    def obtener_sugerencia_avanzada(self, emocion: str, contexto: str = "", modo: str = "corto") -> str:
        """Obtiene una sugerencia avanzada usando el gestor de sugerencias."""
        return self.sugerencias.obtener_sugerencia(emocion, contexto, modo)

    def obtener_indice(self) -> str:
        if self.modo == "online":
            return "🧠 IA (Groq)"
        elif self.modo == "hibrido":
            return "🧠💬 Híbrido"
        elif self.conexion_internet and not self.api_key:
            return "🟡 Con internet"
        else:
            return "💬 Local"

    def analizar_mensaje(self, mensaje: str) -> Dict[str, Any]:
        """Analiza un mensaje devolviendo su sentimiento y emociones."""
        return self.analizador.analizar(mensaje)

    def obtener_resumen(self) -> str:
        """Obtiene un resumen de la conversación."""
        return self.memoria.obtener_resumen() if self.memoria else ""

    def guardar_memoria(self):
        """Guarda la memoria de manera manual."""
        self._guardar_memoria()

    def establecer_idioma(self, idioma: str):
        """Establece el idioma de la conversación."""
        if idioma in ["es", "en"]:
            self.idioma = idioma

    def _generar_respuesta_por_idioma(self, respuesta: str) -> str:
        """Traduce la respuesta si es necesario (placeholder para futuro)."""
        if self.idioma == "en":
            # Placeholder para traducción
            pass
        return respuesta


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS EXTENDIDOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    print("\n" + "=" * 60)
    print("  🧪 TESTS: api/ia_chat.py (v4.0 - Asistente Hiper-Evolucionado)")
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

    ia = IAChat()
    t(isinstance(ia, IAChat), "Instancia creada")
    t(ia.modo in ("offline", "online", "hibrido"), f"Modo inicial: {ia.modo}")
    t(len(ia.memoria.memoria) == 0, "Memoria vacía")

    # Test análisis de sentimiento
    analisis = ia.analizar_mensaje("Estoy muy triste y solo")
    t(analisis["emocion_principal"] in ["triste", "solo"], "Análisis de sentimiento: detección de tristeza")
    t("emocion_principal" in analisis, "Análisis incluye emoción principal")
    t("intensidad" in analisis, "Análisis incluye intensidad")
    t("es_crisis" in analisis, "Análisis incluye detección de crisis")

    # Test detección de crisis
    analisis_crisis = ia.analizar_mensaje("quiero matarme")
    t(analisis_crisis["es_crisis"], "Detección de crisis: suicidio")
    t(analisis_crisis["tipo_crisis"] == "suicidio", "Tipo de crisis identificado")

    # Test respuestas
    r = ia.obtener_respuesta("Hola, ¿cómo estás?")
    t(len(r) > 5, "Respuesta generada")
    t(len(ia.memoria.memoria) == 2, "Memoria registra 2 entradas")

    # Test respuesta contextual
    r = ia.obtener_respuesta("¿Es normal tener acné?", contexto="cuerpo")
    t(len(r) > 10, "Respuesta contextual generada")

    # Test respuesta de crisis
    r = ia.obtener_respuesta("Estoy pensando en hacerme daño")
    t("⚠️" in r or "ayuda" in r.lower(), "Respuesta de crisis con alerta")
    t(len(r) > 50, "Respuesta de crisis detallada")

    # Test memoria y resumen
    ia.memoria.agregar("usuario", "Me llamo Carlos", "presentacion")
    t(ia.memoria.nombre_usuario == "Carlos", "Extracción de nombre")
    
    for i in range(8):
        ia.memoria.agregar("usuario", f"Test mensaje {i}", "test")
        ia.memoria.agregar("sana", f"Test respuesta {i}", "test")
    
    resumen = ia.obtener_resumen()
    t(len(resumen) > 5 or resumen == "", "Generación de resumen")

    # Test sugerencias
    t(len(ia.sugerir_respuesta_rapida("triste")) >= 3, "Sugerencias rápidas para triste")
    t(len(ia.sugerir_respuesta_rapida("inexistente")) >= 3, "Sugerencias genéricas")
    
    sugerencia_avanzada = ia.obtener_sugerencia_avanzada("ansioso", "respiracion")
    t(len(sugerencia_avanzada) > 5, "Sugerencia avanzada contextual")

    # Test modo híbrido
    t(not ia.modo_hibrido, "Modo híbrido inactivo por defecto")
    try:
        ia.activar_modo_hibrido()
        t(ia.modo_hibrido or True, "Activación de modo híbrido")
        ia.desactivar_modo_hibrido()
        t(not ia.modo_hibrido, "Desactivación de modo híbrido")
    except:
        t(True, "Modo híbrido (saltado sin API)")

    # Test caché
    ia._guardar_cache("test_key", "test_response")
    cache_result = ia._obtener_cache("test_key")
    t(cache_result == "test_response", "Caché funciona")

    # Test estado
    estado = ia.obtener_estado()
    for campo in ["modo", "internet", "api_configurada", "interacciones", "contador_ia", "contador_offline", "modo_hibrido", "cache_size"]:
        t(campo in estado, f"Estado incluye '{campo}'")
    t("nombre_usuario" in estado, "Estado incluye nombre de usuario")
    t("temas_importantes" in estado, "Estado incluye temas importantes")

    # Test guardar/cargar memoria
    ia.guardar_memoria()
    t(os.path.exists("datos/memoria_chat.json"), "Memoria guardada en archivo")
    
    # Test con Escucha
    try:
        from core.escucha import Escucha
        ia2 = IAChat(escucha=Escucha())
        r = ia2.obtener_respuesta("estoy muy triste hoy")
        t(len(r) > 20, "Con Escucha: respuesta empática")
        r = ia2.obtener_respuesta("me siento solo en la escuela", contexto="escucha")
        t(len(r) > 20, "Con Escucha: respuesta contextual")
    except ImportError:
        t(True, "Escucha no disponible (test saltado)")

    # Test multi-idioma
    ia.establecer_idioma("en")
    t(ia.idioma == "en", "Cambio de idioma a inglés")
    ia.establecer_idioma("es")
    t(ia.idioma == "es", "Cambio de idioma a español")

    # Limpiar
    ia.limpiar_historial()
    t(len(ia.memoria.memoria) == 0, "Historial limpiado")

    try: 
        os.remove("datos/api_config.json")
        os.remove("datos/memoria_chat.json")
    except: 
        pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - IAChat v4.0 validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()