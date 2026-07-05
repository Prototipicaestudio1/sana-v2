"""
🌿 Sana - Módulo de Arte ASCII Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Colección completa de arte ASCII, emojis, caritas, banners,
animaciones, separadores, cajas de texto y decoraciones
visuales para la interfaz de consola de Sana.
═══════════════════════════════════════════════════════════════
"""

import random


class ASCIIArt:
    """
    Galería visual de Sana.
    
    Contiene:
    - 3 logos (Sana, flor, corazón)
    - 10+ separadores decorativos
    - 14 caritas para emociones
    - 10 iconos de funcionalidades
    - Banners para bienvenida, ejercicios, secciones
    - Animaciones (respiración, carga, corazón latiendo, estrellas)
    - Cajas de texto enmarcadas
    - Listas decoradas
    - Barras de progreso ASCII
    - Mensajes especiales (cumpleaños, logros, ánimo)
    """

    # ═══════════════════════════════════════════════════════════
    # LOGOS
    # ═══════════════════════════════════════════════════════════

    LOGO_SANA = r"""
    ╔══════════════════════╗
    ║                      ║
    ║     ~  S A N A  ~    ║
    ║   Tu espacio seguro  ║
    ║                      ║
    ╚══════════════════════╝
    """

    LOGO_SANA_EXTENDIDO = r"""
         ___________
        /           \
       /   🌿 S A N A \
      /   Tu espacio   \
     /     seguro       \
    /___________________\
    """

    LOGO_FLOR = r"""
       _
     _(_)_
    (_)@(_)
      (_)
    \|/ \|/
     |   |
    """

    LOGO_CORAZON = r"""
      ♥♥♥    ♥♥♥
     ♥   ♥  ♥   ♥
     ♥    ♥♥    ♥
      ♥        ♥
       ♥      ♥
        ♥    ♥
         ♥  ♥
          ♥♥
    """

    # ═══════════════════════════════════════════════════════════
    # SEPARADORES
    # ═══════════════════════════════════════════════════════════

    SEPARADOR_SIMPLE = "─" * 40
    SEPARADOR_DOBLE = "═" * 40
    SEPARADOR_PUNTOS = "• " * 20
    SEPARADOR_ONDAS = "~" * 40
    SEPARADOR_CORAZONES = "♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡"
    SEPARADOR_ESTRELLAS = "★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆"
    SEPARADOR_FLECHAS = "→ ← → ← → ← → ← → ←"
    SEPARADOR_LINEAS = "│ │ │ │ │ │ │ │ │ │"
    SEPARADOR_GUIONES = "- - - - - - - - - -"
    SEPARADOR_PUNTOS_SUSPENSIVOS = "· · · · · · · · · ·"

    # ═══════════════════════════════════════════════════════════
    # CARITAS (14 emociones)
    # ═══════════════════════════════════════════════════════════

    CARITAS = {
        "feliz":      "(◕‿◕)",
        "triste":     "(╥_╥)",
        "enojado":    "(◣_◢)",
        "ansioso":    "(⊙﹏⊙)",
        "solo":       "(._.)",
        "cansado":    "(￣▽￣)💤",
        "confundido": "(•_•)?",
        "calma":      "(￣︶￣)",
        "motivado":   "(•̀ᴗ•́)و",
        "agradecido": "(｡♥‿♥｡)",
        "inseguro":   "(｡•́︿•̀｡)",
        "esperanzado":"(✿◠‿◠)",
        "culpable":   "(｡•́︿•̀｡)💧",
        "neutral":    "(•_•)",
        "amor":       "(♡˙︶˙♡)",
        "orgulloso":  "(￣ω￣)",
        "sorprendido":"(⊙⊙)",
        "pensativo":  "(￣～￣)",
        "aliviado":   "(´▽｀)",
        "travieso":   "(￢‿￢)",
    }

    # ═══════════════════════════════════════════════════════════
    # ICONOS DE FUNCIONALIDADES
    # ═══════════════════════════════════════════════════════════

    ICONOS = {
        "escucha":      "🎧",
        "respiracion":  "🌬️",
        "diario":       "📔",
        "tareas":       "📅",
        "conocimiento": "🧠",
        "ayuda":        "🆘",
        "red_apoyo":    "🤝",
        "menu":         "🏠",
        "volver":       "⬅️",
        "config":       "⚙️",
        "salir":        "👋",
        "guardar":      "💾",
        "editar":       "✏️",
        "eliminar":     "🗑️",
        "favorito":     "⭐",
        "completado":   "✅",
        "pendiente":    "⏳",
        "alerta":       "🚨",
    }

    # ═══════════════════════════════════════════════════════════
    # BANNERS
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def banner_bienvenida(cls) -> str:
        return f"""
{cls.SEPARADOR_DOBLE}
{cls.LOGO_SANA}
{cls.SEPARADOR_DOBLE}
🌿 Bienvenida/o a tu espacio seguro. Sana está aquí para ti.
{cls.SEPARADOR_DOBLE}
        """

    @classmethod
    def banner_ejercicio(cls, nombre: str, descripcion: str = "") -> str:
        banner = f"""
{cls.SEPARADOR_ONDAS}
  🌬️  {nombre}
{cls.SEPARADOR_ONDAS}
        """
        if descripcion:
            banner += f"\n  {descripcion}\n"
        return banner

    @classmethod
    def banner_seccion(cls, icono: str, titulo: str) -> str:
        return f"""
{cls.SEPARADOR_SIMPLE}
  {icono}  {titulo}
{cls.SEPARADOR_SIMPLE}
        """

    @classmethod
    def banner_logro(cls, texto: str) -> str:
        return f"""
{cls.SEPARADOR_ESTRELLAS}
  🎉  {texto}  🎉
{cls.SEPARADOR_ESTRELLAS}
        """

    @classmethod
    def banner_alerta(cls, texto: str) -> str:
        return f"""
{cls.SEPARADOR_DOBLE}
  🚨  {texto}
{cls.SEPARADOR_DOBLE}
        """

    # ═══════════════════════════════════════════════════════════
    # ANIMACIONES
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def animacion_respiracion() -> list:
        """Frames para animación de respiración (expansión/contracción)."""
        return [
            "  (       )",
            "  (  ●  )",
            "  (  ●  )",
            "  ( ●● )",
            "  ( ●● )",
            "  ( ●● )",
            "  (  ●  )",
            "  (  ●  )",
            "  (       )",
        ]

    @staticmethod
    def animacion_carga(frames: int = 10) -> list:
        """Frames de barra de carga."""
        return [
            "[■□□□□□□□□□] 10%",
            "[■■□□□□□□□□] 20%",
            "[■■■□□□□□□□] 30%",
            "[■■■■□□□□□□] 40%",
            "[■■■■■□□□□□] 50%",
            "[■■■■■■□□□□] 60%",
            "[■■■■■■■□□□] 70%",
            "[■■■■■■■■□□] 80%",
            "[■■■■■■■■■□] 90%",
            "[■■■■■■■■■■] 100%",
        ][:frames]

    @staticmethod
    def animacion_corazon() -> list:
        """Frames de corazón latiendo."""
        return [
            "  ♡   ♡  ",
            " ♡ ♡ ♡ ♡ ",
            "♡  ♡  ♡  ♡",
            " ♡ ♡ ♡ ♡ ",
            "  ♡   ♡  ",
            "   ♡ ♡   ",
            "    ♡    ",
        ]

    @staticmethod
    def animacion_estrellas() -> list:
        """Frames de estrellas titilando."""
        return [
            "  ★  ·  ☆  ·  ★  ",
            "  ·  ★  ·  ☆  ·  ",
            "  ☆  ·  ★  ·  ☆  ",
            "  ·  ☆  ·  ★  ·  ",
        ]

    @staticmethod
    def animacion_pensando() -> list:
        """Frames de puntos suspensivos animados."""
        return [
            "Pensando   ",
            "Pensando.  ",
            "Pensando.. ",
            "Pensando...",
        ]

    # ═══════════════════════════════════════════════════════════
    # CAJAS DE TEXTO
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def caja_texto(cls, texto: str, ancho: int = 40, titulo: str = "") -> str:
        """
        Encierra texto en una caja decorativa.
        Soporta múltiples líneas y título opcional.
        """
        lineas = texto.split('\n')
        borde_superior = "┌" + "─" * (ancho - 2) + "┐"
        borde_inferior = "└" + "─" * (ancho - 2) + "┘"
        
        resultado = [borde_superior]
        if titulo:
            resultado.append("│ " + f"📌 {titulo}".ljust(ancho - 2) + "│")
            resultado.append("│" + "─" * (ancho - 2) + "│")
        for linea in lineas:
            # Dividir líneas largas
            while len(linea) > ancho - 4:
                resultado.append("│ " + linea[:ancho - 4].ljust(ancho - 4) + " │")
                linea = linea[ancho - 4:]
            resultado.append("│ " + linea.ljust(ancho - 4) + " │")
        resultado.append(borde_inferior)
        return "\n".join(resultado)

    @classmethod
    def caja_destacada(cls, texto: str, ancho: int = 40) -> str:
        """Caja con bordes dobles para destacar información importante."""
        lineas = texto.split('\n')
        borde_s = "╔" + "═" * (ancho - 2) + "╗"
        borde_i = "╚" + "═" * (ancho - 2) + "╝"
        resultado = [borde_s]
        for linea in lineas:
            resultado.append("║ " + linea.center(ancho - 4) + " ║")
        resultado.append(borde_i)
        return "\n".join(resultado)

    @classmethod
    def caja_redondeada(cls, texto: str, ancho: int = 40) -> str:
        """Caja con bordes redondeados, más amigable."""
        lineas = texto.split('\n')
        borde_s = "╭" + "─" * (ancho - 2) + "╮"
        borde_i = "╰" + "─" * (ancho - 2) + "╯"
        resultado = [borde_s]
        for linea in lineas:
            resultado.append("│ " + linea.ljust(ancho - 4) + " │")
        resultado.append(borde_i)
        return "\n".join(resultado)

    # ═══════════════════════════════════════════════════════════
    # LISTAS Y VIÑETAS
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def lista_decorada(cls, items: list, viñeta: str = "•", numerada: bool = False) -> str:
        """Formatea una lista con viñetas o numeración."""
        resultado = []
        for i, item in enumerate(items, 1):
            if numerada:
                resultado.append(f"  {i}. {item}")
            else:
                resultado.append(f"  {viñeta} {item}")
        return "\n".join(resultado)

    @classmethod
    def menu_opciones(cls, opciones: list, iconos: list = None) -> str:
        """
        Formatea un menú de opciones con iconos.
        
        Args:
            opciones: Lista de textos.
            iconos: Lista de iconos (mismo orden que opciones).
        """
        resultado = []
        for i, opcion in enumerate(opciones, 1):
            icono = iconos[i-1] if iconos and i-1 < len(iconos) else "•"
            resultado.append(f"  {i}. {icono}  {opcion}")
        return "\n".join(resultado)

    # ═══════════════════════════════════════════════════════════
    # BARRAS DE PROGRESO
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def barra_progreso(porcentaje: int, ancho: int = 20, 
                       lleno: str = "█", vacio: str = "░") -> str:
        """Genera una barra de progreso: [████░░░░░░] 40%"""
        porcentaje = max(0, min(100, porcentaje))
        lleno_count = int((porcentaje / 100) * ancho)
        vacio_count = ancho - lleno_count
        return f"[{lleno * lleno_count}{vacio * vacio_count}] {porcentaje}%"

    @staticmethod
    def barra_salud(carga: int, maximo: int = 5) -> str:
        """Barra de carga mental: [★★★★☆] 4/5"""
        carga = max(0, min(maximo, carga))
        return f"[{'★' * carga}{'☆' * (maximo - carga)}] {carga}/{maximo}"

    @staticmethod
    def barra_racha(dias: int) -> str:
        """Barra de racha de días: 🔥🔥🔥 3 días"""
        if dias <= 0:
            return "Sin racha aún 🌱"
        return f"{'🔥' * min(dias, 10)} {dias} día(s)"

    # ═══════════════════════════════════════════════════════════
    # MENSAJES ESPECIALES
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def mensaje_animo(cls) -> str:
        """Retorna un mensaje de ánimo aleatorio decorado."""
        mensajes = [
            "¡Tú puedes con esto! 💪",
            "Un día a la vez 🌅",
            "Eres más fuerte de lo que crees ⭐",
            "Respira hondo, esto pasará 🌬️",
            "No estás solo/a 🤝",
            "Cada paso cuenta 👣",
            "Confía en el proceso 🌱",
            "Eres suficiente, siempre lo has sido 💜",
        ]
        return random.choice(mensajes)

    @classmethod
    def mensaje_logro(cls, logro: str) -> str:
        """Mensaje decorado para celebrar un logro."""
        return f"""
{cls.SEPARADOR_ESTRELLAS}
  🎉  ¡LO LOGRASTE!
  {logro}
  Sana está orgullosa de ti 💚
{cls.SEPARADOR_ESTRELLAS}
        """

    @classmethod
    def mensaje_cumpleanos(cls, nombre: str = "") -> str:
        """Mensaje especial de cumpleaños."""
        return f"""
{cls.SEPARADOR_CORAZONES}
  🎂  ¡FELIZ CUMPLEAÑOS{f' {nombre}' if nombre else ''}!  🎂
  Que tengas un día maravilloso lleno de alegría.
  Te mereces todo lo bueno que te pase hoy y siempre. 💝
{cls.SEPARADOR_CORAZONES}
        """

    @classmethod
    def mensaje_buenas_noches(cls) -> str:
        """Mensaje de buenas noches decorado."""
        return f"""
{cls.SEPARADOR_ONDAS}
  🌙  Buenas noches
  Deja ir lo que pasó hoy. Mañana será un nuevo día.
  Descansa, sueña bonito. Sana te cuida. 💤
{cls.SEPARADOR_ONDAS}
        """

    # ═══════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def carita_para_emocion(cls, emocion: str) -> str:
        """Retorna la carita ASCII correspondiente a una emoción."""
        return cls.CARITAS.get(emocion, cls.CARITAS["neutral"])

    @classmethod
    def icono_para_funcionalidad(cls, funcionalidad: str) -> str:
        """Retorna el icono para una funcionalidad."""
        return cls.ICONOS.get(funcionalidad, "•")

    @classmethod
    def obtener_separador_aleatorio(cls) -> str:
        """Retorna un separador aleatorio para variedad visual."""
        separadores = [
            cls.SEPARADOR_SIMPLE, cls.SEPARADOR_DOBLE, cls.SEPARADOR_PUNTOS,
            cls.SEPARADOR_ONDAS, cls.SEPARADOR_CORAZONES, cls.SEPARADOR_ESTRELLAS,
        ]
        return random.choice(separadores)

    @classmethod
    def centrar_texto(cls, texto: str, ancho: int = 40) -> str:
        """Centra un texto en un ancho determinado."""
        return texto.center(ancho)

    @classmethod
    def subrayar(cls, texto: str, caracter: str = "─") -> str:
        """Subraya un texto."""
        return f"{texto}\n{caracter * len(texto)}"


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para ASCIIArt v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: assets/ascii_art.py (v3.0 - Galería Visual)")
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

    a = ASCIIArt()
    t(isinstance(a, ASCIIArt), "Instancia creada")

    # Logos
    t("S A N A" in a.LOGO_SANA, "Logo contiene 'S A N A'")
    t("espacio seguro" in a.LOGO_SANA, "Logo contiene 'espacio seguro'")
    t(len(a.LOGO_SANA_EXTENDIDO) > 30, "Logo extendido existe")
    t(len(a.LOGO_FLOR) > 10, "Logo flor existe")
    t(len(a.LOGO_CORAZON) > 10, "Logo corazón existe")

    # Separadores
    t(len(a.SEPARADOR_SIMPLE) == 40, "Separador simple: 40 caracteres")
    t(len(a.SEPARADOR_DOBLE) == 40, "Separador doble: 40 caracteres")
    t(len(a.obtener_separador_aleatorio()) > 10, "Separador aleatorio funciona")

    # Caritas
    t(len(a.CARITAS) >= 14, f"{len(a.CARITAS)} caritas (mín. 14)")
    t(a.carita_para_emocion("feliz") == "(◕‿◕)", "Carita feliz correcta")
    t(a.carita_para_emocion("triste") == "(╥_╥)", "Carita triste correcta")
    t(a.carita_para_emocion("inseguro") == "(｡•́︿•̀｡)", "Carita inseguro correcta")
    t(a.carita_para_emocion("inexistente") == "(•_•)", "Emoción inexistente: neutral")

    # Iconos
    t(len(a.ICONOS) >= 12, f"{len(a.ICONOS)} iconos (mín. 12)")
    t(a.icono_para_funcionalidad("red_apoyo") == "🤝", "Icono red_apoyo existe")
    t(a.icono_para_funcionalidad("inexistente") == "•", "Funcionalidad inexistente: bullet")

    # Banners
    banner = a.banner_bienvenida()
    t("S A N A" in banner, "Banner bienvenida contiene 'S A N A'")
    banner = a.banner_ejercicio("4-7-8", "Para ansiedad")
    t("4-7-8" in banner and "ansiedad" in banner, "Banner ejercicio con descripción")
    banner = a.banner_seccion("📔", "Diario")
    t("📔" in banner and "Diario" in banner, "Banner sección correcto")
    banner = a.banner_logro("Racha de 7 días")
    t("🎉" in banner and "Racha" in banner, "Banner logro correcto")
    banner = a.banner_alerta("Crisis detectada")
    t("🚨" in banner and "Crisis" in banner, "Banner alerta correcto")

    # Animaciones
    frames = a.animacion_respiracion()
    t(len(frames) == 9, "Animación respiración: 9 frames")
    frames = a.animacion_carga(5)
    t(len(frames) == 5, "Animación carga: 5 frames")
    t("[" in frames[0], "Frames contienen '['")
    frames = a.animacion_corazon()
    t(len(frames) == 7, "Animación corazón: 7 frames")
    frames = a.animacion_estrellas()
    t(len(frames) == 4, "Animación estrellas: 4 frames")
    frames = a.animacion_pensando()
    t(len(frames) == 4, "Animación pensando: 4 frames")

    # Cajas de texto
    caja = a.caja_texto("Hola mundo", 20)
    t("┌" in caja and "└" in caja, "Caja texto con bordes")
    t("Hola mundo" in caja, "Caja contiene el texto")
    caja = a.caja_texto("Test", 20, titulo="Prueba")
    t("Prueba" in caja, "Caja con título")
    caja = a.caja_destacada("Importante", 25)
    t("╔" in caja and "╚" in caja, "Caja destacada con bordes dobles")
    caja = a.caja_redondeada("Amigable", 25)
    t("╭" in caja and "╰" in caja, "Caja redondeada")

    # Listas
    lista = a.lista_decorada(["Uno", "Dos", "Tres"])
    t("• Uno" in lista and "• Tres" in lista, "Lista con viñetas")
    lista_num = a.lista_decorada(["A", "B", "C"], numerada=True)
    t("1. A" in lista_num and "3. C" in lista_num, "Lista numerada")
    menu = a.menu_opciones(["Hablar", "Respirar"], ["💬", "🌬️"])
    t("1. 💬" in menu and "2. 🌬️" in menu, "Menú con iconos")

    # Barras
    barra = a.barra_progreso(50, 10)
    t("50%" in barra, "Barra progreso: 50%")
    barra = a.barra_salud(4, 5)
    t("4/5" in barra and "★★★★" in barra, "Barra salud: 4/5")
    barra = a.barra_racha(5)
    t("🔥" in barra and "5 día" in barra, "Barra racha: 5 días")
    barra = a.barra_racha(0)
    t("Sin racha" in barra, "Barra racha: sin racha")

    # Mensajes especiales
    animo = a.mensaje_animo()
    t(len(animo) > 5, "Mensaje de ánimo válido")
    logro = a.mensaje_logro("Completaste todas tus tareas")
    t("LO LOGRASTE" in logro, "Mensaje logro contiene título")
    cumple = a.mensaje_cumpleanos("Mariana")
    t("Mariana" in cumple and "FELIZ" in cumple, "Mensaje cumpleaños personalizado")
    noches = a.mensaje_buenas_noches()
    t("Buenas noches" in noches and "🌙" in noches, "Mensaje buenas noches")

    # Utilidades
    centrado = a.centrar_texto("Sana", 20)
    t(len(centrado) == 20, "Texto centrado")
    sub = a.subrayar("Título", "=")
    t("Título" in sub and "======" in sub, "Texto subrayado")

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - ASCIIArt v3.0 validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()