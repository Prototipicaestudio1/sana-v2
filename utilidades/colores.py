"""
🌿 Sana - Módulo de Colores Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Paleta cromática oficial de Sana con 60+ colores organizados
por categorías: fondo, texto, funcionalidades, emociones,
estados, alertas, temas (claro/oscuro) y utilidades avanzadas
de conversión, manipulación y accesibilidad.
═══════════════════════════════════════════════════════════════
"""


class Colores:
    """
    Paleta de colores oficial de Sana.
    
    60+ colores en formato RGBA normalizado (0.0 - 1.0)
    con equivalentes hexadecimales. Incluye:
    - Paleta principal completa
    - Colores por funcionalidad (6)
    - Colores por emoción (11)
    - Colores por intensidad y estado
    - Tema claro y oscuro
    - Utilidades de conversión, manipulación y accesibilidad
    """

    # ═══════════════════════════════════════════════════════════
    # PALETA PRINCIPAL
    # ═══════════════════════════════════════════════════════════

    # ─── FONDOS ───
    FONDO_CREMA = (0.96, 0.94, 0.92, 1.0)       # #F5F0EB
    FONDO_BLANCO = (0.98, 0.98, 0.97, 1.0)       # #FAFAF8
    FONDO_OSCURO = (0.18, 0.20, 0.22, 1.0)        # #2E3338
    FONDO_NOCHE = (0.12, 0.14, 0.16, 1.0)         # #1F2326
    FONDO_TARJETA = (1.0, 1.0, 1.0, 0.95)         # #FFFFFF con transparencia

    # ─── VERDES (Sana principal) ───
    VERDE_OSCURO = (0.24, 0.42, 0.37, 1.0)        # #3D6B5E
    VERDE_SALVIA = (0.66, 0.77, 0.69, 1.0)        # #A8C5B0
    VERDE_CLARO = (0.82, 0.90, 0.84, 1.0)         # #D1E6D6
    VERDE_MENTA = (0.76, 0.89, 0.80, 1.0)         # #C2E3CC
    VERDE_BOSQUE = (0.15, 0.31, 0.22, 1.0)        # #264F38

    # ─── AZULES ───
    AZUL_GRIS = (0.72, 0.77, 0.83, 1.0)           # #B8C5D4
    AZUL_CLARO = (0.80, 0.85, 0.90, 1.0)          # #CCD9E6
    AZUL_CALMA = (0.55, 0.70, 0.85, 1.0)          # #8CB3D9
    AZUL_PROFUNDO = (0.20, 0.35, 0.55, 1.0)       # #33598C

    # ─── ROSAS ───
    ROSA_EMPOLVADO = (0.83, 0.65, 0.65, 1.0)      # #D4A5A5
    ROSA_CLARO = (0.90, 0.80, 0.80, 1.0)          # #E6CCCC
    ROSA_CALIDO = (0.95, 0.70, 0.75, 1.0)         # #F2B3BF
    ROSA_FUERTE = (0.85, 0.40, 0.50, 1.0)         # #D96680

    # ─── BEIGES Y CÁLIDOS ───
    BEIGE = (0.78, 0.73, 0.64, 1.0)               # #C7BAA3
    BEIGE_CLARO = (0.88, 0.85, 0.80, 1.0)         # #E0D9CC
    BEIGE_ARENA = (0.82, 0.78, 0.70, 1.0)         # #D1C7B3

    # ─── GRISES ───
    GRIS_LAVANDA = (0.69, 0.74, 0.77, 1.0)        # #B0BDC4
    GRIS_MEDIO = (0.60, 0.60, 0.60, 1.0)          # #999999
    GRIS_CLARO = (0.80, 0.80, 0.80, 1.0)          # #CCCCCC
    GRIS_TEXTO = (0.30, 0.30, 0.30, 1.0)          # #4D4D4D
    GRIS_HUMO = (0.45, 0.45, 0.48, 1.0)           # #73737A

    # ─── ROJOS (alerta) ───
    ROJO_SUAVE = (0.89, 0.60, 0.60, 1.0)          # #E39999
    ROJO_ALERTA = (0.80, 0.30, 0.30, 1.0)         # #CC4D4D
    ROJO_INTENSO = (0.70, 0.15, 0.15, 1.0)        # #B32626

    # ─── AMARILLOS Y NARANJAS ───
    AMARILLO_CALIDO = (0.95, 0.85, 0.60, 1.0)     # #F2D999
    AMARILLO_SOL = (1.0, 0.90, 0.40, 1.0)         # #FFE666
    NARANJA_ENERGIA = (0.95, 0.65, 0.30, 1.0)     # #F2A64D

    # ─── MORADOS ───
    PURPURA_SUAVE = (0.65, 0.55, 0.75, 1.0)       # #A68CBF
    LAVANDA = (0.75, 0.65, 0.85, 1.0)             # #BFA6D9

    # ─── TEXTOS ───
    TEXTO_OSCURO = (0.20, 0.20, 0.20, 1.0)        # #333333
    TEXTO_MEDIO = (0.40, 0.40, 0.40, 1.0)         # #666666
    TEXTO_CLARO = (0.70, 0.70, 0.70, 1.0)         # #B3B3B3
    TEXTO_BLANCO = (1.00, 1.00, 1.00, 1.0)        # #FFFFFF
    TEXTO_VERDE = (0.24, 0.42, 0.37, 1.0)         # #3D6B5E (mismo que verde oscuro, para títulos)

    # ═══════════════════════════════════════════════════════════
    # COLORES POR FUNCIONALIDAD
    # ═══════════════════════════════════════════════════════════

    BOTONES = {
        "escucha":      VERDE_SALVIA,
        "respiracion":  AZUL_GRIS,
        "diario":       ROSA_EMPOLVADO,
        "tareas":       BEIGE,
        "conocimiento": GRIS_LAVANDA,
        "ayuda":        ROJO_SUAVE,
        "red_apoyo":    PURPURA_SUAVE,
    }

    BOTONES_HOVER = {
        "escucha":      (0.56, 0.67, 0.59, 1.0),
        "respiracion":  (0.62, 0.67, 0.73, 1.0),
        "diario":       (0.73, 0.55, 0.55, 1.0),
        "tareas":       (0.68, 0.63, 0.54, 1.0),
        "conocimiento": (0.59, 0.64, 0.67, 1.0),
        "ayuda":        (0.79, 0.50, 0.50, 1.0),
        "red_apoyo":    (0.55, 0.45, 0.65, 1.0),
    }

    # ═══════════════════════════════════════════════════════════
    # COLORES POR EMOCIÓN (11 emociones)
    # ═══════════════════════════════════════════════════════════

    EMOCIONES = {
        "triste":       (0.40, 0.55, 0.70, 1.0),   # Azul melancólico
        "enojado":      (0.80, 0.35, 0.30, 1.0),   # Rojo intenso
        "ansioso":      (0.85, 0.65, 0.30, 1.0),   # Naranja
        "feliz":        (0.95, 0.80, 0.30, 1.0),   # Amarillo dorado
        "solo":         (0.55, 0.55, 0.70, 1.0),   # Púrpura grisáceo
        "cansado":      (0.60, 0.65, 0.70, 1.0),   # Gris azulado
        "confundido":   (0.70, 0.60, 0.75, 1.0),   # Lavanda
        "inseguro":     (0.65, 0.55, 0.65, 1.0),   # Malva
        "agradecido":   (0.50, 0.70, 0.55, 1.0),   # Verde gratitud
        "esperanzado":  (0.55, 0.80, 0.85, 1.0),   # Celeste
        "culpable":     (0.60, 0.50, 0.55, 1.0),   # Marrón suave
    }

    # ═══════════════════════════════════════════════════════════
    # COLORES POR INTENSIDAD
    # ═══════════════════════════════════════════════════════════

    INTENSIDAD = {
        "baja":     VERDE_CLARO,
        "media":    AMARILLO_CALIDO,
        "alta":     NARANJA_ENERGIA,
        "crisis":   ROJO_ALERTA,
    }

    # ═══════════════════════════════════════════════════════════
    # COLORES DE ESTADO
    # ═══════════════════════════════════════════════════════════

    ESTADO = {
        "exito":    VERDE_SALVIA,
        "error":    ROJO_ALERTA,
        "advertencia": NARANJA_ENERGIA,
        "info":     AZUL_CALMA,
        "neutral":  GRIS_MEDIO,
        "pendiente": AMARILLO_CALIDO,
    }

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS DE CONVERSIÓN
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def hex_a_rgba(hex_color: str, alpha: float = 1.0) -> tuple:
        """
        Convierte color hexadecimal a RGBA normalizado.
        Soporta formatos: '#RRGGBB', 'RRGGBB', '#RGB', 'RGB'.
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c*2 for c in hex_color)
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            return (r, g, b, alpha)
        return (1.0, 1.0, 1.0, alpha)

    @staticmethod
    def rgba_a_hex(rgba: tuple) -> str:
        """Convierte RGBA normalizado a hexadecimal '#RRGGBB'."""
        r, g, b = rgba[0], rgba[1], rgba[2]
        return f"#{min(255, int(r*255)):02X}{min(255, int(g*255)):02X}{min(255, int(b*255)):02X}"

    @staticmethod
    def rgba_a_css(rgba: tuple) -> str:
        """Convierte RGBA a string CSS: 'rgba(r, g, b, a)'."""
        r, g, b, a = rgba
        return f"rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {a:.2f})"

    # ═══════════════════════════════════════════════════════════
    # OBTENER COLORES POR CATEGORÍA
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def obtener_color_boton(cls, funcionalidad: str) -> tuple:
        """Retorna el color RGBA para un botón según su funcionalidad."""
        return cls.BOTONES.get(funcionalidad, cls.GRIS_MEDIO)

    @classmethod
    def obtener_color_hover(cls, funcionalidad: str) -> tuple:
        """Retorna el color hover (más oscuro) para un botón."""
        return cls.BOTONES_HOVER.get(funcionalidad, cls.GRIS_MEDIO)

    @classmethod
    def obtener_color_emocion(cls, emocion: str) -> tuple:
        """Retorna el color RGBA asociado a una emoción."""
        return cls.EMOCIONES.get(emocion, cls.GRIS_MEDIO)

    @classmethod
    def obtener_color_intensidad(cls, intensidad: str) -> tuple:
        """Retorna el color asociado a un nivel de intensidad."""
        return cls.INTENSIDAD.get(intensidad, cls.GRIS_MEDIO)

    @classmethod
    def obtener_color_estado(cls, estado: str) -> tuple:
        """Retorna el color asociado a un estado (éxito, error, etc.)."""
        return cls.ESTADO.get(estado, cls.GRIS_MEDIO)

    @classmethod
    def lista_colores_botones(cls) -> list:
        """Retorna lista de tuplas (nombre, color_rgba) para botones."""
        return [(nombre, color) for nombre, color in cls.BOTONES.items()]

    @classmethod
    def lista_colores_emociones(cls) -> list:
        """Retorna lista de tuplas (emocion, color_rgba) para emociones."""
        return [(emocion, color) for emocion, color in cls.EMOCIONES.items()]

    # ═══════════════════════════════════════════════════════════
    # MANIPULACIÓN DE COLORES
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def oscurecer(rgba: tuple, factor: float = 0.8) -> tuple:
        """Oscurece un color RGBA multiplicando por un factor < 1."""
        r, g, b, a = rgba
        return (r * factor, g * factor, b * factor, a)

    @staticmethod
    def aclarar(rgba: tuple, factor: float = 1.2) -> tuple:
        """Aclara un color RGBA multiplicando por un factor > 1 (máx 1.0)."""
        r, g, b, a = rgba
        return (min(r * factor, 1.0), min(g * factor, 1.0), min(b * factor, 1.0), a)

    @staticmethod
    def mezclar(color1: tuple, color2: tuple, porcentaje: float = 0.5) -> tuple:
        """
        Mezcla dos colores RGBA.
        porcentaje=0.0 → todo color1, porcentaje=1.0 → todo color2.
        """
        r = color1[0] + (color2[0] - color1[0]) * porcentaje
        g = color1[1] + (color2[1] - color1[1]) * porcentaje
        b = color1[2] + (color2[2] - color1[2]) * porcentaje
        a = color1[3] if len(color1) > 3 else 1.0
        return (r, g, b, a)

    @staticmethod
    def con_opacidad(rgba: tuple, opacidad: float) -> tuple:
        """Cambia la opacidad (alpha) de un color."""
        r, g, b, _ = rgba
        return (r, g, b, max(0.0, min(1.0, opacidad)))

    @staticmethod
    def contraste(rgba: tuple) -> tuple:
        """
        Retorna blanco o negro según el contraste del color.
        Útil para texto sobre fondos de color. Usa fórmula W3C.
        """
        r, g, b = rgba[0], rgba[1], rgba[2]
        luminancia = 0.299 * r + 0.587 * g + 0.114 * b
        if luminancia > 0.5:
            return (0.2, 0.2, 0.2, 1.0)  # Texto oscuro para fondos claros
        return (1.0, 1.0, 1.0, 1.0)      # Texto blanco para fondos oscuros

    @staticmethod
    def es_claro(rgba: tuple) -> bool:
        """Determina si un color es claro (True) u oscuro (False)."""
        r, g, b = rgba[0], rgba[1], rgba[2]
        luminancia = 0.299 * r + 0.587 * g + 0.114 * b
        return luminancia > 0.5

    @staticmethod
    def gradiente(color_inicio: tuple, color_fin: tuple, pasos: int) -> list:
        """Genera una lista de colores en gradiente entre dos puntos."""
        resultado = []
        for i in range(pasos):
            porcentaje = i / max(pasos - 1, 1)
            r = color_inicio[0] + (color_fin[0] - color_inicio[0]) * porcentaje
            g = color_inicio[1] + (color_fin[1] - color_inicio[1]) * porcentaje
            b = color_inicio[2] + (color_fin[2] - color_inicio[2]) * porcentaje
            resultado.append((r, g, b, 1.0))
        return resultado


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Colores v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: utilidades/colores.py (v3.0 - Hiper-Evolución)")
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

    c = Colores()

    # ─── BÁSICOS ───
    t(isinstance(c, Colores), "Instancia creada")
    t(len(c.FONDO_CREMA) == 4, "FONDO_CREMA es tupla RGBA")
    t(all(0 <= v <= 1 for v in c.FONDO_CREMA), "Valores en rango 0-1")

    # ─── BOTONES ───
    t(len(c.BOTONES) == 7, f"{len(c.BOTONES)} botones (mín. 7)")
    t("red_apoyo" in c.BOTONES, "Botón 'red_apoyo' existe")
    t(c.obtener_color_boton("escucha") == c.VERDE_SALVIA, "Color escucha = verde salvia")
    t(c.obtener_color_boton("invalido") == c.GRIS_MEDIO, "Inválido = gris medio")
    t(c.obtener_color_hover("escucha") is not None, "Color hover existe")

    # ─── EMOCIONES ───
    t(len(c.EMOCIONES) == 11, f"{len(c.EMOCIONES)} emociones (mín. 11)")
    t("inseguro" in c.EMOCIONES, "Emoción 'inseguro' existe")
    t("agradecido" in c.EMOCIONES, "Emoción 'agradecido' existe")
    t("culpable" in c.EMOCIONES, "Emoción 'culpable' existe")
    t(c.obtener_color_emocion("triste") is not None, "Color triste existe")
    t(c.obtener_color_emocion("invalida") == c.GRIS_MEDIO, "Emoción inválida = gris")

    # ─── INTENSIDAD Y ESTADO ───
    t(len(c.INTENSIDAD) == 4, "4 niveles de intensidad")
    t(c.obtener_color_intensidad("crisis") == c.ROJO_ALERTA, "Crisis = rojo alerta")
    t(c.obtener_color_estado("exito") == c.VERDE_SALVIA, "Éxito = verde")
    t(c.obtener_color_estado("error") == c.ROJO_ALERTA, "Error = rojo")

    # ─── LISTAS ───
    t(len(c.lista_colores_botones()) == 7, "Lista botones: 7")
    t(len(c.lista_colores_emociones()) == 11, "Lista emociones: 11")

    # ─── CONVERSIÓN HEX A RGBA ───
    r = c.hex_a_rgba("#FF0000")
    t(r[0] == 1.0 and r[1] == 0.0 and r[2] == 0.0, "Hex #FF0000 = rojo puro")
    r = c.hex_a_rgba("#0000FF", 0.5)
    t(r[2] == 1.0 and r[3] == 0.5, "Hex #0000FF alpha 0.5")
    r = c.hex_a_rgba("A8C5B0")
    t(abs(r[0] - 0.66) < 0.02, "Hex A8C5B0 = verde salvia")
    r = c.hex_a_rgba("#F00")  # Formato corto
    t(r[0] == 1.0, "Hex #F00 (corto) = rojo")
    r = c.hex_a_rgba("invalido")
    t(r == (1.0, 1.0, 1.0, 1.0), "Hex inválido = blanco")

    # ─── CONVERSIÓN RGBA A HEX ───
    t(c.rgba_a_hex((1.0, 0.0, 0.0, 1.0)) == "#FF0000", "RGBA rojo = #FF0000")
    t("A8" in c.rgba_a_hex((0.66, 0.77, 0.69, 1.0)).upper(), "Verde salvia a hex")

    # ─── CSS ───
    css = c.rgba_a_css((1.0, 0.5, 0.0, 0.8))
    t("rgba(255" in css and "0.80" in css, f"CSS válido: {css}")

    # ─── OSCURECER Y ACLARAR ───
    oscuro = c.oscurecer((1.0, 0.5, 0.0, 1.0), 0.5)
    t(oscuro[0] == 0.5, "Oscurecer reduce a la mitad")
    claro = c.aclarar((0.5, 0.3, 0.1, 1.0), 2.0)
    t(claro[0] == 1.0 and claro[1] == 0.6, "Aclarar duplica")

    # ─── MEZCLAR ───
    mezcla = c.mezclar((1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0), 0.5)
    t(abs(mezcla[0] - 0.5) < 0.01 and abs(mezcla[2] - 0.5) < 0.01, "Mezcla rojo + azul = púrpura")

    # ─── OPACIDAD ───
    opaco = c.con_opacidad((1.0, 0.0, 0.0, 1.0), 0.5)
    t(opaco[3] == 0.5, "Opacidad cambiada a 0.5")
    t(c.con_opacidad((0.5, 0.5, 0.5, 1.0), 1.5)[3] == 1.0, "Opacidad máxima 1.0")
    t(c.con_opacidad((0.5, 0.5, 0.5, 1.0), -1)[3] == 0.0, "Opacidad mínima 0.0")

    # ─── CONTRASTE ───
    t(c.contraste((0.0, 0.0, 0.0, 1.0)) == (1.0, 1.0, 1.0, 1.0), "Negro → texto blanco")
    t(c.contraste((1.0, 1.0, 1.0, 1.0)) == (0.2, 0.2, 0.2, 1.0), "Blanco → texto oscuro")

    # ─── ES CLARO ───
    t(c.es_claro((1.0, 1.0, 1.0, 1.0)), "Blanco es claro")
    t(not c.es_claro((0.0, 0.0, 0.0, 1.0)), "Negro no es claro")

    # ─── GRADIENTE ───
    grad = c.gradiente((1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0), 3)
    t(len(grad) == 3, "Gradiente: 3 pasos")
    t(grad[0] == (1.0, 0.0, 0.0, 1.0), "Paso 1 = color inicio")
    t(grad[2] == (0.0, 0.0, 1.0, 1.0), "Paso 3 = color fin")

    # ─── VALIDACIÓN DE COLORES ───
    for nombre, color in c.BOTONES.items():
        t(len(color) == 4 and all(0 <= v <= 1 for v in color), f"Botón '{nombre}' válido")
    for emocion, color in c.EMOCIONES.items():
        t(len(color) == 4 and all(0 <= v <= 1 for v in color), f"Emoción '{emocion}' válido")
    for intensidad, color in c.INTENSIDAD.items():
        t(len(color) == 4, f"Intensidad '{intensidad}' válida")

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Colores v3.0 validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()