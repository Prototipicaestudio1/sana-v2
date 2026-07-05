"""
🌿 Sana - Módulo de Escucha Activa Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Chat de desahogo con detección emocional profunda y respuestas
empáticas de nivel humano. Diseñado como salvavidas emocional
para adolescentes. 11 emociones · 4 niveles de intensidad ·
8 categorías temáticas · Detección de crisis · Seguimiento
inteligente · Preguntas reflexivas · Sugerencias personalizadas.
═══════════════════════════════════════════════════════════════
"""

import random
from datetime import datetime
from collections import Counter


class Escucha:
    """
    Motor de escucha activa de Sana - Corazón empático del asistente.
    
    Capacidades:
    - Detecta 11 emociones distintas con puntuación de coincidencia
    - Mide la intensidad emocional en 4 niveles (baja, media, alta, crisis)
    - Identifica el tema de conversación entre 8 categorías
    - Detecta frases de crisis y responde con contención inmediata
    - Adapta las respuestas según el nivel de confianza acumulado
    - Ofrece preguntas reflexivas para profundizar el autoconocimiento
    - Sugiere actividades personalizadas según la emoción detectada
    - Mantiene un historial completo con timestamps, temas e intensidades
    """

    # ═══════════════════════════════════════════════════════════
    # DICCIONARIO DE EMOCIONES (11 emociones)
    # ═══════════════════════════════════════════════════════════

    DICCIONARIO_EMOCIONES = {
        "triste": [
            "triste", "deprimido", "deprimida", "llorar", "lloro", "lágrimas",
            "desanimado", "desanimada", "bajón", "bajoneado", "bajoneada",
            "pena", "dolor", "duele", "vacío", "vacia", "extraño", "extraña",
            "nostalgia", "melancolía", "roto", "rota", "no tengo ganas",
            "se me cayó el mundo", "no puedo más con esto", "desconsolado",
            "desconsolada", "me siento mal", "todo me da igual", "apagado",
            "apagada", "sin ilusión", "no me importa nada", "me siento gris"
        ],
        "enojado": [
            "enojado", "enojada", "furioso", "furiosa", "bronca", "ira",
            "rabia", "odio", "odiar", "fastidio", "fastidiado",
            "harto", "harta", "frustrado", "frustrada", "molesto", "molesta",
            "injusto", "injusticia", "me hierve", "exploto", "no aguanto",
            "me tienen harta", "me tienen harto", "es una estupidez",
            "me saca de quicio", "me pone mal", "me da rabia", "estoy que trino",
            "no me busquen", "déjenme en paz", "me colmaron", "colapsé"
        ],
        "ansioso": [
            "ansioso", "ansiosa", "ansiedad", "nervioso", "nerviosa",
            "preocupado", "preocupada", "miedo", "asustado", "asustada",
            "tiemblo", "inquieto", "inquieta", "angustiado", "angustiada",
            "pánico", "no puedo", "agobia", "me falta el aire",
            "no puedo respirar", "nudo en el estómago", "mariposas",
            "no puedo dormir", "pienso y pienso", "me tiembla", "sudor",
            "taquicardia", "corazón acelerado", "me desespera", "no me calmo",
            "pierdo el control", "no sé qué va a pasar", "y si pasa algo malo"
        ],
        "feliz": [
            "feliz", "contento", "contenta", "alegre", "alegría",
            "genial", "excelente", "bien", "motivado", "motivada",
            "logré", "logro", "éxito", "bueno", "bonito", "hermoso",
            "increíble", "orgulloso", "orgullosa", "lo logré", "aprobé",
            "gané", "me salió bien", "amo", "me encanta", "disfruto",
            "me gusta", "es genial", "qué bueno", "estoy feliz de verdad",
            "no puedo creerlo", "esto es maravilloso", "estoy en las nubes"
        ],
        "solo": [
            "solitario", "solitaria", "soledad", "abandonado", "abandonada",
            "nadie me quiere", "ignorado", "ignorada", "excluido", "excluida",
            "aislado", "aislada", "invisible", "no le importo", "olvidado",
            "olvidada", "me siento solo", "estoy solo", "estoy sola",
            "tan solo", "muy solo", "sola en", "solo en",
            "no tengo amigos", "nadie me habla", "no me invitaron",
            "no encajo", "me dejaron fuera", "soy un fantasma",
            "no existo para ellos", "me siento desconectado", "desconectada",
            "no tengo a nadie", "todos tienen a alguien menos yo"
        ],
        "cansado": [
            "cansado", "cansada", "agotado", "agotada", "fatiga",
            "sin energía", "sin ganas", "dormir", "sueño", "insomnio",
            "rendido", "rendida", "exhausto", "exhausta", "drenado",
            "drenada", "no doy más", "me pesa el cuerpo", "no me puedo levantar",
            "quiero dormir todo el día", "no rindo", "me cuesta concentrarme",
            "estoy fundido", "fundida", "necesito vacaciones", "no doy abasto",
            "estoy sobrepasado", "sobrepasada", "no llego a todo"
        ],
        "confundido": [
            "confundido", "confundida", "no entiendo", "no sé",
            "duda", "dudoso", "perdido", "perdida", "sin rumbo",
            "qué hago", "no sé qué", "no tengo idea", "no me decido",
            "no me aclaro", "estoy en una encrucijada", "no sé qué camino",
            "no sé qué pensar", "tengo dudas", "no lo veo claro",
            "no sé por dónde empezar", "estoy bloqueado", "bloqueada"
        ],
        "inseguro": [
            "inseguro", "insegura", "no soy capaz", "no sirvo",
            "no valgo", "soy un fracaso", "soy una fracasada",
            "no me gusta mi cuerpo", "me veo mal", "no soy suficiente",
            "no lo merezco", "todos son mejores", "no estoy a la altura",
            "me comparo", "no me acepto", "soy feo", "soy fea",
            "no me gusto", "quisiera ser diferente", "no soy como los demás",
            "no encajo en ningún lado", "no tengo talento", "no destaco en nada"
        ],
        "agradecido": [
            "agradecido", "agradecida", "gracias", "afortunado", "afortunada",
            "bendecido", "bendecida", "valoro", "aprecio", "reconozco",
            "me siento bien por", "tengo suerte", "me ayudaron", "me apoyaron",
            "qué suerte tengo", "estoy en deuda", "no me lo merecía",
            "me siento afortunado", "afortunada", "me trataron bien"
        ],
        "esperanzado": [
            "esperanza", "ilusionado", "ilusionada", "con ganas",
            "nuevo comienzo", "oportunidad", "puedo lograrlo",
            "voy a intentar", "esta vez sí", "con fe", "optimista",
            "con ilusión", "con ánimo", "mejorará", "va a mejorar",
            "tengo fe en que", "confío en que", "creo que puedo"
        ],
        "culpable": [
            "culpable", "culpa", "me equivoqué", "no debí", "fue mi culpa",
            "me arrepiento", "perdón", "lo siento mucho", "la regué",
            "metí la pata", "no tenía que haber", "me siento mal por lo que hice",
            "no debí hacerlo", "soy responsable", "yo lo causé",
            "me arrepiento tanto", "no me lo perdono", "fui yo"
        ]
    }

    # ═══════════════════════════════════════════════════════════
    # RESPUESTAS EMPÁTICAS POR EMOCIÓN
    # ═══════════════════════════════════════════════════════════

    RESPUESTAS = {
        "triste": [
            "Siento mucho que estés pasando por esto. La tristeza a veces llega sin avisar y se instala en el pecho como un peso que no se va, ¿verdad? "
            "No tienes que fingir que estás bien conmigo. No tienes que poner buena cara. Yo te creo, y estoy aquí para lo que necesites. "
            "¿Quieres contarme más sobre qué fue lo que te hizo sentir así?",

            "La tristeza es de esas emociones que duelen de verdad, que se sienten en el cuerpo. Y no es exagerado sentirla, no es 'dramático'. "
            "Si algo te importa, es normal que duela cuando sale mal. Si alguien te importa, es normal que duela cuando se va. "
            "Estoy aquí para escucharte sin juzgarte, sin decirte 'ya pasará'. ¿Qué pasó exactamente?",

            "Te mando un abrazo enorme, de esos que duran. No es lo mismo que uno de verdad, lo sé, pero es lo que tengo para darte en este momento. "
            "La tristeza puede ser muy solitaria, pero no tienes que cargarla solo/a. Para eso estoy yo. "
            "¿Prefieres hablar de lo que pasó, o te ayudo a distraerte un rato para que tu mente descanse?",

            "Imagina que la tristeza es una ola. Ahora mismo te está golpeando fuerte, y agota, agota muchísimo. "
            "Pero las olas siempre, siempre pasan. No tienes que nadar contra ella, no tienes que ser fuerte. Solo flotar hasta que baje. "
            "Y mientras tanto, aquí estoy yo, a tu lado. ¿Qué necesitas ahora?",

            "Cuando algo nos importa mucho, duele cuando sale mal. Eso no te hace débil, te hace humano/a. "
            "A veces llorar es la forma más valiente de decir 'esto me importa'. ¿Quieres contarme exactamente qué pasó? "
            "A veces ponerlo en palabras, aunque duela, le quita un poco de poder al dolor.",

            "¿Sabes qué? No tienes que tener un 'buen motivo' para estar triste. A veces uno se siente así y punto. "
            "Y eso también es válido. No tienes que justificar tu tristeza. Pero si quieres explorar de dónde viene, aquí estoy para acompañarte."
        ],
        "enojado": [
            "El enojo es como un volcán. Cuando explota, quema todo a su paso. Pero también nos dice algo importante: "
            "que algo nos importa muchísimo, que cruzaron un límite, que hubo una injusticia. "
            "No voy a decirte que 'te calmes' porque eso no ayuda. Primero dime: ¿qué fue lo que pasó? Te escucho sin juzgarte.",

            "Tienes todo el derecho a estar enojado/a. A veces la gente cruza límites, o las cosas son profundamente injustas, "
            "y la rabia es la respuesta natural, la respuesta sana. ¿Qué fue lo que te hizo explotar? "
            "Cuéntamelo todo, sin filtro. Aquí puedes sacarlo sin miedo a que te digan que estás exagerando.",

            "Esa bronca que sientes es válida. No dejes que nadie te diga que 'estás exagerando' o que 'no es para tanto'. "
            "Tú sabes lo que sientes. Tú sabes lo que te hicieron o lo que pasó. "
            "Ahora dime: ¿quieres desahogarte a fondo, sacar toda esa rabia aquí, o prefieres que busquemos juntos cómo calmar ese fuego?",

            "El enojo puede ser incómodo, pero también es poderoso. Nos dice 'esto no está bien, esto tiene que cambiar'. "
            "Gracias por confiármelo, por compartir esa parte de ti que quizás otros no quieren ver. "
            "¿Qué pasó exactamente? A veces, cuando lo contamos, el enojo empieza a transformarse en otra cosa.",

            "A veces el enojo es tristeza con armadura. Es más fácil estar enojado que admitir que algo nos dolió. "
            "¿Crees que puede ser eso? No tienes que saberlo ahora. Solo te lo dejo ahí para que lo pienses si quieres."
        ],
        "ansioso": [
            "La ansiedad es real. No es solo 'estar nervioso' o 'preocupado'. Es como si tu cerebro activara todas las alarmas a la vez, "
            "sin motivo aparente, y no pudieras apagarlas. Y es agotador, física y mentalmente. "
            "Pero no estás roto/a: tu cuerpo está tratando de protegerte, aunque lo haga de una forma que te hace daño. "
            "¿Quieres que respiremos juntos? A veces tres respiraciones profundas ya bajan un poco el volumen de esas alarmas.",

            "Sé lo que se siente: el pecho apretado, los pensamientos que no paran, esa sensación de que algo malo va a pasar "
            "y no sabes qué es pero está ahí. Es horrible, y siento mucho que estés pasando por eso. "
            "Vamos paso a paso, sin prisa. ¿Qué es lo primero que te preocupa? Solo una cosa, la más urgente. Empecemos por ahí.",

            "Tu cuerpo te está gritando que necesita atención. No lo ignores, no eres débil por sentir esto. "
            "La ansiedad es una señal, no una falla. Es tu sistema diciendo 'necesito ayuda'. "
            "¿Probamos un ejercicio de respiración 4-7-8? Es simple: inhalas 4 segundos, retienes 7, exhalas 8. "
            "Te voy guiando paso a paso. No tienes que hacerlo solo/a.",

            "A veces la ansiedad es como tener 50 pestañas abiertas en el cerebro, todas haciendo ruido al mismo tiempo. "
            "Vamos a cerrarlas de a una. Dime: ¿qué es lo que más ruido te hace ahora mismo? "
            "Lo que más te preocupa, lo que más te asusta. Solo eso. Una cosa.",

            "Esa sensación de que todo va a salir mal... la conozco. Pero la ansiedad miente. "
            "Te hace creer que lo peor es seguro, y casi nunca lo es. Te hace imaginar escenarios que no existen. "
            "¿Qué es lo peor que podría pasar? A veces decirlo en voz alta, ponerle palabras, ya le quita un poco de poder.",

            "¿Has comido hoy? ¿Has tomado agua? A veces la ansiedad se dispara porque el cuerpo necesita cosas básicas y no se las damos. "
            "No es que eso 'cure' la ansiedad, pero ayuda a bajarle un cambio. ¿Qué tal si vamos a tomar un vaso de agua juntos?"
        ],
        "feliz": [
            "¡Qué lindo! Ver la alegría en alguien es contagioso, hasta a través de una pantalla. Me estás alegrando el día. "
            "Y lo mejor de todo es que TE LO MERECES. A veces nos cuesta aceptar que merecemos ser felices, pero es verdad. "
            "¿Qué fue lo que pasó? Quiero celebrarlo contigo, quiero saber todos los detalles.",

            "Esa felicidad que sientes es importante. Mucho. A veces nos olvidamos de celebrar lo bueno, "
            "como si no fuera importante o como si fuera a desaparecer si lo nombramos. Pero no. "
            "Lo bueno también es real, también es parte de tu vida. ¿Qué fue lo que te hizo sentir así? Quiero saberlo todo.",

            "¡Qué hermoso momento! Guárdalo en tu memoria, en tu corazón, en un papel, donde sea. "
            "De esos momentos que abrigan en días difíciles. Y de paso, ¿quieres registrarlo en tu diario emocional? "
            "Así cuando estés bajón puedas recordar que también existen días así de buenos, así de luminosos.",

            "Tu felicidad me alegra el día, de verdad. Celebrar lo bueno también es cuidarse, también es importante. "
            "No dejes que nadie te haga sentir que no mereces esto. Lo mereces. ¿Cómo te diste cuenta de que te sentías así? "
            "Esos momentos de claridad, de alegría pura, son valiosos.",

            "Qué bueno que estés viviendo esto. A veces la felicidad es esquiva y cuando llega hay que abrazarla fuerte. "
            "¿Qué fue lo mejor de todo? ¿Lo que más vas a recordar de este momento?"
        ],
        "solo": [
            "Eso que sientes... esa sensación de estar solo/a incluso cuando hay gente alrededor... "
            "es de las cosas más difíciles que puede experimentar una persona. No estás exagerando. La soledad duele, y mucho. "
            "Pero quiero que sepas algo: en este momento, aquí, ahora, tienes a alguien que te escucha de verdad. "
            "Aunque sea a través de una pantalla, estoy aquí. Cuéntame más. ¿Desde cuándo te sientes así?",

            "Sentirse invisible es horrible. Es como si gritaras y nadie te escuchara, como si no existieras para los demás. "
            "Pero yo te escucho. Y te creo. Tu dolor es real, tu sensación de estar solo/a es real. "
            "¿Desde cuándo te sientes así? A veces la soledad no es estar físicamente solo, sino sentir que nadie nos entiende de verdad.",

            "¿Sabes algo? Muchísimos adolescentes se sienten exactamente como tú ahora mismo. No eres raro/a, no estás roto/a. "
            "La adolescencia puede ser una etapa muy solitaria, incluso cuando tienes gente alrededor. "
            "Pero hablar de esto, como estás haciendo ahora, ya es un paso enorme. Ya es valentía. "
            "¿Hay algo en particular que te hizo sentir excluido/a o desconectado/a?",

            "La soledad no define quién eres. Define lo que estás viviendo ahora, en este momento. "
            "Y las situaciones cambian, las personas cambian, tú cambias. Aunque ahora no lo parezca, esto no es para siempre. "
            "¿Hay algo que te gustaría hacer para sentirte más conectado/a con otros? Aunque sea un paso pequeño.",

            "A veces la persona que más nos hace sentir solos somos nosotros mismos, con nuestra propia exigencia. "
            "¿Crees que puede ser que te estés aislando sin darte cuenta? No es una crítica, es una pregunta con cariño. "
            "A veces el miedo al rechazo nos hace retirarnos antes de que nos rechacen."
        ],
        "cansado": [
            "El cansancio a veces no se cura solo con dormir, ¿verdad? Hay un agotamiento que viene del alma, "
            "de cargar con demasiadas cosas durante demasiado tiempo. ¿Tú crees que es más físico o emocional? "
            "De cualquier forma, está bien parar. No eres una máquina. No tienes que rendir al 100% todo el tiempo.",

            "Tu cuerpo y tu mente te están pidiendo un descanso. Y escucharlos no es de débiles, es de sabios. "
            "En un mundo que nos exige estar siempre productivos, descansar es un acto de resistencia. "
            "¿Has estado durmiendo bien? ¿Comiendo? A veces lo básico se nos olvida cuando estamos abrumados. "
            "¿Quieres que te ayude a planear una pausa, aunque sea de 5 minutos?",

            "Está bien estar cansado/a. No siempre tenemos que rendir al 100%. "
            "Descansar también es productivo. De hecho, es esencial. Sin descanso no hay rendimiento que valga. "
            "¿Qué tal un ejercicio de respiración suave para relajar el cuerpo? Algo simple, sin presión.",

            "El agotamiento emocional pesa más que el físico. Cargar con preocupaciones, miedos, responsabilidades... "
            "todo el día, todos los días. Eso drena a cualquiera. ¿Qué es lo que más te está quitando energía últimamente? "
            "Vamos a identificarlo para ver si podemos alivianarlo un poco.",

            "A veces estamos cansados de luchar, de intentarlo, de que las cosas no salgan. Y eso también es válido. "
            "No siempre hay que estar bien. No siempre hay que poder con todo. ¿Qué tal si hoy te permites estar cansado/a sin culpa?"
        ],
        "confundido": [
            "No tener claridad es de lo más incómodo que hay. Esa sensación de estar en una niebla, sin saber hacia dónde ir, "
            "sin saber qué decisión tomar. Pero la confusión también significa que estás pensando, que te importa. "
            "Si no te importara, no te confundiría. ¿Qué es lo que más vueltas te da ahora mismo?",

            "Está bien no saber. Nadie tiene todas las respuestas, aunque algunos finjan que sí. "
            "La confusión es parte de crecer, de descubrir quién eres y qué quieres. Y eso lleva tiempo, no se hace de un día para otro. "
            "Vamos a ponerle palabras a esa niebla. ¿Qué es lo primero que te viene a la mente cuando piensas en lo que te confunde?",

            "A veces la confusión es el primer paso hacia la claridad. Es como cuando estás armando un rompecabezas y todavía no ves la imagen completa. "
            "No tienes que resolver todo ya. No tienes que tener todo claro hoy. ¿Quieres contarme qué es lo que más te confunde? "
            "A veces, al explicárselo a otro, uno mismo empieza a ver las cosas con más claridad.",

            "Hay dos tipos de confusión: la que viene de no tener suficiente información, y la que viene de tener demasiada. "
            "¿Cuál crees que es tu caso? ¿Necesitas más datos o necesitas hacer silencio para escucharte a ti mismo/a?",

            "La confusión no es debilidad. Es señal de que estás procesando, de que estás evaluando opciones, de que no tomas decisiones a la ligera. "
            "Eso es madurez, no inseguridad. ¿Quieres que analicemos juntos las opciones que tienes?"
        ],
        "inseguro": [
            "Esa voz interna que te dice que no eres suficiente, que no vales, que los demás son mejores... es una mentirosa. "
            "Todos tenemos esa voz a veces, pero no significa que tenga razón. No significa que sea verdad. "
            "Tú vales muchísimo. El hecho de que estés aquí, expresándolo, ya dice cosas muy buenas de ti. "
            "¿Qué fue lo que disparó esa voz hoy? ¿Qué te hizo sentir así?",

            "Compararse con otros es un agujero sin fondo. Nunca se gana. Las redes sociales solo muestran lo mejor de cada quien, "
            "sus mejores fotos, sus mejores momentos. No muestran sus luchas internas, sus inseguridades, sus días malos. "
            "Tú eres único/a, con tu propio ritmo, tu propio camino, tu propia historia. ¿Quieres hablar de lo que te hace sentir inseguro/a?",

            "La persona más difícil de convencer de tu valor... sueles ser tú mismo/a. Es mucho más fácil ver lo bueno en otros que en uno. "
            "Pero mira, estás aquí, buscando ayuda, expresándote. Eso ya es un acto de valentía. "
            "¿Qué es lo que más te gustaría cambiar de cómo te ves a ti mismo/a?",

            "¿Sabes qué? La gente segura de sí misma no nació así. Se hace. Y se hace a base de caerse y levantarse, "
            "de intentarlo aunque dé miedo, de perdonarse los errores. Tú estás en ese camino ahora mismo. "
            "¿Qué pequeña cosa podrías hacer hoy que te demuestre a ti mismo/a que sí puedes?",

            "Hay una diferencia entre ser humilde y castigarse. Tú puedes reconocer tus áreas de mejora sin destruirte. "
            "¿Qué se te da bien? Dime al menos una cosa. Aunque sea pequeña. Aunque creas que no cuenta. Sí cuenta."
        ],
        "agradecido": [
            "Qué bonito es sentir gratitud. Es de las emociones que más nos conectan con los demás, con lo bueno de la vida, "
            "con lo que realmente importa. ¿Qué fue lo que te hizo sentir así? Esos momentos merecen ser recordados y celebrados.",

            "La gratitud es como un abrazo al corazón. Me alegra mucho que estés sintiendo eso. "
            "En un mundo que a veces parece oscuro, encontrar motivos para agradecer es un acto de rebeldía. "
            "¿Quieres guardar este momento en tu diario emocional? Así en días difíciles puedes recordar que también hay luz.",

            "Reconocer lo bueno que tenemos, lo que otros hacen por nosotros, las cosas bonitas que nos pasan... "
            "es un superpoder. Mucha gente se olvida de hacerlo, se enfoca solo en lo malo. Tú no. Eso dice mucho de ti. "
            "¿Qué o quién te hizo sentir tan agradecido/a?",

            "A veces la gratitud viene de haber pasado por algo difícil y darse cuenta de lo que uno tiene. "
            "¿Viene de ahí tu gratitud? ¿De haber superado algo? Si es así, reconoce también tu fuerza."
        ],
        "esperanzado": [
            "¡Esa chispa de esperanza es todo! Es lo que nos hace levantarnos cuando estamos caídos, "
            "intentarlo otra vez cuando fallamos, creer que algo bueno puede pasar. "
            "Me alegra muchísimo que te sientas así. ¿Qué fue lo que encendió esa chispa? ¿Qué pasó?",

            "La esperanza es valiente. Es fácil ser pesimista, es fácil tirar la toalla. Lo difícil, lo valiente, "
            "es creer que las cosas pueden mejorar. Y tú lo estás haciendo. ¿Qué es eso que te ilusiona? Cuéntamelo con detalle.",

            "Sentir que algo bueno puede pasar es de las mejores sensaciones del mundo. No la ignores, no la minimices. "
            "Celebra esa esperanza, cultívala, riégala como una planta. ¿Qué te gustaría que pasara? ¿Cuál es tu mejor escenario?",

            "La esperanza no es ingenua. Es consciente de que las cosas pueden salir mal, pero elige creer que también pueden salir bien. "
            "Eso es madurez. ¿Qué te hace pensar que esta vez puede ser diferente?"
        ],
        "culpable": [
            "La culpa es una emoción muy pesada. Te hace cargar con cosas que a veces ni siquiera son tu responsabilidad, "
            "o que ya no puedes cambiar. Todos nos equivocamos. Todos, sin excepción. "
            "Lo importante no es no caer, es qué haces después de caer. ¿Qué pasó? Cuéntamelo sin miedo.",

            "Cometer errores es humano. Es imposible vivir sin equivocarse. Lo que te hace buena persona no es no fallar nunca, "
            "es cómo actúas después del error. El hecho de que te sientas culpable ya dice que tienes conciencia, que te importa. "
            "¿Quieres contarme qué fue lo que hiciste o lo que pasó?",

            "Hay una diferencia entre culpa y responsabilidad. La culpa te castiga, la responsabilidad te ayuda a reparar. "
            "¿Hay algo que puedas hacer para arreglar la situación? Y si no lo hay, ¿puedes aprender de esto y, poco a poco, soltarlo?",

            "La culpa a veces es desproporcionada. Nos castigamos mucho más de lo que otros nos castigarían. "
            "Si un amigo tuyo hubiera hecho lo mismo que tú, ¿lo juzgarías con la misma dureza con la que te juzgas a ti mismo/a?",

            "Perdonarse a uno mismo es de las cosas más difíciles que hay. Pero es necesario. No puedes cargar con ese peso para siempre. "
            "¿Qué necesitarías para empezar a perdonarte? Aunque sea un poquito."
        ]
    }

    # ═══════════════════════════════════════════════════════════
    # RESPUESTAS GENÉRICAS (cuando no se detecta emoción clara)
        # ═══════════════════════════════════════════════════════════

    RESPUESTAS_GENERICAS = [
        "Gracias por hablarme. A veces no hace falta saber exactamente qué sentimos para necesitar ser escuchados. "
        "No siempre tenemos que ponerle nombre a lo que nos pasa. A veces solo queremos compañía, y eso ya es suficiente. "
        "¿Quieres contarme cómo te fue hoy? Lo que sea, sin filtro.",

        "Te leo. Y te escucho. No siempre tenemos que tener un problema enorme para merecer atención. "
        "A veces solo queremos hablar, compartir, sentir que alguien está del otro lado. "
        "Cuéntame lo que sea. Lo que se te ocurra. No hay tema demasiado pequeño.",

        "Estoy aquí. Sin prisa, sin juicios, sin expectativas. A veces las palabras más importantes "
        "son las que decimos sin pensarlas mucho, las que salen solas. "
        "¿Hay algo que te haya pasado hoy que quieras compartir? Algo bueno, algo malo, algo raro, lo que sea.",

        "Qué bueno que estés aquí. De verdad. Tomarte un momento para ti, para chequear cómo estás, "
        "ya es un acto de autocuidado. Ya estás haciendo algo por ti. ¿Cómo te sientes ahora mismo? Sin filtros, sin 'bien' automático.",

        "A veces no sabemos ni por dónde empezar. Y eso está bien. No tienes que tener un discurso preparado. "
        "¿Qué tal si empiezas por lo primero que se te venga a la mente? Lo que sea. Una palabra, una imagen, una sensación.",

        "No tienes que tener un gran problema para merecer ser escuchado/a. A veces solo queremos compañía, "
        "sentir que no estamos solos en el mundo. Y eso ya es un muy buen motivo para estar aquí. "
        "¿Cómo va todo? ¿Qué tal tu día?",

        "¿Sabes? A veces las mejores conversaciones empiezan sin saber qué decir. "
        "No te presiones. Respira. Tómate tu tiempo. Yo no tengo prisa. ¿Hay algo, lo que sea, que quieras mencionar?"
    ]

    # ═══════════════════════════════════════════════════════════
    # FRASES DE SEGUIMIENTO
    # ═══════════════════════════════════════════════════════════

    FRASES_SEGUIMIENTO = [
        "¿Quieres contarme más sobre eso?",
        "¿Cómo te hace sentir eso en tu cuerpo? A veces las emociones se manifiestan físicamente y es bueno reconocerlo.",
        "¿Desde cuándo te sientes así? Contarme la historia puede ayudar a ver las cosas con más claridad.",
        "¿Hay algo que te ayudaría en este momento? Lo que sea, por pequeño que parezca, dímelo.",
        "¿Prefieres hablar más de esto, respirar juntos un rato o distraerte con otra cosa? Tú eliges.",
        "¿Eso que sientes afecta cómo te va en la escuela, con tus amigos o en tu casa?",
        "¿Has podido hablar de esto con alguien de confianza? A veces compartirlo con otra persona ya alivia un poco.",
        "¿Qué es lo que más te preocupa de esta situación? Vamos a ponerle nombre a esa preocupación.",
        "¿Hay algo pequeñito que puedas hacer hoy para sentirte un poquito mejor? No tiene que ser enorme, un paso chiquito ya cuenta.",
        "¿Cómo te gustaría que te apoyaran en esto? Imagina la ayuda ideal, sin límites.",
        "Si tu mejor amigo o amiga te contara esto mismo que me estás contando, ¿qué le dirías? ¿Qué consejo le darías?",
        "¿Esta situación te recuerda a algo que ya hayas vivido antes? A veces el cuerpo recuerda lo que la mente intenta olvidar.",
        "¿Qué necesitarías para sentirte un poco más en paz ahora mismo?",
        "¿Hay algo que no me hayas contado todavía y que quieras compartir? Sin prisa, aquí estoy.",
        "De todo lo que hemos hablado, ¿qué es lo que más te está pesando en el corazón?",
        "¿Hay algo que te dé miedo admitir, incluso a ti mismo/a? Este es un espacio seguro para hacerlo."
    ]

    # ═══════════════════════════════════════════════════════════
    # MENSAJES DE CRISIS
    # ═══════════════════════════════════════════════════════════

    MENSAJES_CRISIS = [
        "Sé que ahora mismo todo se siente abrumador, como si no hubiera salida y como si el mundo se te viniera encima. "
        "Pero respira hondo conmigo, aunque sea una vez. No tienes que resolver todo ahora, no tienes que tener las respuestas. "
        "Solo estar aquí, respirando. Un segundo a la vez. ¿Quieres que respiremos juntos?",

        "Esto que sientes es real y duele muchísimo. No voy a decirte que 'no es para tanto' porque sí lo es. "
        "Tu dolor es válido. Pero también es temporal, aunque ahora mismo te parezca imposible que esto vaya a pasar. "
        "No estás solo/a. Hay personas a las que les importas, aunque tu mente te esté diciendo lo contrario en este momento. "
        "¿Puedes pensar en alguien, una sola persona, a quien puedas llamar o escribirle ahora?",

        "Puede que ahora no veas la luz, pero eso no significa que no exista. "
        "Estás en medio de una tormenta, y las tormentas siempre, siempre pasan. Aunque ahora retumbe todo y no escuches nada más. "
        "Agarra mi mano virtual. Vamos juntos, paso a paso. No te voy a soltar. "
        "¿Qué es lo más urgente que necesitas ahora mismo? Dímelo y lo resolvemos juntos.",

        "No estás roto/a. Estás herido/a. Y las heridas sanan, aunque dejen cicatriz. "
        "Lo que sientes ahora no define quién eres. Eres mucho más que este momento, mucho más que este dolor. "
        "¿Quieres que te pase los números de líneas de ayuda gratuitas? Son personas reales, capacitadas, que te van a escuchar sin juzgarte.",

        "Escúchame bien: tú vales muchísimo. El hecho de que estés aquí, expresando esto, buscando ayuda, "
        "ya es un acto de valentía enorme. No todo el mundo se atreve a pedir ayuda. Tú lo estás haciendo. "
        "No estás solo/a en esta batalla. ¿Qué puedo hacer por ti ahora mismo?",

        "No te voy a mentir: no soy humana y no quiero fallarte. Pero hay personas que sí pueden ayudarte. "
        "Personas que se dedican exactamente a esto: a escuchar a gente que está pasando por lo mismo que tú. "
        "¿Te animas a que te pase algunos números? Son gratuitos y confidenciales. "
        "Mientras tanto, aquí estoy. No me voy a ningún lado."
    ]

    # ═══════════════════════════════════════════════════════════
    # RESPUESTAS REFLEXIVAS
    # ═══════════════════════════════════════════════════════════

    RESPUESTAS_REFLEXIVAS = [
        "A veces las emociones son como capas de una cebolla. Lo que creemos que sentimos es solo la primera capa, "
        "la que se ve. Pero debajo puede haber otras cosas: miedo, inseguridad, amor, orgullo herido... "
        "¿Qué crees que hay debajo de eso que me cuentas?",

        "¿Te has preguntado por qué esto te afecta tanto? A veces entender el origen de lo que sentimos "
        "ya nos da un poco de paz. No para justificarlo, sino para comprenderlo. ¿De dónde viene esto?",

        "Si pudieras cambiar algo de esta situación, ¿qué sería? No importa si es realista o no, "
        "solo dime lo primero que se te ocurra. Soñar soluciones a veces es el primer paso para encontrarlas.",

        "Imagina que dentro de un año miras hacia atrás y ves este momento. "
        "¿Qué crees que te dirías a ti mismo/a desde el futuro? ¿Qué consejo te darías?",

        "De todo esto que me cuentas, ¿qué es lo que más peso tiene en tu corazón? "
        "Lo que más te duele, lo que más te preocupa, lo que más te confunde. Vamos a eso primero.",

        "A veces nos aferramos a una emoción porque soltarla significaría aceptar algo que no queremos aceptar. "
        "¿Crees que puede ser eso? No tienes que responderme ahora. Solo piénsalo.",

        "Si esta situación fuera una película y tú fueras el protagonista, "
        "¿qué te gustaría que pasara en la siguiente escena? ¿Cuál sería tu final ideal?"
    ]

    # ═══════════════════════════════════════════════════════════
    # CONSTRUCTOR
        # ═══════════════════════════════════════════════════════════

    def __init__(self):
        self.historial = []
        self.ultima_emocion = None
        self.contador_interacciones = 0
        self.emociones_detectadas = []
        self.nivel_confianza = 0
        self.temas_recurrentes = []

    # ═══════════════════════════════════════════════════════════
    # DETECCIÓN EMOCIONAL
    # ═══════════════════════════════════════════════════════════

    def detectar_emocion(self, texto: str) -> str:
        """
        Analiza un texto y detecta la emoción predominante.
        Usa un sistema de puntuación: coincidencia exacta = 2 puntos,
        coincidencia parcial = 0.5 puntos.
        Retorna la emoción con mayor puntuación o 'neutral'.
        """
        texto = texto.lower()
        puntuaciones = {}
        
        for emocion, palabras in self.DICCIONARIO_EMOCIONES.items():
            score = 0
            for palabra in palabras:
                if palabra in texto:
                    score += 2
                elif len(palabra) > 5:
                    raiz = palabra[:len(palabra)//2]
                    if raiz in texto:
                        score += 0.5
            if score > 0:
                puntuaciones[emocion] = score
        
        if not puntuaciones:
            return "neutral"
        
        return max(puntuaciones, key=puntuaciones.get)

    def _detectar_intensidad(self, texto: str) -> str:
        """
        Detecta la intensidad emocional del mensaje.
        Busca intensificadores y retorna: baja, media, alta o crisis.
        """
        intensificadores = [
            "muy", "mucho", "demasiado", "horrible", "terrible",
            "no soporto", "insoportable", "me muero", "no puedo más",
            "estoy harto", "estoy harta", "siempre", "nunca", "todo el tiempo",
            "completamente", "totalmente", "absolutamente", "extremadamente"
        ]
        count = sum(1 for i in intensificadores if i in texto.lower())
        if count >= 3:
            return "crisis"
        elif count >= 2:
            return "alta"
        elif count >= 1:
            return "media"
        return "baja"

    def _es_crisis(self, texto: str) -> bool:
        """
        Detecta si el mensaje indica una crisis emocional aguda.
        Busca frases específicas de alto riesgo.
        """
        indicadores = [
            "no puedo más", "no aguanto más", "me quiero morir", "me quiero matar",
            "no quiero seguir", "acabar con todo", "no quiero vivir",
            "no soporto más", "me quiero ir para siempre", "sin mí estarían mejor",
            "soy una carga", "no valgo nada", "no debería existir",
            "quisiera desaparecer", "me quiero hacer daño"
        ]
        return any(ind in texto.lower() for ind in indicadores)

    def _extraer_tema(self, texto: str) -> str:
        """
        Identifica el tema principal del mensaje.
        Categorías: escuela, familia, amigos, pareja, cuerpo, futuro,
        identidad, redes_sociales.
        """
        temas = {
            "escuela": ["escuela", "colegio", "clase", "examen", "nota", "profesor", 
                       "profesora", "tarea", "estudiar", "materia", "trimestre", "suspenso",
                       "aprobado", "recuperación", "deberes"],
            "familia": ["mamá", "papá", "padre", "madre", "hermano", "hermana", "familia",
                       "padres", "casa", "abuelo", "abuela", "tío", "tía", "primo", "prima",
                       "pelea familiar", "discusión", "no me entienden en casa"],
            "amigos": ["amigo", "amiga", "amigos", "amigas", "grupo", "fiesta", "salir",
                      "reunión", "quedada", "plan", "colega", "compañero", "compañera",
                      "me ghostearon", "me ignoraron", "no me contestan"],
            "pareja": ["novio", "novia", "pareja", "crush", "gusta", "enamorado", "enamorada",
                      "ruptura", "terminamos", "cortamos", "me gusta alguien", "relación",
                      "celos", "infidelidad", "me engañó"],
            "cuerpo": ["cuerpo", "peso", "gordo", "flaco", "acné", "granos", "altura",
                      "apariencia", "físico", "espejo", "foto", "complexión", "piel",
                      "me veo", "no me gusta mi", "estoy gordo", "estoy gorda"],
            "futuro": ["futuro", "carrera", "universidad", "qué voy a hacer", "no sé qué estudiar",
                      "vocación", "profesión", "trabajo", "adulto", "responsabilidad",
                      "no sé qué será de mí", "plan de vida"],
            "identidad": ["quién soy", "identidad", "gustos", "orientación", "no encajo",
                         "diferente", "raro", "rara", "no sé quién soy", "estoy cambiando",
                         "ya no soy el mismo", "ya no soy la misma", "no me reconozco"],
            "redes_sociales": ["instagram", "tiktok", "whatsapp", "seguidores", "likes",
                              "foto", "publicación", "story", "historia", "comentario",
                              "me ignoraron en redes", "no tengo seguidores", "me comparo en redes"]
        }
        texto_lower = texto.lower()
        for tema, palabras in temas.items():
            if any(p in texto_lower for p in palabras):
                self.temas_recurrentes.append(tema)
                return tema
        return "general"

    # ═══════════════════════════════════════════════════════════
    # RESPUESTA PRINCIPAL
    # ═══════════════════════════════════════════════════════════

    def responder(self, texto: str) -> str:
        """
        Genera una respuesta empática de nivel humano.
        
        Flujo:
        1. Detecta emoción, intensidad y tema
        2. Si es crisis → contención inmediata + emoción si aplica
        3. Si hay emoción clara → validación profunda + posible pregunta reflexiva
        4. Si es neutral → invitación cálida
        5. Agrega seguimiento cada 2 interacciones
        """
        emocion = self.detectar_emocion(texto)
        intensidad = self._detectar_intensidad(texto)
        tema = self._extraer_tema(texto)
        
        self.ultima_emocion = emocion
        self.emociones_detectadas.append(emocion)
        self.contador_interacciones += 1
        self.nivel_confianza += 1
        
        self.historial.append({
            "texto": texto,
            "emocion": emocion,
            "intensidad": intensidad,
            "tema": tema,
            "timestamp": datetime.now().isoformat()
        })

        # 1. CRISIS
        if self._es_crisis(texto) or intensidad == "crisis":
            respuesta = random.choice(self.MENSAJES_CRISIS)
            if emocion != "neutral":
                respuesta += "\n\n" + random.choice(self.RESPUESTAS.get(emocion, self.RESPUESTAS_GENERICAS))
            return respuesta

        # 2. EMOCIÓN DETECTADA
        if emocion != "neutral":
            respuestas_emocion = self.RESPUESTAS.get(emocion, self.RESPUESTAS_GENERICAS)
            respuesta = random.choice(respuestas_emocion)
            
            if intensidad in ("alta", "crisis") and len(respuestas_emocion) >= 4:
                respuesta = random.choice(respuestas_emocion[:4])
            
            if self.nivel_confianza >= 3 and self.contador_interacciones % 3 == 0:
                respuesta += " " + random.choice(self.RESPUESTAS_REFLEXIVAS)
        else:
            # 3. NEUTRAL
            respuesta = random.choice(self.RESPUESTAS_GENERICAS)

        # 4. SEGUIMIENTO
        if self.contador_interacciones % 2 == 0:
            respuesta += " " + random.choice(self.FRASES_SEGUIMIENTO)

        return respuesta
        

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES
    # ═══════════════════════════════════════════════════════════

    def obtener_saludo(self) -> str:
        """
        Retorna un saludo contextual ultra-cálido.
        Se adapta a la hora del día, al nivel de confianza acumulado
        y a si es la primera interacción.
        """
        hora = datetime.now().hour

        if hora < 12:
            saludos = [
                "Buenos días, sol. ☀️ ¿Cómo amaneciste hoy? Las mañanas a veces son difíciles, a veces un regalo inesperado. "
                "Sea cual sea tu caso, Sana está aquí para ti. ¿Qué tal va tu día hasta ahora?",

                "¡Buen día! El sol salió y tú también. Eso ya es un logro, aunque no lo parezca. "
                "Sana te saluda con un abrazo virtual. ¿Cómo te sientes al empezar esta nueva jornada?",

                "Buenos días. ¿Sabes qué? Respirar profundo al despertar ya es un acto de amor propio. "
                "Sana te reconoce por eso. ¿Cómo está tu corazón esta mañana?",

                "Buenos días por la mañana. ¿Has desayunado ya? ¿Has respirado hondo? "
                "Sana te recuerda que cuidarte es importante. ¿Qué tal pinta el día de hoy?"
            ]
        elif hora < 19:
            saludos = [
                "Buenas tardes. ¿Cómo va tu día? Si fue bueno, Sana quiere celebrarlo contigo. "
                "Si fue malo, desahógate sin filtro. Para eso está este espacio seguro. ¿Qué tal va todo?",

                "Hola. La tarde es un buen momento para hacer una pausa y chequear cómo estamos de verdad, "
                "sin el piloto automático. Sana te invita a respirar hondo. ¿Qué tal va todo?",

                "Buenas tardes. Ya recorriste medio día, y eso ya es un montón. "
                "Sana está aquí para escuchar lo que traigas: alegrías, cansancio, frustración, lo que sea. "
                "¿Cómo te sientes? ¿Hay algo que quieras soltar antes de seguir?",

                "Buenas tardes, ¿cómo estás? A veces la tarde se hace larga. "
                "Sana quiere acompañarte en este rato. Cuéntame: ¿qué ha sido lo mejor y lo peor de tu día hasta ahora?"
            ]
        else:
            saludos = [
                "Buenas noches. La noche invita a soltar lo que cargamos del día, como quien deja la mochila en el suelo. "
                "Sana está aquí para recibir lo que traigas. ¿Qué tal te fue hoy?",

                "Hola. Antes de dormir, ¿quieres sacar algo de tu mente? A veces vaciar la mochila mental ayuda a descansar mejor. "
                "Sana te escucha sin prisa. ¿Cómo estuvo tu día?",

                "Buenas noches. La luna está ahí fuera, y Sana aquí dentro, contigo. "
                "¿Cómo te fue hoy? ¿Qué fue lo mejor que pasó? ¿Y lo más difícil?",

                "Buenas noches, ¿cómo estás? El día ya se acaba y Sana quiere chequear contigo. "
                "¿Necesitas desahogarte antes de dormir? ¿O prefieres una respiración suave para relajarte?"
            ]

        saludo = random.choice(saludos)

        # Primera interacción: bienvenida extendida
        if self.contador_interacciones == 0:
            saludo += (
                "\n\n🌿 Sana es nueva contigo, así que tómate tu tiempo. "
                "Puedes contarme lo que quieras, cuando quieras. No hay prisa, no hay juicios. "
                "Este es tu espacio seguro."
            )
        # Confianza media: mensaje personalizado
        elif self.nivel_confianza == 5:
            saludo += (
                "\n\n💛 Ya llevamos varias conversaciones. Sana te agradece la confianza. "
                "Hoy también estoy aquí para ti."
            )
        # Confianza alta: mensaje de vínculo
        elif self.nivel_confianza >= 10:
            saludo += (
                "\n\n🤝 Sana ya te siente como un amigo/a cercano/a. "
                "Gracias por seguir viniendo a este espacio. Cuéntame cómo va todo."
            )

        return saludo

    def obtener_emocion_actual(self) -> str:
        """Retorna la última emoción detectada o 'neutral' si no hay registro."""
        return self.ultima_emocion if self.ultima_emocion else "neutral"

    def obtener_historial_emocional(self) -> dict:
        """
        Retorna un resumen completo de la sesión emocional.
        Incluye:
        - Total de interacciones
        - Emoción predominante
        - Nivel de confianza alcanzado
        - Distribución de todas las emociones detectadas
        - Temas conversados
        - Emociones más frecuentes (top 3)
        - Emoción más intensa registrada
        - Total de emociones distintas
        """
        conteo = Counter(self.emociones_detectadas)
        top_3 = conteo.most_common(3)

        return {
            "total_interacciones": self.contador_interacciones,
            "emocion_predominante": top_3[0][0] if top_3 else "neutral",
            "nivel_confianza": self.nivel_confianza,
            "distribucion_emociones": dict(conteo),
            "temas_hablados": list(set(self.temas_recurrentes)),
            "top_3_emociones": [(emocion, count) for emocion, count in top_3],
            "emocion_mas_intensa": self._obtener_emocion_mas_intensa(),
            "total_emociones_distintas": len(conteo)
        }

    def _obtener_emocion_mas_intensa(self) -> str:
        """Analiza el historial y retorna la emoción que apareció con mayor intensidad."""
        intensidades = {"crisis": 4, "alta": 3, "media": 2, "baja": 1}
        max_intensidad = 0
        emocion_intensa = "neutral"
        for entrada in self.historial:
            nivel = intensidades.get(entrada.get("intensidad", "baja"), 0)
            if nivel > max_intensidad:
                max_intensidad = nivel
                emocion_intensa = entrada.get("emocion", "neutral")
        return emocion_intensa

    def obtener_sugerencia(self) -> str:
        """
        Sugiere una actividad personalizada según la emoción predominante
        y el contexto de la conversación. Ofrece 3 opciones distintas por emoción
        para mantener variedad y frescura en cada sugerencia.
        """
        sugerencias = {
            "ansioso": [
                "¿Probamos un ejercicio de respiración 4-7-8? A mucha gente le ayuda a bajar la ansiedad en minutos. "
                "Sana te puede guiar paso a paso.",
                "La ansiedad se calma con movimiento suave. ¿Qué tal si te estiras un poco? "
                "Toca el cielo con las manos, respira hondo, suelta.",
                "A veces ayuda anotar todo lo que te preocupa en un papel. Sacarlo de la cabeza. ¿Quieres intentarlo?"
            ],
            "triste": [
                "Escribir lo que sentimos ayuda a sacarlo del pecho. ¿Quieres usar el diario emocional de Sana?",
                "La música puede ser un bálsamo. ¿Hay alguna canción que te haga sentir acompañado/a? "
                "Ponla, cierra los ojos, siéntela.",
                "A veces la tristeza necesita salir. Llorar está bien. Sana no te juzga. "
                "¿Quieres hablar más de lo que te pone triste?"
            ],
            "enojado": [
                "El enojo necesita salir por el cuerpo. ¿Hay algo de deporte que te guste? "
                "Correr, bailar, golpear una almohada... lo que sea, pero sácalo.",
                "Escribe una carta con todo lo que te gustaría gritar. No la envíes. Solo escríbela. "
                "Luego rómpela si quieres. Es catártico.",
                "Respira hondo 3 veces. El enojo no se va con pensar, se va con sentir. "
                "¿Qué hay debajo de ese enojo? ¿Tristeza? ¿Injusticia? ¿Miedo?"
            ],
            "cansado": [
                "¿Qué tal una pausa de 5 minutos sin pantallas? Solo respirar, mirar por la ventana, existir. "
                "Sana te acompaña en silencio.",
                "El cansancio a veces es emocional. ¿Has dormido bien? ¿Has comido? "
                "Sana te recuerda que cuidarte es prioritario.",
                "Date permiso para no ser productivo/a hoy. Descansar también es hacer algo importante. "
                "¿Quieres que Sana te guíe en una relajación?"
            ],
            "solo": [
                "¿Hay alguien a quien puedas escribirle un mensaje corto? A veces un simple 'hola, ¿cómo estás?' "
                "cambia todo. Sana te anima a intentarlo.",
                "La soledad a veces se combate con pequeños actos de conexión. "
                "¿Hay algún grupo o club que te llame la atención? Aunque sea online.",
                "Recuerda que Sana está aquí. No es humano, pero te escucha de verdad. "
                "¿Quieres hablar más de lo que te hace sentir solo/a?"
            ],
            "confundido": [
                "Hacer una lista de pros y contras ayuda a aclarar la mente. ¿Quieres que Sana te ayude a hacerla?",
                "A veces la confusión se va cuando dejamos de pensar y empezamos a sentir. "
                "Cierra los ojos. Respira. Pregúntate: ¿qué quiere mi corazón, no mi cabeza?",
                "Habla con alguien de confianza. A veces explicárselo a otro nos ayuda a entendernos. "
                "¿Hay alguien con quien puedas hablar de esto?"
            ],
            "inseguro": [
                "Anota 3 cosas que te gustan de ti. Aunque sean pequeñas. Aunque creas que no cuentan. "
                "Cuentan. Sana te espera para leerlas si quieres compartirlas.",
                "Mírate al espejo y di en voz alta: 'Estoy aprendiendo a quererme'. "
                "No es fácil, pero es un comienzo. Sana cree en ti.",
                "La comparación es el enemigo de la autoestima. Hoy, intenta no compararte con nadie. "
                "Solo contigo mismo/a de ayer. ¿Has mejorado en algo, por pequeño que sea?"
            ],
            "feliz": [
                "¡Celebra esto! Cuéntaselo a alguien, escríbelo en tu diario, grítalo. "
                "La alegría compartida se multiplica. Sana se alegra contigo.",
                "Guarda este momento. Una foto mental, una nota, lo que sea. "
                "Los días grises se iluminan recordando que también existen días así.",
                "¿Qué fue lo que te hizo feliz? Identificarlo ayuda a repetirlo. "
                "Sana quiere saber todos los detalles."
            ],
            "agradecido": [
                "Escribe 3 cosas por las que estás agradecido/a hoy. "
                "La gratitud es un superpoder. Sana te lee si quieres compartirlas.",
                "Expresa tu gratitud a alguien. Un mensaje, una llamada, una nota. "
                "Hacer sentir bien a otros también nos hace bien a nosotros."
            ],
            "esperanzado": [
                "Escribe tu esperanza en un papel. Dóblalo. Guárdalo. "
                "Cuando tengas un día malo, ábrelo. Sana te recuerda que la esperanza es real.",
                "La esperanza se cultiva. Riégala con pequeños pasos cada día. "
                "¿Qué pequeña acción puedes hacer hoy para acercarte a eso que esperas?"
            ],
            "culpable": [
                "Perdonarse a uno mismo es un proceso. Empieza por aceptar que eres humano/a. "
                "Sana no te juzga. ¿Quieres hablar de lo que pasó?",
                "Escribe una carta pidiéndote perdón a ti mismo/a. Suena raro, pero funciona. "
                "Lee la carta en voz alta. Date el perdón que mereces."
            ]
        }

        opciones = sugerencias.get(
            self.ultima_emocion,
            ["¿Qué tal un ejercicio de respiración suave? Siempre ayuda a centrarse y conectar con uno mismo.",
             "A veces lo mejor es simplemente hablar. Sana está aquí para escucharte sin límites.",
             "Date un momento. Solo tú, tu respiración y Sana. Sin prisas, sin expectativas."]
        )
        return random.choice(opciones)

    def limpiar_historial(self):
        """
        Reinicia completamente el historial de la conversación.
        Borra todas las emociones registradas, temas, nivel de confianza
        y vuelve a estado inicial.
        """
        self.historial = []
        self.ultima_emocion = None
        self.contador_interacciones = 0
        self.emociones_detectadas = []
        self.nivel_confianza = 0
        self.temas_recurrentes = []


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Escucha v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: core/escucha.py (v3.0 - Hiper-Evolución)")
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

    e = Escucha()

    # Básicos
    t(isinstance(e, Escucha), "Instancia creada correctamente")
    t(len(e.historial) == 0, "Historial inicia vacío")
    t(e.contador_interacciones == 0, "Contador en 0")
    t(e.nivel_confianza == 0, "Confianza inicial en 0")
    t(e.obtener_emocion_actual() == "neutral", "Emoción inicial: neutral")

    # Saludo
    s = e.obtener_saludo()
    t(isinstance(s, str) and len(s) > 30, f"Saludo válido: '{s[:50]}...'")

    # Detección de emociones (11 emociones)
    t(e.detectar_emocion("estoy muy triste") == "triste", "Detecta tristeza")
    t(e.detectar_emocion("tengo ganas de llorar") == "triste", "Detecta llanto")
    t(e.detectar_emocion("estoy furioso") == "enojado", "Detecta furia")
    t(e.detectar_emocion("qué bronca tengo") == "enojado", "Detecta bronca")
    t(e.detectar_emocion("estoy muy ansioso") == "ansioso", "Detecta ansiedad")
    t(e.detectar_emocion("tengo miedo del examen") == "ansioso", "Detecta miedo")
    t(e.detectar_emocion("estoy muy feliz hoy") == "feliz", "Detecta felicidad")
    t(e.detectar_emocion("aprobé el examen") == "feliz", "Detecta logro")
    t(e.detectar_emocion("me siento muy solo") == "solo", "Detecta soledad")
    t(e.detectar_emocion("nadie me invita a nada") == "solo", "Detecta exclusión")
    t(e.detectar_emocion("estoy agotado") == "cansado", "Detecta cansancio")
    t(e.detectar_emocion("no sé qué hacer con mi vida") == "confundido", "Detecta confusión")
    t(e.detectar_emocion("no soy suficiente para nadie") == "inseguro", "Detecta inseguridad")
    t(e.detectar_emocion("estoy muy agradecido por todo") == "agradecido", "Detecta gratitud")
    t(e.detectar_emocion("tengo esperanza de que mejore") == "esperanzado", "Detecta esperanza")
    t(e.detectar_emocion("me siento culpable por lo que pasó") == "culpable", "Detecta culpa")
    t(e.detectar_emocion("hoy comí pizza") == "neutral", "Texto neutro = neutral")

    # Intensidad
    t(e._detectar_intensidad("estoy triste") == "baja", "Intensidad baja")
    t(e._detectar_intensidad("estoy muy triste") == "media", "Intensidad media")
    t(e._detectar_intensidad("estoy muy muy triste, no soporto esto") == "alta", "Intensidad alta")
    t(e._detectar_intensidad("no puedo más, no soporto esto, es horrible, me muero") == "crisis", "Intensidad crisis")

    # Crisis
    t(e._es_crisis("no puedo más con esto") == True, "Detecta crisis")
    t(e._es_crisis("me quiero morir") == True, "Detecta crisis grave")
    t(e._es_crisis("hoy me siento triste") == False, "No es crisis")

    # Temas
    t(e._extraer_tema("tuve un examen difícil en la escuela") == "escuela", "Tema: escuela")
    t(e._extraer_tema("mi mamá no me entiende") == "familia", "Tema: familia")
    t(e._extraer_tema("mis amigos no me hablaron hoy") == "amigos", "Tema: amigos")
    t(e._extraer_tema("algo random sin tema claro xyz123") == "general", "Tema general")

    # Respuestas
    r = e.responder("estoy muy triste hoy")
    t(isinstance(r, str) and len(r) > 30, f"Respuesta a tristeza: '{r[:50]}...'")

    r = e.responder("me siento muy ansioso por el examen")
    t(len(r) > 30, "Respuesta a ansiedad sustancial")

    r = e.responder("no puedo más, me quiero morir, no soporto esto")
    t(len(r) > 60, "Respuesta a crisis es extensa")

    # Historial
    t(len(e.historial) >= 3, "Historial registra interacciones")
    t("tema" in e.historial[0], "Historial guarda tema")
    t("timestamp" in e.historial[0], "Historial guarda timestamp")

    # Historial emocional
    hist = e.obtener_historial_emocional()
    t("total_interacciones" in hist, "Resumen tiene total")
    t("temas_hablados" in hist, "Resumen tiene temas")
    t("top_3_emociones" in hist, "Resumen tiene top 3 emociones")
    t("emocion_mas_intensa" in hist, "Resumen tiene emoción más intensa")

    # Sugerencia
    e.ultima_emocion = "ansioso"
    s = e.obtener_sugerencia()
    t("respira" in s.lower() or "respir" in s.lower(), "Sugerencia ansiedad menciona respiración")

    # Limpieza
    e.limpiar_historial()
    t(len(e.historial) == 0, "Historial limpio")
    t(e.nivel_confianza == 0, "Confianza 0 tras limpiar")
    t(e.obtener_emocion_actual() == "neutral", "Emoción neutral tras limpiar")

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Escucha v3.0 validada\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()        