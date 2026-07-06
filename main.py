"""
🌿 SANA v2.0 - Servidor con APIs Reales
Conecta todos los módulos Python con el frontend HTML
"""

import os, sys, json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.respiracion import Respiracion
from core.escucha import Escucha
from api.lineas_ayuda import LineasAyuda
from api.ia_chat import IAChat
from zonas.diario import Diario
from zonas.alertas import Alertas
from zonas.bitacora import Bitacora
from zonas.organizador import Organizador
from zonas.conocimiento import Conocimiento

respiracion = Respiracion()
escucha = Escucha()
lineas_ayuda = LineasAyuda()
ia_chat = IAChat()
diario = Diario()
alertas = Alertas()
bitacora = Bitacora()
organizador = Organizador()
conocimiento = Conocimiento()

PUERTO = int(os.environ.get('PORT', 8080))


class SanaHandler(SimpleHTTPRequestHandler):

    def json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length:
            body = self.rfile.read(length).decode()
            return parse_qs(body)
        return {}

    def do_GET(self):
        p = urlparse(self.path)
        path = p.path
        qs = parse_qs(p.query)

        def q(key, default=''):
            return qs.get(key, [default])[0]

        # ──── STATS ────
        if path == '/api/stats':
            return self.json({
                "tests": 983, "modulos": 27, "emociones": 11,
                "ejercicios": 7, "lineas_ayuda": 45, "version": "2.0",
                "status": "online"
            })

        # ──── RESPIRACIÓN: Lista ejercicios ────
        if path == '/api/respiracion/lista':
            ejercicios = []
            for clave, ej in respiracion.EJERCICIOS.items():
                ejercicios.append({
                    "clave": clave, "nombre": ej["nombre"],
                    "descripcion": ej["descripcion"], "beneficio": ej["beneficio"],
                    "nivel": ej["nivel"], "ciclos": ej["ciclos"],
                    "visualizacion": ej["visualizacion"],
                    "emocion_ideal": ej["emocion_ideal"]
                })
            return self.json({"ejercicios": ejercicios})

        # ──── RESPIRACIÓN: Info de un ejercicio ────
        if path == '/api/respiracion/info':
            clave = q('ejercicio', '4-7-8')
            ej = respiracion.obtener_ejercicio(clave)
            if not ej:
                return self.json({"error": "No encontrado"}, 404)
            return self.json({
                "clave": clave, "nombre": ej["nombre"],
                "descripcion": ej["descripcion"], "beneficio": ej["beneficio"],
                "pasos": [{"texto": t, "segundos": s} for t, s in ej["pasos"]],
                "ciclos": ej["ciclos"], "visualizacion": ej["visualizacion"],
                "frase_inicio": respiracion.obtener_frase_inicio(),
                "frase_cierre": respiracion.obtener_frase_cierre()
            })

        # ──── RESPIRACIÓN: Recomendar por emoción ────
        if path == '/api/respiracion/recomendar':
            estado = q('estado', 'ansioso')
            return self.json({"recomendado": respiracion.obtener_recomendacion(estado)})

        # ──── RESPIRACIÓN: Modo crisis ────
        if path == '/api/respiracion/crisis':
            return self.json({"crisis": respiracion.obtener_mensaje_crisis()})

        # ──── EMOCIONES: Detectar ────
        if path == '/api/emociones/detectar':
            texto = q('texto', '')
            if texto:
                resultado = escucha.detectar_emocion(texto)
                return self.json(resultado)
            return self.json({"emocion": "neutral"})

        # ──── DIARIO: Obtener entradas ────
        if path == '/api/diario/entradas':
            entradas = []
            if hasattr(diario, 'obtener_entradas'):
                entradas = diario.obtener_entradas()
            return self.json({"entradas": entradas})

        # ──── DIARIO: Guardar ────
        if path == '/api/diario/guardar':
            texto = q('texto', '')
            emocion = q('emocion', '')
            nota = q('nota', '')
            if texto:
                if hasattr(diario, 'agregar_entrada'):
                    diario.agregar_entrada(texto, emocion)
                return self.json({"guardado": True, "entrada": {"texto": texto, "emocion": emocion}})
            return self.json({"error": "Sin texto"}, 400)

        # ──── LÍNEAS DE AYUDA: Países ────
        if path == '/api/lineas-ayuda/paises':
            return self.json({"paises": list(lineas_ayuda.PAISES.keys())})

        # ──── LÍNEAS DE AYUDA: Por país ────
        if path == '/api/lineas-ayuda':
            pais = q('pais', 'México')
            lineas_data = lineas_ayuda.PAISES.get(pais, {})
            lineas = lineas_data.get('lineas', [])
            return self.json({
                "pais": pais,
                "prefijo": lineas_data.get('prefijo', ''),
                "lineas": [{"nombre": l[0], "numero": l[1], "descripcion": l[2], "categoria": l[3]} for l in lineas]
            })

        # ──── ALERTAS: Red de apoyo ────
        if path == '/api/alertas/red':
            red = alertas.obtener_red() if hasattr(alertas, 'obtener_red') else []
            return self.json({"red": red})

        # ──── BITÁCORA: Entradas ────
        if path == '/api/bitacora/entradas':
            escuela = q('escuela', '')
            entradas = []
            if hasattr(bitacora, 'obtener_entradas'):
                entradas = bitacora.obtener_entradas(escuela=escuela) if escuela else bitacora.entradas
            return self.json({"entradas": entradas})

        # ──── BITÁCORA: Agregar ────
        if path == '/api/bitacora/agregar':
            tipo = q('tipo', 'observacion')
            alumno = q('alumno', '')
            grupo = q('grupo', '')
            texto = q('texto', '')
            autor = q('autor', 'Docente')
            escuela = q('escuela', 'general')
            if alumno and texto:
                entrada = bitacora.agregar_entrada(tipo, alumno, grupo, texto, autor, escuela)
                return self.json({"guardado": True, "entrada": entrada})
            return self.json({"error": "Faltan datos"}, 400)

        # ──── ORGANIZADOR ────
        if path == '/api/organizador/tareas':
            tareas = organizador.obtener_tareas() if hasattr(organizador, 'obtener_tareas') else []
            return self.json({"tareas": tareas})

        # ──── CONOCIMIENTO ────
        if path == '/api/conocimiento/faqs':
            faqs = conocimiento.FAQS if hasattr(conocimiento, 'FAQS') else {}
            return self.json({"faqs": faqs})

        # ──── CHAT: Historial ────
        if path == '/api/chat/historial':
            return self.json({"historial": []})

        # ──── Archivos estáticos ────
        if path == '/' or path == '':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        p = urlparse(self.path)
        path = p.path
        body = self.read_body()

        def b(key, default=''):
            return body.get(key, [default])[0]

        # ──── CHAT IA ────
        if path == '/api/chat':
            mensaje = b('mensaje', '')
            if not mensaje:
                return self.json({"error": "Sin mensaje"}, 400)

            # Intentar IA real, fallback a respuesta local
            try:
                respuesta = ia_chat.chatear(mensaje) if hasattr(ia_chat, 'chatear') else None
                if respuesta:
                    return self.json({"respuesta": respuesta, "modo": "ia"})
            except:
                pass

            # Fallback local con escucha
            emocion = escucha.detectar_emocion(mensaje) if hasattr(escucha, 'detectar_emocion') else {"emocion": "neutral"}
            respuestas = {
                "triste": "Te escucho. ¿Quieres que hagamos un ejercicio de respiración juntos? 🌿",
                "ansioso": "Vamos a respirar profundo. Inhala... exhala... ¿Quieres probar el ejercicio 4-7-8?",
                "enojado": "Es válido sentirse así. ¿Quieres contarme más o prefieres distraerte un rato?",
                "feliz": "¡Qué bonito! Disfruta este momento. ¿Qué fue lo que te hizo sentir así? 😊",
                "neutral": "Gracias por compartir. Estoy aquí para lo que necesites. 💜"
            }
            respuesta = respuestas.get(emocion.get('emocion', 'neutral'), respuestas['neutral'])
            return self.json({"respuesta": respuesta, "modo": "local", "emocion": emocion})

        # ──── DIARIO: Guardar POST ────
        if path == '/api/diario/guardar':
            texto = b('texto', '')
            emocion = b('emocion', '')
            if texto:
                if hasattr(diario, 'agregar_entrada'):
                    diario.agregar_entrada(texto, emocion)
                return self.json({"guardado": True})
            return self.json({"error": "Sin texto"}, 400)

        return self.json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        print(f"🌿 {self.client_address[0]} - {format % args}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"🌿 SANA v2.0 - Servidor en puerto {PUERTO}")
    server = HTTPServer(('0.0.0.0', PUERTO), SanaHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.server_close()


if __name__ == '__main__':
    main()
