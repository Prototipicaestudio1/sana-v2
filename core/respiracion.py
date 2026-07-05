"""
🌿 Sana - Módulo de Respiración Guiada Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Ejercicios de respiración científicamente respaldados para
calmar ansiedad, estrés, crisis y mejorar el bienestar general.
Diseñado como un salvavidas respiratorio para adolescentes.
7 ejercicios · Frases de acompañamiento · Recomendaciones
personalizadas · Visualización guiada · Modo crisis rápida.
═══════════════════════════════════════════════════════════════
"""

import time
import random


class Respiracion:
    """
    Motor de ejercicios respiratorios de Sana - El ancla en la tormenta.
    
    Técnicas basadas en:
    - Respiración diafragmática (médula espinal)
    - Coherencia cardíaca (Instituto HeartMath)
    - Mindfulness (Jon Kabat-Zinn)
    - Pranayama (yoga tradicional)
    - Técnicas de grounding para crisis de ansiedad
    
    Cada ejercicio está diseñado para un estado emocional específico
    y puede ser ejecutado con callbacks para integrarse con la UI.
    """

    # ═══════════════════════════════════════════════════════════
    # EJERCICIOS DISPONIBLES (7 ejercicios)
    # ═══════════════════════════════════════════════════════════

    EJERCICIOS = {
        "4-7-8": {
            "nombre": "Respiración 4-7-8",
            "descripcion": "Inhala 4 segundos, retén 7 segundos, exhala 8 segundos. "
                          "Esta técnica activa el sistema nervioso parasimpático, "
                          "reduciendo el ritmo cardíaco y la presión arterial.",
            "pasos": [
                ("Inhala profundamente por la nariz", 4),
                ("Sostén el aire suavemente", 7),
                ("Exhala todo el aire por la boca, haciendo un sonido suave como el viento", 8)
            ],
            "ciclos": 4,
            "beneficio": "Reduce la ansiedad en 2-3 minutos, ayuda a conciliar el sueño, "
                        "calma el sistema nervioso simpático. Usada por Navy SEALs para dormir.",
            "emocion_ideal": ["ansioso", "ansiosa", "insomnio", "crisis", "miedo"],
            "nivel": "intermedio",
            "visualizacion": "Imagina que cada inhalación es una ola que sube suavemente, "
                           "cada retención es la ola en su punto más alto, "
                           "y cada exhalación es la ola rompiendo en la orilla y llevándose la tensión."
        },
        "caja": {
            "nombre": "Respiración de Caja (Box Breathing)",
            "descripcion": "Inhala 4s, retén 4s, exhala 4s, retén 4s. "
                          "Forma un cuadrado perfecto con tu respiración. "
                          "Usada por fuerzas especiales para mantener la calma en combate.",
            "pasos": [
                ("Inhala contando mentalmente hasta 4", 4),
                ("Sostén el aire contando hasta 4", 4),
                ("Exhala lentamente contando hasta 4", 4),
                ("Mantén los pulmones vacíos contando hasta 4", 4)
            ],
            "ciclos": 4,
            "beneficio": "Mejora la concentración y la claridad mental, equilibra emociones intensas, "
                        "reduce el estrés agudo. Ideal antes de exámenes o presentaciones.",
            "emocion_ideal": ["estresado", "estresada", "enojado", "enojada", "disperso", "dispersa"],
            "nivel": "principiante",
            "visualizacion": "Dibuja un cuadrado en tu mente. Cada lado es una fase. "
                           "Al inhalar recorres el lado superior. Al retener, bajas por el derecho. "
                           "Al exhalar, recorres el inferior. Al retener vacío, subes por el izquierdo. "
                           "Un cuadrado perfecto de calma."
        },
        "5-5": {
            "nombre": "Respiración 5-5 (Coherencia Cardíaca)",
            "descripcion": "Inhala 5 segundos, exhala 5 segundos. "
                          "Simple, efectiva y discreta. Puedes hacerla en cualquier lugar, "
                          "incluso en clase o en el transporte público, sin que nadie lo note.",
            "pasos": [
                ("Inhala profunda y silenciosamente por la nariz", 5),
                ("Exhala suave y completamente por la nariz o boca", 5)
            ],
            "ciclos": 6,
            "beneficio": "Fácil de recordar incluso en crisis. Ideal para ansiedad en público, "
                        "antes de hablar en clase o cuando necesitas calmarte rápido y sin llamar la atención.",
            "emocion_ideal": ["crisis", "pánico", "agobia", "emergencia", "ya", "ahora"],
            "nivel": "principiante",
            "visualizacion": "Visualiza un péndulo que se balancea. Al inhalar va hacia la derecha, "
                           "al exhalar hacia la izquierda. Un ritmo constante, predecible, seguro."
        },
        "abdominal": {
            "nombre": "Respiración Abdominal (Diafragmática)",
            "descripcion": "Respiración profunda usando el diafragma, no el pecho. "
                          "Coloca una mano en el abdomen y otra en el pecho. "
                          "Solo debe moverse la mano del abdomen.",
            "pasos": [
                ("Infla el abdomen como un globo al inhalar lentamente por la nariz", 4),
                ("Desinfla el abdomen suavemente al exhalar por la boca", 6)
            ],
            "ciclos": 5,
            "beneficio": "Reduce la tensión muscular acumulada, mejora la oxigenación de la sangre, "
                        "activa el nervio vago (responsable de la relajación profunda). "
                        "Ideal para tensión física y estrés crónico.",
            "emocion_ideal": ["cansado", "cansada", "tenso", "tensa", "agotado", "agotada", "dolor"],
            "nivel": "principiante",
            "visualizacion": "Imagina que tu abdomen es un globo de luz cálida. "
                           "Al inhalar, el globo se expande con luz dorada. "
                           "Al exhalar, la luz se va por tus piernas, llevándose la tensión a la tierra."
        },
        "alterna": {
            "nombre": "Respiración Alterna (Nadi Shodhana)",
            "descripcion": "Tapando una fosa nasal alternadamente. "
                          "Técnica milenaria del yoga para equilibrar hemisferios cerebrales. "
                          "Usa el pulgar y el anular para tapar las fosas.",
            "pasos": [
                ("Tapa la fosa izquierda, inhala por la derecha", 4),
                ("Tapa la fosa derecha, exhala por la izquierda", 4),
                ("Inhala por la izquierda (misma fosa)", 4),
                ("Tapa la izquierda, exhala por la derecha", 4)
            ],
            "ciclos": 3,
            "beneficio": "Equilibra los hemisferios cerebrales, calma la mente dispersa, "
                        "mejora el enfoque y la claridad mental. Ideal para confusión o indecisión.",
            "emocion_ideal": ["confundido", "confundida", "disperso", "dispersa", "bloqueado", "bloqueada"],
            "nivel": "intermedio",
            "visualizacion": "Visualiza dos ríos de energía: uno dorado (derecha, energía solar, activa) "
                           "y uno plateado (izquierda, energía lunar, calmante). "
                           "Con cada ciclo, ambos ríos se encuentran y se equilibran en tu centro."
        },
        "suspiro": {
            "nombre": "Suspiro Fisiológico",
            "descripcion": "Dos inhalaciones cortas por la nariz seguidas de una exhalación larga por la boca. "
                          "Técnica descubierta por el neurocientífico Andrew Huberman (Stanford). "
                          "El alivio más rápido para el estrés agudo.",
            "pasos": [
                ("Primera inhalación corta por la nariz (llena los pulmones a medias)", 2),
                ("Segunda inhalación corta por la nariz (llena los pulmones completamente)", 2),
                ("Exhala todo el aire lentamente por la boca, como si suspiraras", 6)
            ],
            "ciclos": 3,
            "beneficio": "Restablece el patrón respiratorio en segundos. El suspiro fisiológico "
                        "reinicia los niveles de CO2 en sangre y calma el sistema nervioso "
                        "más rápido que cualquier otra técnica. Ideal para crisis repentinas.",
            "emocion_ideal": ["crisis", "pánico", "ataque", "urgente", "ya", "no puedo"],
            "nivel": "principiante",
            "visualizacion": "Imagina que estás inflando un globo en dos soplidos rápidos "
                           "y luego lo dejas desinflarse lentamente. Con cada ciclo, "
                           "el globo se lleva un poco de tu ansiedad."
        },
        "progresiva": {
            "nombre": "Respiración Progresiva 4-4-4-4",
            "descripcion": "Inhala 4s, retén 4s, exhala 4s, retén vacío 4s. "
                          "Similar a la respiración de caja pero enfocada en la relajación muscular. "
                          "En cada exhalación, suelta conscientemente un grupo muscular.",
            "pasos": [
                ("Inhala y tensa suavemente los hombros", 4),
                ("Retén el aire y mantén la tensión", 4),
                ("Exhala y suelta completamente los hombros, déjalos caer", 4),
                ("Descansa con los pulmones vacíos, siente el peso de tus hombros relajados", 4)
            ],
            "ciclos": 4,
            "beneficio": "Combina respiración con relajación muscular progresiva. "
                        "Ideal para tensión acumulada en cuello, hombros y espalda. "
                        "Ayuda a tomar conciencia de las zonas de tensión corporal.",
            "emocion_ideal": ["tenso", "tensa", "contracturado", "contracturada", "rígido", "rígida"],
            "nivel": "principiante",
            "visualizacion": "Visualiza tus músculos como esponjas. Al inhalar, las esponjas se llenan de agua tibia. "
                           "Al exhalar, escurres el agua y con ella se va toda la tensión acumulada."
        }
    }

    # ═══════════════════════════════════════════════════════════
    # FRASES DE ACOMPAÑAMIENTO
    # ═══════════════════════════════════════════════════════════

    FRASES_INICIO = [
        "Busca un lugar cómodo, donde puedas estar tranquilo/a por unos minutos. "
        "Si quieres, cierra los ojos. Si no, fija la mirada en un punto. Vamos a respirar juntos.",
        
        "Si puedes, cierra los ojos suavemente. Si estás en un lugar público, solo baja la mirada. "
        "Nadie va a notar que estás haciendo un ejercicio de respiración. Es tu momento, solo tuyo.",
        
        "Pon una mano en tu pecho y otra en tu abdomen. ¿Sientes cómo respiras ahora? "
        "Sin cambiar nada, solo observa. Ahora vamos a hacer esa respiración más profunda y consciente.",
        
        "No importa si tu mente se distrae. Es normal. Cada vez que se vaya, tráela de vuelta "
        "a tu respiración sin juzgarte. Como quien entrena un músculo. La atención se entrena así.",
        
        "Vamos a hacer una pausa juntos. Solo tú y tu respiración. Todo lo demás puede esperar "
        "unos minutos. El mundo no se va a acabar porque te tomes este tiempo para ti.",
        
        "Si vienen pensamientos, déjalos pasar como nubes en el cielo. No te aferres a ellos, "
        "no los empujes. Solo observa cómo vienen y se van, mientras tu respiración sigue su ritmo.",
        
        "Date permiso para estar aquí, ahora. No tienes que hacer nada más. No tienes que ser productivo/a. "
        "Solo respirar. Eso ya es suficiente. Eso ya es cuidarte.",
        
        "Suelta los hombros. Afloja la mandíbula. Destensa el entrecejo. "
        "No te habías dado cuenta de que estabas tenso/a, ¿verdad? Ahora respira."
    ]

    FRASES_CIERRE = [
        "Bien hecho. Tómate un momento para notar cómo te sientes ahora. "
        "¿Hay alguna diferencia en tu cuerpo, en tu mente, en tu estado de ánimo?",
        
        "Excelente trabajo. Respirar es un superpoder que siempre llevas contigo. "
        "Nadie puede quitártelo. Úsalo cuando lo necesites.",
        
        "Muy bien. ¿Notas cómo tu corazón late más tranquilo? ¿Cómo tus pensamientos van más lentos? "
        "Eso es tu sistema nervioso diciéndote 'gracias'.",
        
        "Terminamos este ejercicio, pero puedes volver a él cuando quieras. "
        "Tu respiración siempre está ahí, esperándote, como una amiga fiel.",
        
        "Buen trabajo. Recuerda: no necesitas una crisis para respirar. "
        "Puedes hacerlo en cualquier momento, en cualquier lugar. Es tu herramienta gratuita y portátil.",
        
        "¿Te sientes un poco más en calma? Aunque sea un poquito, ya es un logro. "
        "Cada respiración consciente es un acto de amor propio.",
        
        "Quédate un momento con esta sensación. Sea cual sea. No la juzgues. "
        "Solo obsérvala. Así se construye la conciencia emocional.",
        
        "Increíble. Acabas de dedicarte unos minutos a ti mismo/a. "
        "En un mundo que te exige todo el tiempo, eso es revolucionario. Sana está orgullosa de ti."
    ]

    MENSAJES_PAUSA = [
        "Siente el aire entrando por tu nariz, fresco y limpio, llenando tus pulmones de calma.",
        "Nota cómo se expande tu pecho, cómo tus costillas se abren como un abanico.",
        "Deja ir la tensión con cada exhalación. Imagina que es humo gris que sale de ti.",
        "Cada exhalación te relaja un poco más. Como si soltaras un peso que no sabías que cargabas.",
        "Estás aquí, estás a salvo. En este momento, en esta respiración, no hay peligro.",
        "Tus músculos se aflojan. Tus pensamientos se aquietan. Solo existe este momento.",
        "Si vienen preocupaciones, déjalas pasar. Siempre puedes volver a preocuparte después si quieres.",
        "Eres más que tus pensamientos. Eres el cielo, no las nubes. Las nubes pasan, el cielo permanece."
    ]

    # ═══════════════════════════════════════════════════════════
    # MENSAJES PARA MODO CRISIS (acceso rápido)
    # ═══════════════════════════════════════════════════════════

    MENSAJES_CRISIS_RAPIDA = [
        "🚨 CRISIS DE ANSIEDAD - Respiramos juntos YA:\n"
        "1. Inhala 2 veces cortas por la nariz (sniff, sniff)\n"
        "2. Exhala largo por la boca (como si soplaras una vela)\n"
        "3. Repite 3 veces. Estás a salvo. Esto va a pasar.",

        "🚨 CALMA INMEDIATA:\n"
        "Mira a tu alrededor y nombra en voz alta o mentalmente:\n"
        "• 5 cosas que puedas VER\n"
        "• 4 cosas que puedas TOCAR\n"
        "• 3 cosas que puedas ESCUCHAR\n"
        "• 2 cosas que puedas OLER\n"
        "• 1 cosa que puedas SABOREAR\n"
        "Luego respira profundo. Ya pasó lo peor.",

        "🚨 ATAQUE DE PÁNICO - Grounding:\n"
        "Agarra algo frío (agua, metal, pared). Siéntelo.\n"
        "Golpea suavemente tus piernas con las palmas: izquierda, derecha, izquierda, derecha.\n"
        "Respira conmigo: inhala 4s, exhala 6s. Repite hasta que baje.\n"
        "No te vas a morir. Es tu cuerpo protegiéndote. Ya está pasando."
    ]

    def __init__(self):
        self.ejercicio_actual = None
        self.ciclo_actual = 0
        self.en_progreso = False
        self.historial_ejercicios = []
        self.contador_total = 0

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS PRINCIPALES
    # ═══════════════════════════════════════════════════════════

    def obtener_ejercicios(self) -> list:
        """
        Retorna lista de todos los ejercicios disponibles.
        
        Returns:
            Lista de tuplas (nombre, descripcion)
        """
        return [(ej["nombre"], ej["descripcion"]) for ej in self.EJERCICIOS.values()]

    def obtener_ejercicio(self, clave: str) -> dict:
        """
        Obtiene los detalles completos de un ejercicio.
        
        Args:
            clave: Identificador del ejercicio.
        
        Returns:
            Diccionario con datos del ejercicio o None.
        """
        return self.EJERCICIOS.get(clave, None)

    def obtener_frase_inicio(self) -> str:
        """Retorna una frase de inicio aleatoria para acompañar el ejercicio."""
        return random.choice(self.FRASES_INICIO)

    def obtener_frase_cierre(self) -> str:
        """Retorna una frase de cierre aleatoria para finalizar el ejercicio."""
        return random.choice(self.FRASES_CIERRE)

    def obtener_mensaje_pausa(self) -> str:
        """Retorna un mensaje de acompañamiento durante las pausas de respiración."""
        return random.choice(self.MENSAJES_PAUSA)

    def obtener_mensaje_crisis(self) -> str:
        """Retorna un mensaje de intervención rápida para crisis de ansiedad."""
        return random.choice(self.MENSAJES_CRISIS_RAPIDA)

    def ejecutar_ciclo(self, clave: str, callback_inicio=None, callback_paso=None, 
                       callback_fin=None, callback_pausa=None) -> bool:
        """
        Ejecuta un ciclo completo de respiración con callbacks para la UI.
        
        Args:
            clave: Identificador del ejercicio.
            callback_inicio: Función(nombre_ejercicio) al iniciar.
            callback_paso: Función(texto_paso, segundos) en cada paso.
            callback_fin: Función(frase_cierre) al finalizar.
            callback_pausa: Función(mensaje) durante las pausas entre pasos.
        
        Returns:
            True si se ejecutó correctamente.
        """
        ejercicio = self.EJERCICIOS.get(clave)
        if not ejercicio:
            return False

        self.ejercicio_actual = clave
        self.en_progreso = True
        self.historial_ejercicios.append(clave)
        self.contador_total += 1

        if callback_inicio:
            callback_inicio(ejercicio["nombre"])

        for ciclo in range(ejercicio["ciclos"]):
            self.ciclo_actual = ciclo + 1
            for texto, segundos in ejercicio["pasos"]:
                if callback_paso:
                    callback_paso(texto, segundos)
                time.sleep(0.1)  # En producción: time.sleep(segundos)
            
            # Mensaje de pausa entre ciclos
            if callback_pausa and ciclo < ejercicio["ciclos"] - 1:
                callback_pausa(self.obtener_mensaje_pausa())

        self.en_progreso = False
        if callback_fin:
            callback_fin(self.obtener_frase_cierre())

        return True

    def obtener_recomendacion(self, estado: str) -> str:
        """
        Recomienda el ejercicio más adecuado según el estado emocional.
        Ahora con 7 ejercicios y recomendaciones por palabra clave.
        
        Args:
            estado: Emoción o estado del usuario.
        
        Returns:
            Clave del ejercicio recomendado.
        """
        estado = estado.lower()
        
        # Mapeo ampliado de estados a ejercicios
        recomendaciones = {
            # Ansiedad y crisis
            "ansioso": "4-7-8", "ansiosa": "4-7-8", "ansiedad": "4-7-8",
            "crisis": "suspiro", "pánico": "suspiro", "ataque": "suspiro",
            "miedo": "4-7-8", "asustado": "4-7-8", "asustada": "4-7-8",
            "nervioso": "caja", "nerviosa": "caja",
            
            # Estrés y presión
            "estresado": "caja", "estresada": "caja", "estrés": "caja",
            "presión": "caja", "examen": "caja", "presentación": "caja",
            "entrevista": "caja", "prueba": "caja",
            
            # Sueño
            "insomnio": "4-7-8", "dormir": "4-7-8", "no duermo": "4-7-8",
            "desvelado": "4-7-8", "desvelada": "4-7-8",
            
            # Tensión física
            "tenso": "progresiva", "tensa": "progresiva", "contracturado": "progresiva",
            "dolor": "abdominal", "cuerpo": "progresiva", "rígido": "progresiva",
            
            # Cansancio
            "cansado": "abdominal", "cansada": "abdominal",
            "agotado": "abdominal", "agotada": "abdominal",
            "fatiga": "abdominal", "sin energía": "abdominal",
            
            # Confusión y bloqueo
            "confundido": "alterna", "confundida": "alterna",
            "disperso": "alterna", "dispersa": "alterna",
            "bloqueado": "alterna", "bloqueada": "alterna",
            
            # Enojo
            "enojado": "caja", "enojada": "caja", "furioso": "caja",
            "bronca": "caja", "ira": "caja",
            
            # Tristeza
            "triste": "abdominal", "bajón": "abdominal",
            "deprimido": "abdominal", "deprimida": "abdominal",
            
            # Emergencia
            "urgente": "suspiro", "ya": "suspiro", "ahora": "suspiro",
            "emergencia": "suspiro", "no puedo más": "suspiro",
        }
        
        # Buscar coincidencia exacta primero
        if estado in recomendaciones:
            return recomendaciones[estado]
        
        # Buscar coincidencia parcial
        for clave, ejercicio in recomendaciones.items():
            if clave in estado or estado in clave:
                return ejercicio
        
        # Por defecto: 5-5 que es la más universal
        return "5-5"

    def obtener_recomendacion_razonada(self, estado: str) -> str:
        """
        Retorna una recomendación con explicación amigable.
        
        Args:
            estado: Emoción del usuario.
        
        Returns:
            Texto explicando por qué se recomienda ese ejercicio.
        """
        clave = self.obtener_recomendacion(estado)
        ejercicio = self.EJERCICIOS[clave]
        
        explicaciones = {
            "4-7-8": "Te recomiendo la respiración 4-7-8 porque es excelente para calmar "
                    "la ansiedad y ayudar a dormir. Es como un botón de 'apagado' para tu sistema nervioso.",
            "caja": "Te recomiendo la respiración de caja porque necesitas claridad mental y enfoque. "
                   "Es la que usan los Navy SEALs para mantener la calma bajo presión.",
            "5-5": "Te recomiendo la respiración 5-5 porque es simple, discreta y efectiva. "
                  "Puedes hacerla en cualquier lugar sin que nadie se dé cuenta.",
            "abdominal": "Te recomiendo la respiración abdominal porque tu cuerpo necesita relajación profunda. "
                        "Es como un masaje interno para tus órganos.",
            "alterna": "Te recomiendo la respiración alterna porque necesitas equilibrar tu mente. "
                      "Es como resetear tu cerebro cuando tienes mil pensamientos a la vez.",
            "suspiro": "Te recomiendo el suspiro fisiológico porque necesitas alivio rápido. "
                      "Es la técnica más rápida que existe para bajar el estrés en segundos.",
            "progresiva": "Te recomiendo la respiración progresiva porque tienes tensión acumulada "
                         "en el cuerpo. Vamos a soltar cada músculo, uno por uno."
        }
        
        return f"{explicaciones.get(clave, '')}\n\n{ejercicio['descripcion']}"

    def formato_guiado(self, clave: str) -> str:
        """
        Retorna el texto completo del ejercicio para mostrar en pantalla.
        Incluye visualización guiada.
        """
        ejercicio = self.EJERCICIOS.get(clave)
        if not ejercicio:
            return "Ejercicio no encontrado."

        texto = f"🌬️ {ejercicio['nombre']}\n"
        texto += "─" * 40 + "\n\n"
        texto += f"{ejercicio['descripcion']}\n\n"
        texto += f"💡 Beneficio: {ejercicio['beneficio']}\n\n"
        texto += f"🎯 Ideal para: {', '.join(ejercicio['emocion_ideal'][:4])}\n"
        texto += f"📊 Nivel: {ejercicio['nivel'].capitalize()}\n\n"
        texto += "📋 Pasos:\n"
        for i, (paso, seg) in enumerate(ejercicio["pasos"], 1):
            texto += f"  {i}. {paso} ({seg}s)\n"
        texto += f"\n🔄 Repetir {ejercicio['ciclos']} veces.\n\n"
        texto += f"🌈 Visualización:\n{ejercicio['visualizacion']}"

        return texto

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas de uso de ejercicios."""
        from collections import Counter
        conteo = Counter(self.historial_ejercicios)
        return {
            "total_ejercicios": self.contador_total,
            "ejercicio_mas_usado": conteo.most_common(1)[0][0] if conteo else "ninguno",
            "historial": dict(conteo)
        }

    def obtener_todos_nombres(self) -> list:
        """Retorna lista con los nombres de todos los ejercicios."""
        return [ej["nombre"] for ej in self.EJERCICIOS.values()]

    def obtener_por_nivel(self, nivel: str) -> list:
        """
        Filtra ejercicios por nivel.
        
        Args:
            nivel: 'principiante' o 'intermedio'
        
        Returns:
            Lista de tuplas (nombre, descripcion)
        """
        return [(ej["nombre"], ej["descripcion"]) 
                for ej in self.EJERCICIOS.values() 
                if ej["nivel"] == nivel]

    def obtener_por_emocion(self, emocion: str) -> list:
        """
        Busca ejercicios recomendados para una emoción.
        
        Args:
            emocion: Emoción a buscar.
        
        Returns:
            Lista de nombres de ejercicios.
        """
        emocion = emocion.lower()
        resultados = []
        for clave, ej in self.EJERCICIOS.items():
            if any(emocion in e for e in ej["emocion_ideal"]):
                resultados.append(ej["nombre"])
        return resultados if resultados else [self.EJERCICIOS["5-5"]["nombre"]]


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Respiración v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: core/respiracion.py (v3.0 - Hiper-Evolución)")
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

    r = Respiracion()

    # Básicos
    t(isinstance(r, Respiracion), "Instancia creada")
    t(r.ejercicio_actual is None, "Sin ejercicio activo")
    t(not r.en_progreso, "No está en progreso")
    t(r.contador_total == 0, "Contador en 0")

    # Ejercicios
    ejercicios = r.obtener_ejercicios()
    t(len(ejercicios) >= 7, f"{len(ejercicios)} ejercicios (mín. 7)")
    t(isinstance(ejercicios[0], tuple), "Ejercicios son tuplas")
    t(len(ejercicios[0]) == 2, "Tupla tiene 2 elementos")

    # Ejercicio específico
    ej = r.obtener_ejercicio("suspiro")
    t(ej is not None, "Nuevo ejercicio 'suspiro' existe")
    ej = r.obtener_ejercicio("progresiva")
    t(ej is not None, "Nuevo ejercicio 'progresiva' existe")
    t(r.obtener_ejercicio("4-7-8")["ciclos"] == 4, "4-7-8: 4 ciclos")
    t(r.obtener_ejercicio("noexiste") is None, "Inválido retorna None")

    # Frases
    t(len(r.obtener_frase_inicio()) > 15, "Frase inicio sustancial")
    t(len(r.obtener_frase_cierre()) > 15, "Frase cierre sustancial")
    t(len(r.obtener_mensaje_pausa()) > 10, "Mensaje pausa sustancial")
    t(len(r.obtener_mensaje_crisis()) > 20, "Mensaje crisis sustancial")

    # Recomendaciones
    t(r.obtener_recomendacion("ansioso") == "4-7-8", "Ansiedad → 4-7-8")
    t(r.obtener_recomendacion("crisis") == "suspiro", "Crisis → suspiro")
    t(r.obtener_recomendacion("estresado") == "caja", "Estrés → caja")
    t(r.obtener_recomendacion("confundido") == "alterna", "Confusión → alterna")
    t(r.obtener_recomendacion("cansado") == "abdominal", "Cansancio → abdominal")
    t(r.obtener_recomendacion("tenso") == "progresiva", "Tensión → progresiva")
    t(r.obtener_recomendacion("alegre") == "5-5", "No mapeado → 5-5")

    # Recomendación razonada
    razon = r.obtener_recomendacion_razonada("ansioso")
    t(len(razon) > 50, "Recomendación razonada sustancial")
    t("4-7-8" in razon or "respiración" in razon.lower(), "Contiene nombre del ejercicio")

    # Formato guiado
    guia = r.formato_guiado("caja")
    t("Respiración de Caja" in guia, "Formato incluye nombre")
    t("Beneficio:" in guia, "Formato incluye beneficio")
    t("Visualización:" in guia, "Formato incluye visualización")

    # Ejecutar ciclo
    eventos = []
    r.ejecutar_ciclo("5-5",
        callback_inicio=lambda n: eventos.append(f"inicio:{n}"),
        callback_paso=lambda t, s: eventos.append(f"paso:{t}"),
        callback_fin=lambda f: eventos.append(f"fin:{f}"))
    t(len(eventos) > 0, "Eventos registrados")
    t(any("inicio:" in e for e in eventos), "Evento inicio")
    t(any("fin:" in e for e in eventos), "Evento fin")

    # Estadísticas
    stats = r.obtener_estadisticas()
    t(stats["total_ejercicios"] >= 1, "Estadísticas: total registrado")
    t("ejercicio_mas_usado" in stats, "Estadísticas: ejercicio más usado")

    # Todos los nombres
    nombres = r.obtener_todos_nombres()
    t(len(nombres) == 7, "7 nombres de ejercicios")

    # Por nivel
    principiantes = r.obtener_por_nivel("principiante")
    t(len(principiantes) >= 3, f"{len(principiantes)} ejercicios principiantes")

    # Por emoción
    por_emocion = r.obtener_por_emocion("ansioso")
    t(len(por_emocion) >= 1, "Ejercicios para ansiedad encontrados")

    # Datos completos
    for clave, ej in r.EJERCICIOS.items():
        for campo in ["nombre", "descripcion", "pasos", "ciclos", "beneficio", "emocion_ideal", "nivel", "visualizacion"]:
            t(campo in ej, f"'{clave}' tiene campo '{campo}'")

    # Variedad
    frases = [r.obtener_frase_inicio() for _ in range(15)]
    t(len(set(frases)) >= 3, f"Variedad frases inicio: {len(set(frases))}/15")

    total = p_tests + f_tests
    print(f"\n  📊 {p_tests}/{total} tests pasados")
    if f_tests == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Respiración v3.0 validada\n")
    else:
        print(f"  ⚠️  {f_tests} test(s) fallaron\n")
    return f_tests == 0


if __name__ == "__main__":
    ejecutar_tests()