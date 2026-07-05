"""
🌿 Sana - Módulo de Conocimiento Corporal Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Información científica, inclusiva y empática sobre los cambios
fisiológicos de la adolescencia. 30+ FAQs organizadas por
categorías, con lenguaje claro, sin tabúes y con perspectiva
de género. Diseñado para que ningún adolescente se sienta
solo/a en los cambios de su cuerpo.
═══════════════════════════════════════════════════════════════
"""

import random
from collections import Counter


class Conocimiento:
    """
    Enciclopedia corporal empática de Sana.
    
    Responde preguntas sobre cambios fisiológicos con:
    - Rigor científico adaptado a lenguaje adolescente
    - Perspectiva de género inclusiva (personas con vulva/pene)
    - Metáforas y analogías para facilitar la comprensión
    - Validación emocional en cada respuesta
    - Derivación a profesionales cuando corresponde
    """

    # ═══════════════════════════════════════════════════════════
    # FAQS (31 preguntas frecuentes)
    # ═══════════════════════════════════════════════════════════

    FAQS = [
        # ─── CRECIMIENTO ───
        (
            "¿Es normal que me duela el cuerpo al crecer?",
            "Sí, es completamente normal. Se llaman 'dolores de crecimiento' y suelen aparecer en piernas y brazos, "
            "especialmente por la noche. Ocurren porque tus huesos y músculos están estirándose rápido, como cuando "
            "estiras una liga. Si el dolor es muy intenso, te despierta todas las noches o no desaparece con un masaje suave, "
            "consulta con un médico para descartar otras causas."
        ),
        (
            "¿Por qué unos crecen más rápido que otros?",
            "Cada cuerpo tiene su propio ritmo, como una orquesta donde cada instrumento entra en momentos distintos. "
            "Depende de tu genética (tus papás), tu alimentación, tus hormonas y hasta de cuánto duermes. "
            "No hay un 'cronograma' único. Algunos dan el estirón a los 11, otros a los 15. Todos los ritmos son normales "
            "y llegarás a tu altura final a tu tiempo."
        ),
        (
            "¿Hasta qué edad se crece?",
            "En general, las personas con vulva suelen dejar de crecer alrededor de los 16-18 años, "
            "y las personas con pene alrededor de los 18-21. Pero ojo: esto es un promedio. "
            "Algunas personas crecen hasta los 25. La altura final depende de muchos factores y todos son válidos."
        ),
        (
            "¿Es normal que me duelan las articulaciones?",
            "Sí, durante el estirón puberal las articulaciones pueden doler porque los huesos crecen más rápido "
            "que los músculos y tendones. Es como si el cuerpo estuviera 'descoordinado' por un tiempo. "
            "Estiramientos suaves, buena hidratación y calcio ayudan. Si el dolor es persistente, consulta."
        ),
        (
            "¿Por qué tengo estrías si soy joven?",
            "Las estrías son completamente normales en la adolescencia. Aparecen cuando la piel se estira rápido "
            "durante el crecimiento y no tiene tiempo de adaptarse. Son como las marcas de un mapa: muestran por dónde "
            "has crecido. Con el tiempo se aclaran. Hidratar la piel ayuda a prevenirlas."
        ),

        # ─── PIEL Y VELLO ───
        (
            "¿Por qué me salen granitos? ¿Es normal?",
            "Sí, es muy normal. Se llama acné y afecta al 85% de los adolescentes. Aparece porque tus hormonas "
            "(especialmente la testosterona, que todos tienen en distintas cantidades) estimulan las glándulas de la piel "
            "produciendo más grasa. Lavar tu cara con agua tibia y un limpiador suave dos veces al día ayuda. "
            "No te revientes los granitos: eso deja marcas. Si es muy severo, un dermatólogo puede ayudarte muchísimo."
        ),
        (
            "¿Es normal que me salga vello en partes nuevas?",
            "Totalmente normal. Durante la pubertad, el vello aparece en axilas, zona púbica, piernas, y a veces "
            "en pecho, espalda, glúteos o cara. La cantidad y distribución depende de tu genética y tus hormonas. "
            "Hay personas con mucho vello, otras con poco. Todo es normal. Si te incomoda, hay formas seguras de removerlo."
        ),
        (
            "¿Por qué sudo más ahora? ¿Huele diferente?",
            "Tus glándulas sudoríparas se activan con las hormonas de la pubertad. El olor corporal aparece porque "
            "las bacterias naturales de tu piel descomponen el sudor. No es suciedad, es biología. "
            "Usar desodorante (en roll-on, spray o crema), ducharte a diario y usar ropa de algodón ayuda. "
            "Evita los desodorantes con alcohol si tienes piel sensible."
        ),
        (
            "¿Qué es la caspa y por qué me sale?",
            "La caspa es la descamación del cuero cabelludo. En la adolescencia puede aumentar porque las hormonas "
            "estimulan la producción de grasa en el cuero cabelludo. No es peligrosa ni contagiosa. "
            "Un shampoo anticaspa suave suele resolverlo. Si persiste, un dermatólogo puede orientarte."
        ),

        # ─── CAMBIOS EN PERSONAS CON VULVA ───
        (
            "¿Qué es la menstruación y cuándo empieza?",
            "La menstruación (o regla) es el desprendimiento del endometrio, la capa interna del útero que se prepara "
            "cada mes por si hay embarazo. Si no lo hay, se desprende y sale por la vagina. Suele comenzar entre los 9 y 16 años. "
            "Los primeros ciclos pueden ser irregulares (un mes sí, otro no) y eso es normal mientras el cuerpo se regula. "
            "Dura entre 3 y 7 días. Puedes usar toallas, tampones, copa menstrual, ropa interior absorbente: tú eliges."
        ),
        (
            "¿Es normal que me duela mucho la regla?",
            "Algo de molestia o cólicos leves es normal. Pero si el dolor es tan intenso que no puedes ir a la escuela "
            "o hacer tu vida normal, NO es normal y merece atención médica. Se llama dismenorrea y tiene tratamiento. "
            "No tienes que 'aguantarte'. Consulta con un ginecólogo o médico general."
        ),
        (
            "¿Es normal que me duela el pecho al crecer?",
            "Sí. El desarrollo mamario puede causar sensibilidad, molestias o incluso bultitos temporales. "
            "Un seno puede crecer más rápido que el otro al principio (luego se emparejan). "
            "Usar un sostén cómodo ayuda. Si sientes bultos duros que no cambian, consulta."
        ),
        (
            "¿Qué es el flujo vaginal? ¿Es normal?",
            "Sí, es normal y saludable. Es un líquido blanquecino o transparente que tu vagina produce para limpiarse "
            "y protegerse de infecciones. Cambia durante el ciclo: más abundante y claro en ovulación, más espeso antes de la regla. "
            "Si tiene mal olor fuerte, color verdoso/amarillento, textura como requesón o causa picazón, consulta a un médico."
        ),
        (
            "¿Cómo sé si mi primera regla está cerca?",
            "Tu cuerpo te da pistas: puede aparecer flujo vaginal blanquecino unos meses antes, "
            "tus senos empiezan a desarrollarse, puede salir vello púbico. La mayoría tiene su primera regla "
            "unos 2 años después de que empiezan a crecer los senos. No hay una edad 'correcta', cada cuerpo es diferente."
        ),

        # ─── CAMBIOS EN PERSONAS CON PENE ───
        (
            "¿Es normal tener erecciones sin razón?",
            "Sí, completamente. Durante la pubertad, las hormonas (testosterona) causan erecciones espontáneas "
            "incluso sin ningún estímulo sexual. También son normales al despertar (erecciones matutinas). "
            "Es el cuerpo 'practicando' y ajustándose a nuevos niveles hormonales. Puede ser incómodo en público, "
            "pero suele pasar desapercibido. Ponte una mochila o chaqueta en el regazo si te preocupa."
        ),
        (
            "¿Qué son los sueños húmedos? ¿Les pasa a todos?",
            "Son eyaculaciones involuntarias durante el sueño. Son normales y comunes en la pubertad, aunque no a todos "
            "les ocurren. Indican que tu sistema reproductor está funcionando correctamente. "
            "No son algo de qué avergonzarse. Si te pasan, es señal de que tu cuerpo está sano."
        ),
        (
            "¿Por qué me cambia la voz? ¿Cuándo se estabiliza?",
            "La voz cambia porque tu laringe (la 'caja de la voz') crece y tus cuerdas vocales se alargan y engrosan "
            "por acción de la testosterona. Durante la transición puede haber 'gallos' o quiebres. "
            "Es temporal y suele estabilizarse hacia los 17-19 años. ¡Paciencia! Tu voz está encontrando su nuevo tono."
        ),
        (
            "¿Es normal que un testículo esté más bajo que el otro?",
            "Sí, totalmente normal. La mayoría de las personas con pene tienen un testículo ligeramente más bajo "
            "que el otro (generalmente el izquierdo). Esto ayuda a que no choquen entre sí al caminar. "
            "Si notas un bulto, dolor o cambio repentino de tamaño, consulta con un médico."
        ),
        (
            "¿Qué es el frenillo y por qué a veces molesta?",
            "El frenillo es una pequeña banda de piel que une el prepucio con el glande. En algunos adolescentes "
            "puede ser corto y causar molestias durante las erecciones. Se llama frenillo corto y tiene solución "
            "médica sencilla. No es algo de qué avergonzarse. Consulta con un urólogo si te molesta."
        ),

        # ─── EMOCIONES Y CEREBRO ───
        (
            "¿Por qué me siento más irritable o emocional?",
            "Tu cerebro está en plena remodelación durante la adolescencia. Es como una obra en construcción: "
            "hay andamios, ruido y desorden. Las hormonas afectan los neurotransmisores que regulan el ánimo. "
            "Además, la amígdala (centro emocional) está más activa que la corteza prefrontal (control de impulsos). "
            "Por eso sientes todo con más intensidad. Con el tiempo tu cerebro termina su 'remodelación' y se equilibra."
        ),
        (
            "¿Es normal querer estar solo/a a veces?",
            "Sí, completamente. La adolescencia es una etapa de construir tu identidad, y eso a veces requiere "
            "espacio propio para pensar, escucharte, descubrirte. Alternar entre querer compañía y soledad es saludable. "
            "Si el aislamiento es constante y te causa malestar profundo, ahí conviene hablarlo con alguien."
        ),
        (
            "¿Por qué me siento diferente a los demás?",
            "Porque eres único/a. Y eso no es malo, es maravilloso. La adolescencia es justo el momento en que "
            "descubrimos quiénes somos realmente, y eso a veces nos hace sentir 'diferentes'. "
            "La mayoría de tus compañeros sienten exactamente lo mismo, aunque no lo digan. "
            "Si tu diferencia te causa sufrimiento, habla con un adulto de confianza."
        ),
        (
            "¿Por qué a veces estoy feliz y de repente triste?",
            "Se llama labilidad emocional y es muy común en la adolescencia. Las hormonas fluctúan mucho y tu cerebro "
            "está aprendiendo a regularlas. Es como un termostato que todavía no está bien calibrado: "
            "a veces hace frío, a veces calor. Con el tiempo se estabiliza. Mientras tanto, sé amable contigo mismo/a."
        ),

        # ─── SUEÑO Y ENERGÍA ───
        (
            "¿Por qué tengo tanto sueño todo el tiempo?",
            "Los adolescentes necesitan entre 8 y 10 horas de sueño diarias (más que los adultos). "
            "Tu ritmo circadiano cambia en la pubertad, haciendo que te dé sueño más tarde y necesites dormir más. "
            "Además, crecer consume muchísima energía. Dormir bien mejora tu ánimo, tus notas y tu salud. "
            "Intenta mantener horarios regulares y evita pantallas una hora antes de dormir."
        ),
        (
            "¿Por qué me cuesta tanto despertarme?",
            "No es flojera, es biología. Durante la adolescencia, la melatonina (la hormona del sueño) se libera "
            "más tarde en la noche, por eso te duermes tarde. Y por la mañana, tu cuerpo todavía la tiene alta. "
            "Es como si vivieras en un huso horario diferente al de los adultos. La buena noticia: es temporal."
        ),
        (
            "¿Es normal tener insomnio a mi edad?",
            "Puede pasar. El estrés escolar, las preocupaciones, las redes sociales y los cambios hormonales "
            "pueden afectar tu sueño. Si te pasa ocasionalmente, no te preocupes. Si es frecuente, intenta: "
            "1) Apagar pantallas 1h antes, 2) Hacer ejercicio durante el día, 3) Tener un horario fijo. "
            "Si el insomnio persiste más de un mes, consulta con un médico."
        ),

        # ─── DIVERSIDAD CORPORAL Y AUTOESTIMA ───
        (
            "¿Es normal compararme con otros cuerpos?",
            "Es muy común, pero también muy dañino. Los cuerpos que ves en redes sociales y series tienen filtros, "
            "edición, maquillaje profesional y a veces cirugías. No son 'reales'. Hay infinita diversidad: "
            "alturas, pesos, formas, colores, tamaños. Tu cuerpo está en plena transición y es único. "
            "Enfócate en lo que tu cuerpo puede HACER (bailar, correr, abrazar, reír) más que en cómo se ve."
        ),
        (
            "¿Por qué no me gusta mi cuerpo?",
            "Es muy frecuente en la adolescencia. Tu cuerpo está cambiando tan rápido que a veces no te reconoces. "
            "Los estándares de belleza irreales de las redes sociales tampoco ayudan. "
            "La autoaceptación es un proceso. Empieza por agradecer a tu cuerpo por lo que te permite hacer. "
            "Si la insatisfacción es muy profunda, hablar con un terapeuta puede ayudar muchísimo con la autoestima."
        ),
        (
            "¿Es normal tener estrías, celulitis o imperfecciones?",
            "No solo es normal, es universal. Las estrías las tiene casi todo el mundo (incluidos modelos y famosos). "
            "La celulitis es simplemente la forma en que la grasa se distribuye bajo la piel y afecta al 90% de las mujeres. "
            "Las marcas en la piel son características humanas, todas las pieles las tienen. "
            "Las redes sociales te hacen creer que existe la piel perfecta, pero es un mito."
        ),

        # ─── ALIMENTACIÓN Y EJERCICIO ───
        (
            "¿Por qué tengo más hambre que antes?",
            "Tu cuerpo está construyendo huesos, músculos, órganos y tejidos nuevos. ¡Es una obra en construcción! "
            "Eso requiere mucha energía. Escucha a tu cuerpo: come cuando tengas hambre, elige alimentos nutritivos "
            "y no te castigues por comer. Necesitas más calorías ahora que cuando eras niño/a. Es normal."
        ),
        (
            "¿Debo hacer dieta para tener el cuerpo que quiero?",
            "A tu edad, las dietas restrictivas pueden ser peligrosas. Tu cuerpo necesita nutrientes para crecer. "
            "En lugar de 'dieta', piensa en 'alimentación saludable': frutas, verduras, proteínas, cereales integrales. "
            "Si te preocupa tu peso, consulta con un médico o nutricionista especializado en adolescentes. "
            "Nunca hagas dietas de internet. Tu salud es primero."
        ),
    ]

    # ═══════════════════════════════════════════════════════════
    # CATEGORÍAS
    # ═══════════════════════════════════════════════════════════

    CATEGORIAS = {
        "crecimiento": [0, 1, 2, 3, 4],
        "piel_y_vello": [5, 6, 7, 8],
        "cambios_vulva": [9, 10, 11, 12, 13],
        "cambios_pene": [14, 15, 16, 17, 18],
        "emociones": [19, 20, 21, 22],
        "sueno": [23, 24, 25],
        "diversidad_y_autoestima": [26, 27, 28],
        "alimentacion": [29, 30]
    }

    # ═══════════════════════════════════════════════════════════
    # MENSAJES DE APOYO
    # ═══════════════════════════════════════════════════════════

    MENSAJES_APOYO = [
        "Tu cuerpo está haciendo exactamente lo que necesita. Confía en él, es sabio.",
        "No hay un cuerpo 'normal'. Hay 8 mil millones de cuerpos diferentes en el mundo.",
        "Los cambios son señal de que estás creciendo, no de que algo esté mal.",
        "Si algo te preocupa, hablarlo con un adulto de confianza o un médico siempre es buena idea.",
        "La adolescencia es como una segunda infancia para tu cerebro. Ten paciencia contigo mismo/a.",
        "Cada cuerpo baila a su propio ritmo. No llegas tarde ni temprano, llegas a tu tiempo.",
        "Las redes sociales mienten. Los cuerpos reales tienen textura, pliegues, estrías e historia.",
        "Tu cuerpo es el vehículo de tu vida, no un adorno. Trátalo con cariño.",
        "Lo que sientes por tu cuerpo puede cambiar. Hoy no te gusta, mañana puedes hacer las paces con él.",
        "Eres mucho más que tu apariencia. Eres tus ideas, tus risas, tus sueños, tu forma de querer.",
        "La autoestima se construye de a poco. Cada día que te hablas bonito, pones un ladrillo.",
        "Está bien tener días malos con tu cuerpo. No significa que hayas retrocedido. Es parte del camino."
    ]

    MENSAJES_DERIVACION = [
        "No tengo información específica sobre eso, pero tu duda es totalmente válida. "
        "Te recomiendo consultar con un médico, enfermero/a escolar o un adulto de confianza. "
        "No hay preguntas tontas cuando se trata de tu cuerpo. Es inteligente preguntar.",

        "Esa es una excelente pregunta. Aunque no tengo la respuesta exacta, "
        "un profesional de la salud puede orientarte mucho mejor. ¿Te animas a consultarlo? "
        "Mientras tanto, recuerda: todas las dudas sobre el cuerpo son legítimas.",

        "Tu curiosidad es valiosa. No tengo esa información específica, pero "
        "un médico, ginecólogo/a o urólogo puede responderla con precisión. "
        "Consultar es un acto de amor propio. No te quedes con la duda.",

        "Qué bueno que preguntes. Aunque no tengo todos los detalles, "
        "quiero que sepas que preguntar sobre tu cuerpo es sano y necesario. "
        "Consulta con un adulto de confianza o un profesional de la salud."
    ]

    def __init__(self):
        self.historial_consultas = []
        self.faqs_mas_consultadas = []

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS PRINCIPALES
    # ═══════════════════════════════════════════════════════════

    def obtener_faqs(self) -> list:
        """Retorna todas las FAQs."""
        return self.FAQS

    def obtener_por_categoria(self, categoria: str) -> list:
        """Filtra FAQs por categoría."""
        indices = self.CATEGORIAS.get(categoria, [])
        return [self.FAQS[i] for i in indices]

    def buscar(self, termino: str) -> list:
        """Busca FAQs por palabra clave en pregunta o respuesta."""
        termino = termino.lower()
        resultados = []
        for pregunta, respuesta in self.FAQS:
            if termino in pregunta.lower() or termino in respuesta.lower():
                resultados.append((pregunta, respuesta))
        return resultados

    def obtener_categorias(self) -> list:
        """Retorna las categorías disponibles con descripción."""
        descripciones = {
            "crecimiento": "Cambios de altura, huesos y dolores de crecimiento",
            "piel_y_vello": "Acné, vello corporal, sudor y cambios en la piel",
            "cambios_vulva": "Menstruación, desarrollo mamario, flujo vaginal",
            "cambios_pene": "Erecciones, sueños húmedos, cambio de voz",
            "emociones": "Cambios de ánimo, irritabilidad, necesidad de soledad",
            "sueno": "Sueño adolescente, insomnio, ritmo circadiano",
            "diversidad_y_autoestima": "Imagen corporal, comparación, autoaceptación",
            "alimentacion": "Hambre, nutrición, dietas saludables"
        }
        return [(cat, descripciones.get(cat, "")) for cat in self.CATEGORIAS.keys()]

    def obtener_mensaje_apoyo(self) -> str:
        """Retorna un mensaje aleatorio de apoyo corporal positivo."""
        return random.choice(self.MENSAJES_APOYO)

    def obtener_mensaje_derivacion(self) -> str:
        """Retorna un mensaje de derivación a profesional de salud."""
        return random.choice(self.MENSAJES_DERIVACION)

    def responder(self, pregunta: str) -> str:
        """
        Busca la mejor respuesta para una consulta.
        Si no encuentra, deriva a profesional de forma empática.
        """
        self.historial_consultas.append(pregunta)
        resultados = self.buscar(pregunta)
        
        if resultados:
            pregunta_encontrada, respuesta = resultados[0]
            self.faqs_mas_consultadas.append(pregunta_encontrada)
            return respuesta
        
        return self.obtener_mensaje_derivacion()

    def obtener_respuesta_por_indice(self, indice: int) -> tuple:
        """Obtiene una FAQ por su índice."""
        if 0 <= indice < len(self.FAQS):
            return self.FAQS[indice]
        return None, None

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas de consultas."""
        conteo = Counter(self.faqs_mas_consultadas)
        return {
            "total_consultas": len(self.historial_consultas),
            "faqs_mas_consultadas": conteo.most_common(5),
            "categorias_disponibles": len(self.CATEGORIAS),
            "total_faqs": len(self.FAQS)
        }

    def obtener_faqs_relacionadas(self, indice: int) -> list:
        """Retorna FAQs relacionadas a una consultada (misma categoría)."""
        for categoria, indices in self.CATEGORIAS.items():
            if indice in indices:
                relacionados = [i for i in indices if i != indice]
                return [self.FAQS[i] for i in relacionados[:3]]
        return []


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Conocimiento v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/conocimiento.py (v3.0 - Hiper-Evolución)")
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

    c = Conocimiento()

    # Básicos
    t(isinstance(c, Conocimiento), "Instancia creada")
    t(len(c.obtener_faqs()) >= 30, f"{len(c.obtener_faqs())} FAQs (mín. 30)")

    # FAQs son tuplas válidas
    for i, faq in enumerate(c.obtener_faqs()):
        t(isinstance(faq, tuple) and len(faq) == 2, f"FAQ {i} es tupla (pregunta, respuesta)")
        t("?" in faq[0] or "¿" in faq[0], f"FAQ {i} tiene signo de interrogación")
        t(len(faq[1]) > 40, f"FAQ {i} respuesta sustancial")

    # Categorías
    categorias = c.obtener_categorias()
    t(len(categorias) >= 8, f"{len(categorias)} categorías (mín. 8)")
    t(isinstance(categorias[0], tuple) and len(categorias[0]) == 2, "Categorías tienen descripción")

    # Filtrar por categoría
    faqs_emociones = c.obtener_por_categoria("emociones")
    t(len(faqs_emociones) >= 3, f"Categoría emociones: {len(faqs_emociones)} FAQs")

    faqs_sueno = c.obtener_por_categoria("sueno")
    t(len(faqs_sueno) >= 2, f"Categoría sueño: {len(faqs_sueno)} FAQs")

    faqs_alimentacion = c.obtener_por_categoria("alimentacion")
    t(len(faqs_alimentacion) >= 2, f"Categoría alimentación: {len(faqs_alimentacion)} FAQs")

    # Búsqueda
    t(len(c.buscar("acné")) >= 1, "Búsqueda 'acné' encuentra")
    t(len(c.buscar("granitos")) >= 1, "Búsqueda 'granitos' encuentra")
    t(len(c.buscar("menstruación")) >= 1, "Búsqueda 'menstruación' encuentra")
    t(len(c.buscar("erección")) >= 1 or len(c.buscar("erecciones")) >= 1, "Búsqueda 'erección/erecciones' encuentra")
    t(len(c.buscar("xyzfantasiaxyz")) == 0, "Término inexistente = 0 resultados")

    # Responder
    r = c.responder("me salen granitos en la cara")
    t("acné" in r.lower() or "granitos" in r.lower() or "piel" in r.lower() or "grasa" in r.lower(), "Respuesta granitos relevante")

    r = c.responder("pregunta sin sentido xyz123")
    t(len(r) > 30, "Derivación a profesional sustancial")

    # Historial
    t(len(c.historial_consultas) == 2, "Historial: 2 consultas")

    # Mensaje de apoyo
    apoyo = c.obtener_mensaje_apoyo()
    t(isinstance(apoyo, str) and len(apoyo) > 15, f"Apoyo: '{apoyo[:50]}...'")

    # Mensaje de derivación
    deriv = c.obtener_mensaje_derivacion()
    t(len(deriv) > 30, "Derivación sustancial")

    # Obtener por índice
    p, r = c.obtener_respuesta_por_indice(0)
    t(p is not None and r is not None, "Índice 0 válido")
    p, r = c.obtener_respuesta_por_indice(999)
    t(p is None and r is None, "Índice 999 inválido")

    # FAQs relacionadas
    relacionadas = c.obtener_faqs_relacionadas(0)
    t(len(relacionadas) >= 1, "FAQs relacionadas encontradas")

    # Estadísticas
    stats = c.obtener_estadisticas()
    t("total_consultas" in stats, "Stats: total consultas")
    t("faqs_mas_consultadas" in stats, "Stats: FAQs más consultadas")
    t("total_faqs" in stats, "Stats: total FAQs")

    # Variedad mensajes de apoyo
    mensajes = [c.obtener_mensaje_apoyo() for _ in range(15)]
    t(len(set(mensajes)) >= 5, f"Variedad apoyo: {len(set(mensajes))}/15")

    # Lenguaje inclusivo (sin estigmatizar)
    for p, r in c.obtener_faqs():
        texto = p + " " + r
        t("anormal" not in texto.lower(), f"FAQ sin 'anormal': '{p[:40]}...'")
        t("defecto" not in texto.lower(), f"FAQ sin 'defecto': '{p[:40]}...'")

    # Cobertura de temas clave
    temas = ["menstruación", "vello", "voz", "sueño", "pecho", "sudor", "ánimo",
             "acné", "estrés", "dieta"]
    for tema in temas:
        encontrado = any(tema in p.lower() or tema in r.lower() for p, r in c.obtener_faqs())
        t(encontrado, f"Tema '{tema}' cubierto en FAQs")

    # Verificaciones especiales
    t(any("erección" in p.lower() or "erección" in r.lower() or 
          "erecciones" in p.lower() or "erecciones" in r.lower() 
          for p, r in c.obtener_faqs()), "Tema 'erección/erecciones' cubierto")
    t(any("autoestima" in p.lower() or "autoestima" in r.lower() 
          for p, r in c.obtener_faqs()), "Tema 'autoestima' cubierto")

    total = p_tests + f_tests
    print(f"\n  📊 {p_tests}/{total} tests pasados")
    if f_tests == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Conocimiento v3.0 validado\n")
    else:
        print(f"  ⚠️  {f_tests} test(s) fallaron\n")
    return f_tests == 0


if __name__ == "__main__":
    ejecutar_tests()