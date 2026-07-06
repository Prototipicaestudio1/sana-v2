"""
🌿 SANA v2.0 - Servidor Principal
Persistencia TOTAL en GitHub · Todo por usuario y comunidad
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
ia_chat = IAChat(escucha=escucha)
diario = Diario()
alertas = Alertas()
bitacora = Bitacora()
organizador = Organizador()
escuelas = Escuelas()
regularizacion = Regularizacion()
usuarios = Usuarios()

PUERTO = int(os.environ.get('PORT', 8080))
github = GitHubSync()

# Cargar TODO desde GitHub al iniciar
if not github.modo_local:
    print("🔄 Cargando datos desde GitHub...")
    github.load_all(escuelas, usuarios, bitacora, regularizacion, organizador, alertas)
    print(f"✅ {len(escuelas.escuelas)} escuelas | {len(usuarios.usuarios)} usuarios | {len(bitacora.entradas)} bitácoras | {len(regularizacion.material)} guías | {len(organizador.planes)} planes")

def sync_all():
    """Sincroniza TODO a GitHub"""
    if not github.modo_local:
        github.sync_all(escuelas, usuarios, bitacora, regularizacion, organizador, alertas)

class SanaHandler(SimpleHTTPRequestHandler):
    def json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length: return parse_qs(self.rfile.read(length).decode())
        return {}

    def do_GET(self):
        p = urlparse(self.path); path = p.path; qs = parse_qs(p.query)
        def q(k, d=''): return qs.get(k, [d])[0]

        if path == '/api/stats':
            return self.json({
                "tests": 983, "modulos": 27, "version": "2.0",
                "usuarios": len(usuarios.usuarios), "escuelas": len(escuelas.escuelas),
                "bitacoras": len(bitacora.entradas), "guias": len(regularizacion.material),
                "planes": len(organizador.planes), "ia": ia_chat.obtener_estado()["modo"]
            })

        # ──── REGISTRO / LOGIN ────
        if path == '/api/registro':
            n = q('nombre', ''); t = q('tipo', 'alumno'); cod = q('codigo', '')
            if not n: return self.json({"error": "Falta nombre"}, 400)
            cod_esc = None
            if cod and (cod.startswith('DOC-') or cod.startswith('ADM-')):
                val = escuelas.validar_codigo(cod)
                if val.get('valido'): cod_esc = val.get('codigo_escuela')
            user = usuarios.registrar(n, t, cod_esc, cod if t == 'docente' else None)
            sync_all(); return self.json({"user": user, "mensaje": "Guarda tu ID"})

        if path == '/api/login':
            uid = q('user_id', ''); cod = q('codigo', '')
            if uid:
                u = usuarios.login(uid)
                return self.json({"valido": True, "user": u}) if u else self.json({"valido": False})
            if cod.startswith('DOC-') or cod.startswith('ADM-'):
                return self.json(escuelas.validar_codigo(cod))
            return self.json({"valido": False})

        # ──── PERFIL ────
        if path == '/api/perfil':
            u = usuarios.obtener_por_id(q('user_id', ''))
            return self.json({"user": u}) if u else self.json({"error": "No encontrado"}, 404)

        if path == '/api/perfil/actualizar':
            if usuarios.actualizar_perfil(q('user_id', ''), q('nombre', '')):
                sync_all(); return self.json({"ok": True})
            return self.json({"error": "No encontrado"}, 404)

        # ──── ESCUELAS ────
        if path == '/api/escuelas/lista': return self.json({"escuelas": escuelas.listar_escuelas()})
        if path == '/api/escuelas/registrar':
            esc = escuelas.registrar_escuela(q('nombre', ''), int(q('docentes', '0')), int(q('admin', '0')))
            sync_all(); return self.json({"escuela": esc})

        # ──── RESPIRACIÓN ────
        if path == '/api/respiracion/lista':
            return self.json({"ejercicios": [{"clave": c, "nombre": e["nombre"], "descripcion": e["descripcion"], "nivel": e["nivel"], "ciclos": e["ciclos"]} for c, e in respiracion.EJERCICIOS.items()]})
        if path == '/api/respiracion/info':
            ej = respiracion.obtener_ejercicio(q('ejercicio', '4-7-8'))
            if not ej: return self.json({"error": "No encontrado"}, 404)
            return self.json({"clave": q('ejercicio'), "nombre": ej["nombre"], "descripcion": ej["descripcion"], "pasos": [{"texto": t, "segundos": s} for t, s in ej["pasos"]], "ciclos": ej["ciclos"], "frase_inicio": respiracion.obtener_frase_inicio(), "frase_cierre": respiracion.obtener_frase_cierre()})
        if path == '/api/respiracion/recomendar': return self.json({"recomendado": respiracion.obtener_recomendacion(q('estado', 'ansioso'))})
        if path == '/api/respiracion/crisis': return self.json({"crisis": respiracion.obtener_mensaje_crisis()})

        # ──── EMOCIONES ────
        if path == '/api/emociones/detectar':
            t = q('texto', '')
            return self.json(escucha.detectar_emocion(t)) if t else self.json({"emocion": "neutral"})

        # ──── DIARIO (por usuario) ────
        if path == '/api/diario/entradas':
            return self.json({"entradas": usuarios.obtener_diario(q('user_id', ''))})
        if path == '/api/diario/borrar':
            usuarios.borrar_diario(q('user_id', ''), int(q('id', '0'))); sync_all()
            return self.json({"ok": True})

        # ──── LÍNEAS DE AYUDA ────
        if path == '/api/lineas-ayuda/paises': return self.json({"paises": list(lineas_ayuda.PAISES.keys())})
        if path == '/api/lineas-ayuda':
            ld = lineas_ayuda.PAISES.get(q('pais', 'México'), {})
            return self.json({"pais": q('pais'), "lineas": [{"nombre": l[0], "numero": l[1], "categoria": l[3]} for l in ld.get('lineas', [])]})

        # ──── BITÁCORA (por escuela) ────
        if path == '/api/bitacora/entradas':
            return self.json({"entradas": bitacora.obtener_entradas(q('escuela', '')) if hasattr(bitacora, 'obtener_entradas') else bitacora.entradas})
        if path == '/api/bitacora/agregar':
            e = bitacora.agregar_entrada(q('tipo', 'observacion'), q('alumno', ''), q('grupo', ''), q('texto', ''), q('autor', ''), q('escuela', ''))
            sync_all(); return self.json({"guardado": True, "entrada": e})

        # ──── ORGANIZADOR (por escuela) ────
        if path == '/api/organizador/planes':
            return self.json({"planes": organizador.obtener_planes(q('escuela', ''))})
        if path == '/api/organizador/tareas':
            return self.json({"tareas": organizador.obtener_tareas()})

        # ──── REGULARIZACIÓN (público + por escuela) ────
        if path == '/api/regularizacion/materias': return self.json({"materias": regularizacion.obtener_materias()})
        if path == '/api/regularizacion/guias':
            return self.json({"guias": regularizacion.obtener_guias(q('materia', ''), q('escuela', ''))})

        # ──── ALERTAS (por escuela) ────
        if path == '/api/alertas/red':
            return self.json({"red": alertas.obtener_red(q('escuela', ''))})

        if path == '/' or path == '': self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        p = urlparse(self.path); path = p.path; b = self.read_body()
        def v(k, d=''): return b.get(k, [d])[0]

        # ──── CHAT IA ────
        if path == '/api/chat':
            msg = v('mensaje', '')
            if not msg: return self.json({"error": "Sin mensaje"}, 400)
            try:
                resp = ia_chat.obtener_respuesta(msg)
                return self.json({"respuesta": resp, "modo": "ia"})
            except:
                return self.json({"respuesta": "💬 Estoy aquí para ti. Cuéntame más. 🌿", "modo": "local"})

        # ──── DIARIO ────
        if path == '/api/diario/guardar':
            e = usuarios.agregar_diario(v('user_id', ''), {"texto": v('texto', ''), "emocion": v('emocion', '')})
            sync_all(); return self.json({"guardado": True, "entrada": e}) if e else self.json({"error": "Faltan datos"}, 400)

        # ──── REGULARIZACIÓN ────
        if path == '/api/regularizacion/agregar':
            regularizacion.agregar_guia(v('materia', ''), v('titulo', ''), v('contenido', ''), v('autor', ''), v('escuela', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/regularizacion/borrar':
            regularizacion.eliminar_guia(int(v('id', '0'))); sync_all(); return self.json({"ok": True})

        # ──── ORGANIZADOR ────
        if path == '/api/organizador/crear-plan':
            organizador.crear_plan(v('nombre', ''), v('materia', ''), v('objetivo', ''), v('actividades', ''), v('escuela', ''), v('autor', ''))
            sync_all(); return self.json({"guardado": True})

        # ──── ALERTAS ────
        if path == '/api/alertas/agregar':
            alertas.agregar_contacto(v('nombre', ''), v('telefono', ''), v('relacion', ''), v('escuela', ''))
            sync_all(); return self.json({"guardado": True})

        return self.json({"error": "Not found"}, 404)

    def log_message(self, f, *a):
        print(f"🌿 {self.client_address[0]} - {f % a}")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"🌿 SANA v2.0 :{PUERTO}")
    HTTPServer(('0.0.0.0', PUERTO), SanaHandler).serve_forever()

if __name__ == '__main__':
    main()
