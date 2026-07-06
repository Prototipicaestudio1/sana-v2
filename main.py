"""
🌿 SANA v2.0 - Servidor Principal Completo
Persistencia total en GitHub · Login alumnos y docentes
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
from zonas.regularizacion import Regularizacion
from zonas.usuarios import Usuarios
from backend.github_sync import GitHubSync

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
usuarios = Usuarios()

PUERTO = int(os.environ.get('PORT', 8080))
github = GitHubSync()

# Cargar datos desde GitHub al iniciar
if not github.modo_local:
    print("🔄 Cargando datos desde GitHub...")
    github.load_all(escuelas, usuarios)
    print(f"✅ {len(escuelas.escuelas)} escuelas, {len(usuarios.usuarios)} usuarios")


def sync_all_data():
    """Guarda todos los datos en GitHub"""
    if not github.modo_local:
        github.sync_all(escuelas, usuarios)


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
            return self.json({"tests": 983, "modulos": 27, "version": "2.0", "usuarios": len(usuarios.usuarios), "escuelas": len(escuelas.escuelas)})

        # ──── REGISTRO ALUMNO ────
        if path == '/api/registro':
            nombre = q('nombre', '')
            tipo = q('tipo', 'alumno')
            if not nombre: return self.json({"error": "Falta nombre"}, 400)
            user = usuarios.registrar(nombre, tipo)
            sync_all_data()
            return self.json({"user": user, "mensaje": "Guarda tu ID para entrar"})

        # ──── LOGIN ────
        if path == '/api/login':
            codigo = q('codigo', '')
            user_id = q('user_id', '')
            if user_id:
                user = usuarios.login(user_id)
                if user: return self.json({"valido": True, "user": user})
                return self.json({"valido": False})
            if codigo.startswith('DOC-') or codigo.startswith('ADM-'):
                return self.json(escuelas.validar_codigo(codigo))
            return self.json({"valido": False})

        # ──── PERFIL ────
        if path == '/api/perfil':
            user_id = q('user_id', '')
            user = usuarios.obtener_por_id(user_id)
            if user: return self.json({"user": user})
            return self.json({"error": "No encontrado"}, 404)

        # ──── ACTUALIZAR PERFIL ────
        if path == '/api/perfil/actualizar':
            user_id = q('user_id', '')
            nombre = q('nombre', '')
            if usuarios.actualizar_perfil(user_id, nombre):
                sync_all_data()
                return self.json({"actualizado": True})
            return self.json({"error": "No encontrado"}, 404)

        # ──── ESCUELAS ────
        if path == '/api/escuelas/lista':
            return self.json({"escuelas": escuelas.listar_escuelas()})

        if path == '/api/escuelas/registrar':
            nombre = q('nombre', '')
            docs = int(q('docentes', '0'))
            admins = int(q('admin', '0'))
            if not nombre: return self.json({"error": "Falta nombre"}, 400)
            escuela = escuelas.registrar_escuela(nombre, docs, admins)
            sync_all_data()
            return self.json({"escuela": escuela})

        # ──── RESPIRACIÓN ────
        if path == '/api/respiracion/lista':
            ejercicios = []
            for c, ej in respiracion.EJERCICIOS.items():
                ejercicios.append({"clave": c, "nombre": ej["nombre"], "descripcion": ej["descripcion"], "beneficio": ej["beneficio"], "nivel": ej["nivel"], "ciclos": ej["ciclos"]})
            return self.json({"ejercicios": ejercicios})

        if path == '/api/respiracion/info':
            clave = q('ejercicio', '4-7-8')
            ej = respiracion.obtener_ejercicio(clave)
            if not ej: return self.json({"error": "No encontrado"}, 404)
            return self.json({"clave": clave, "nombre": ej["nombre"], "descripcion": ej["descripcion"], "beneficio": ej["beneficio"], "pasos": [{"texto": t, "segundos": s} for t, s in ej["pasos"]], "ciclos": ej["ciclos"], "frase_inicio": respiracion.obtener_frase_inicio(), "frase_cierre": respiracion.obtener_frase_cierre()})

        if path == '/api/respiracion/recomendar':
            return self.json({"recomendado": respiracion.obtener_recomendacion(q('estado', 'ansioso'))})

        if path == '/api/respiracion/crisis':
            return self.json({"crisis": respiracion.obtener_mensaje_crisis()})

        # ──── EMOCIONES ────
        if path == '/api/emociones/detectar':
            texto = q('texto', '')
            if texto: return self.json(escucha.detectar_emocion(texto))
            return self.json({"emocion": "neutral"})

        # ──── DIARIO ────
        if path == '/api/diario/entradas':
            user_id = q('user_id', '')
            if user_id:
                return self.json({"entradas": usuarios.obtener_diario(user_id)})
            return self.json({"entradas": []})

        if path == '/api/diario/borrar':
            user_id = q('user_id', '')
            entrada_id = int(q('id', '0'))
            if usuarios.borrar_diario(user_id, entrada_id):
                sync_all_data()
                return self.json({"borrado": True})
            return self.json({"error": "No encontrado"}, 404)

        # ──── LÍNEAS DE AYUDA ────
        if path == '/api/lineas-ayuda/paises':
            return self.json({"paises": list(lineas_ayuda.PAISES.keys())})

        if path == '/api/lineas-ayuda':
            pais = q('pais', 'México')
            ld = lineas_ayuda.PAISES.get(pais, {})
            return self.json({"pais": pais, "lineas": [{"nombre": l[0], "numero": l[1], "descripcion": l[2], "categoria": l[3]} for l in ld.get('lineas', [])]})

        # ──── BITÁCORA ────
        if path == '/api/bitacora/entradas':
            escuela = q('escuela', '')
            return self.json({"entradas": bitacora.obtener_entradas(escuela) if hasattr(bitacora, 'obtener_entradas') else bitacora.entradas})

        if path == '/api/bitacora/agregar':
            entrada = bitacora.agregar_entrada(q('tipo', 'observacion'), q('alumno', ''), q('grupo', ''), q('texto', ''), q('autor', 'Docente'), q('escuela', 'general'))
            sync_all_data()
            return self.json({"guardado": True, "entrada": entrada})

        if path == '/api/bitacora/borrar':
            id_entrada = int(q('id', '0'))
            if hasattr(bitacora, 'eliminar_entrada'):
                bitacora.eliminar_entrada(id_entrada)
                sync_all_data()
                return self.json({"borrado": True})
            return self.json({"error": "No implementado"}, 400)

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
            respuestas = {"triste": "Te escucho. ¿Quieres hacer un ejercicio de respiración? 🌿", "ansioso": "Vamos a respirar. ¿Probamos 4-7-8?", "enojado": "Es válido. ¿Quieres contarme más?", "feliz": "¡Qué bueno! 😊", "neutral": "Gracias por compartir. Estoy aquí 💜"}
            return self.json({"respuesta": respuestas.get(emocion.get('emocion', 'neutral'), respuestas['neutral']), "modo": "local"})

        # ──── DIARIO ────
        if path == '/api/diario/guardar':
            user_id = b('user_id', '')
            texto = b('texto', '')
            emocion = b('emocion', '')
            if user_id and texto:
                entrada = usuarios.agregar_diario(user_id, {"texto": texto, "emocion": emocion})
                sync_all_data()
                return self.json({"guardado": True, "entrada": entrada})
            return self.json({"error": "Faltan datos"}, 400)

        # ──── REGULARIZACIÓN ────
        if path == '/api/regularizacion/agregar':
            guia = regularizacion.agregar_guia(b('materia', ''), b('titulo', ''), b('contenido', ''), b('autor', ''), b('escuela', ''))
            sync_all_data()
            return self.json({"guardado": True, "guia": guia})

        # ──── ORGANIZADOR ────
        if path == '/api/organizador/crear-plan':
            plan = organizador.crear_plan(b('nombre', ''), b('materia', ''), b('objetivo', ''), b('actividades', ''), b('escuela', ''), b('autor', ''))
            sync_all_data()
            return self.json({"guardado": True, "plan": plan})

        # ──── BORRAR PLAN ────
        if path == '/api/organizador/borrar-plan':
            id_plan = int(b('id', '0'))
            if hasattr(organizador, 'eliminar_plan'):
                organizador.eliminar_plan(id_plan)
                sync_all_data()
                return self.json({"borrado": True})
            return self.json({"error": "No implementado"}, 400)

        # ──── BORRAR GUÍA ────
        if path == '/api/regularizacion/borrar':
            id_guia = int(b('id', '0'))
            regularizacion.eliminar_guia(id_guia)
            sync_all_data()
            return self.json({"borrado": True})

        # ──── ALERTAS ────
        if path == '/api/alertas/agregar':
            contacto = alertas.agregar_contacto(b('nombre', ''), b('telefono', ''), b('relacion', ''), b('escuela', ''))
            sync_all_data()
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
