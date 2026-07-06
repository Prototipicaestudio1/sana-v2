"""
🌿 SANA v2.0 - Servidor Principal Completo
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
from zonas.escuelas import Escuelas
from backend.github_sync import GitHubSync
from zonas.regularizacion import Regularizacion

respiracion = Respiracion()
escucha = Escucha()
lineas_ayuda = LineasAyuda()
ia_chat = IAChat()
diario = Diario()
alertas = Alertas()
bitacora = Bitacora()
organizador = Organizador()
escuelas = Escuelas()
regularizacion = Regularizacion()

PUERTO = int(os.environ.get('PORT', 8080))
github = GitHubSync()

# Cargar datos desde GitHub al iniciar
if not github.modo_local:
    print("🔄 Sincronizando datos desde GitHub...")
    datos_github = github.obtener_datos()
    if datos_github:
        if "escuelas" in datos_github:
            escuelas.escuelas = datos_github["escuelas"]
            escuelas._guardar()
            print(f"✅ {len(datos_github['escuelas'])} escuelas cargadas")

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
            return parse_qs(self.rfile.read(length).decode())
        return {}

    def do_GET(self):
        p = urlparse(self.path)
        path = p.path
        qs = parse_qs(p.query)
        def q(k, d=''): return qs.get(k, [d])[0]

        # ──── STATS ────
        if path == '/api/stats':
            return self.json({"tests": 983, "modulos": 27, "emociones": 11, "ejercicios": 7, "lineas_ayuda": 45, "version": "2.0"})

        # ──── LOGIN DOCENTE/ADMIN ────
        if path == '/api/login':
            codigo = q('codigo', '')
            if not codigo:
                return self.json({"valido": False, "error": "Sin código"}, 400)
            resultado = escuelas.validar_codigo(codigo)
            return self.json(resultado)

        # ──── ESCUELAS ────
        if path == '/api/escuelas/lista':
            return self.json({"escuelas": escuelas.listar_escuelas()})

        if path == '/api/escuelas/registrar':
            nombre = q('nombre', '')
            docs = int(q('docentes', '0'))
            admins = int(q('admin', '0'))
            if not nombre:
                return self.json({"error": "Falta nombre"}, 400)
            escuela = escuelas.registrar_escuela(nombre, docs, admins)
            return self.json({"escuela": escuela})

        # ──── RESPIRACIÓN ────
        if path == '/api/respiracion/lista':
            ejercicios = []
            for c, ej in respiracion.EJERCICIOS.items():
                ejercicios.append({"clave": c, "nombre": ej["nombre"], "descripcion": ej["descripcion"], "beneficio": ej["beneficio"], "nivel": ej["nivel"], "ciclos": ej["ciclos"], "visualizacion": ej["visualizacion"]})
            return self.json({"ejercicios": ejercicios})

        if path == '/api/respiracion/info':
            clave = q('ejercicio', '4-7-8')
            ej = respiracion.obtener_ejercicio(clave)
            if not ej: return self.json({"error": "No encontrado"}, 404)
            return self.json({"clave": clave, "nombre": ej["nombre"], "descripcion": ej["descripcion"], "beneficio": ej["beneficio"], "pasos": [{"texto": t, "segundos": s} for t, s in ej["pasos"]], "ciclos": ej["ciclos"], "visualizacion": ej["visualizacion"], "frase_inicio": respiracion.obtener_frase_inicio(), "frase_cierre": respiracion.obtener_frase_cierre()})

        if path == '/api/respiracion/recomendar':
            return self.json({"recomendado": respiracion.obtener_recomendacion(q('estado', 'ansioso'))})

        if path == '/api/respiracion/crisis':
            return self.json({"crisis": respiracion.obtener_mensaje_crisis()})

        # ──── EMOCIONES ────
        if path == '/api/emociones/detectar':
            texto = q('texto', '')
            if texto:
                return self.json(escucha.detectar_emocion(texto))
            return self.json({"emocion": "neutral"})

        # ──── DIARIO ────
        if path == '/api/diario/entradas':
            return self.json({"entradas": diario.obtener_entradas() if hasattr(diario, 'obtener_entradas') else []})

        # ──── LÍNEAS DE AYUDA ────
        if path == '/api/lineas-ayuda/paises':
            return self.json({"paises": list(lineas_ayuda.PAISES.keys())})

        if path == '/api/lineas-ayuda':
            pais = q('pais', 'México')
            ld = lineas_ayuda.PAISES.get(pais, {})
            return self.json({"pais": pais, "prefijo": ld.get('prefijo', ''), "lineas": [{"nombre": l[0], "numero": l[1], "descripcion": l[2], "categoria": l[3]} for l in ld.get('lineas', [])]})

        # ──── BITÁCORA ────
        if path == '/api/bitacora/entradas':
            return self.json({"entradas": bitacora.obtener_entradas(q('escuela', '')) if hasattr(bitacora, 'obtener_entradas') else bitacora.entradas})

        if path == '/api/bitacora/agregar':
            entrada = bitacora.agregar_entrada(q('tipo', 'observacion'), q('alumno', ''), q('grupo', ''), q('texto', ''), q('autor', 'Docente'), q('escuela', 'general'))
            return self.json({"guardado": True, "entrada": entrada})

        # ──── ORGANIZADOR ────
        if path == '/api/organizador/planes':
            return self.json({"planes": organizador.obtener_planes(q('escuela', ''))})

        if path == '/api/organizador/tareas':
            return self.json({"tareas": organizador.obtener_tareas()})

        # ──── REGULARIZACIÓN ────
        if path == '/api/regularizacion/materias':
            return self.json({"materias": regularizacion.obtener_materias()})

        if path == '/api/regularizacion/guias':
            return self.json({"guias": regularizacion.obtener_guias(q('materia', ''), q('escuela', ''))})

        # ──── ALERTAS ────
        if path == '/api/alertas/red':
            return self.json({"red": alertas.obtener_red(q('escuela', ''))})

        # ──── ESTÁTICOS ────
        if path == '/' or path == '':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        p = urlparse(self.path)
        path = p.path
        body = self.read_body()
        def b(k, d=''): return body.get(k, [d])[0]

        # ──── CHAT ────
        if path == '/api/chat':
            mensaje = b('mensaje', '')
            if not mensaje: return self.json({"error": "Sin mensaje"}, 400)
            try:
                resp = ia_chat.chatear(mensaje) if hasattr(ia_chat, 'chatear') else None
                if resp: return self.json({"respuesta": resp, "modo": "ia"})
            except: pass
            emocion = escucha.detectar_emocion(mensaje) if hasattr(escucha, 'detectar_emocion') else {"emocion": "neutral"}
            respuestas = {"triste": "Te escucho. ¿Quieres hacer un ejercicio de respiración? 🌿", "ansioso": "Vamos a respirar. ¿Probamos el ejercicio 4-7-8?", "enojado": "Es válido. ¿Quieres contarme más?", "feliz": "¡Qué bueno! Disfrútalo 😊", "neutral": "Gracias por compartir. Estoy aquí 💜"}
            return self.json({"respuesta": respuestas.get(emocion.get('emocion', 'neutral'), respuestas['neutral']), "modo": "local", "emocion": emocion})

        # ──── DIARIO ────
        if path == '/api/diario/guardar':
            texto = b('texto', '')
            emocion = b('emocion', '')
            if texto and hasattr(diario, 'agregar_entrada'):
                diario.agregar_entrada(texto, emocion)
                return self.json({"guardado": True})
            return self.json({"error": "Sin texto"}, 400)

        # ──── REGULARIZACIÓN: Agregar guía ────
        if path == '/api/regularizacion/agregar':
            guia = regularizacion.agregar_guia(b('materia', ''), b('titulo', ''), b('contenido', ''), b('autor', ''), b('escuela', ''))
            escuelas.agregar_material(b('escuela', ''), {"materia": b('materia', ''), "titulo": b('titulo', ''), "contenido": b('contenido', '')})
            return self.json({"guardado": True, "guia": guia})

        # ──── ORGANIZADOR: Crear plan ────
        if path == '/api/organizador/crear-plan':
            plan = organizador.crear_plan(b('nombre', ''), b('materia', ''), b('objetivo', ''), b('actividades', ''), b('escuela', ''), b('autor', ''))
            escuelas.agregar_plan(b('escuela', ''), {"nombre": b('nombre', ''), "materia": b('materia', ''), "objetivo": b('objetivo', '')})
            return self.json({"guardado": True, "plan": plan})

        # ──── ALERTAS: Agregar contacto ────
        if path == '/api/alertas/agregar':
            contacto = alertas.agregar_contacto(b('nombre', ''), b('telefono', ''), b('relacion', ''), b('escuela', ''))
            return self.json({"guardado": True, "contacto": contacto})

        return self.json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        print(f"🌿 {self.client_address[0]} - {format % args}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"🌿 SANA v2.0 en puerto {PUERTO}")
    HTTPServer(('0.0.0.0', PUERTO), SanaHandler).serve_forever()

if __name__ == '__main__':
    main()
