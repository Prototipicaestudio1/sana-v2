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
from zonas.director import Director
from zonas.primaria import Primaria
from zonas.juegos import Juegos
from zonas.buzon import Buzon
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
director = Director()
primaria = Primaria()
juegos = Juegos()
buzon = Buzon()

PUERTO = int(os.environ.get('PORT', 8080))
github = GitHubSync()

if not github.modo_local:
    print("🔄 Cargando datos desde GitHub...")
    datos = github.obtener_datos()
    if datos:
        if "escuelas" in datos and datos["escuelas"]:
            escuelas.escuelas = datos["escuelas"]
            escuelas._guardar()
        if "usuarios" in datos and datos["usuarios"]:
            usuarios.usuarios = datos["usuarios"]
            usuarios._guardar()
        if "bitacoras" in datos:
            bitacora.entradas = datos["bitacoras"]
            bitacora.guardar()
        if "regularizacion" in datos:
            regularizacion.material = datos["regularizacion"]
            regularizacion._guardar()
        if "planes" in datos:
            organizador.planes = datos["planes"]
        if "tareas" in datos:
            organizador.tareas = datos["tareas"]
        organizador._guardar()
        if "director" in datos:
            ddata = datos["director"]
            if "avisos" in ddata: director.avisos = ddata["avisos"]
            if "bajas" in ddata: director.bajas = ddata["bajas"]
        if "primaria" in datos:
            pdata = datos["primaria"]
            if "grupos" in pdata: primaria.grupos = pdata["grupos"]
            if "padres" in pdata: primaria.padres = pdata["padres"]
            primaria._guardar()
        if "juegos" in datos: juegos.juegos = datos["juegos"]
    print(f"✅ {len(escuelas.escuelas)} escuelas | {len(usuarios.usuarios)} usuarios | {len(primaria.grupos)} grupos")

def sync_all():
    if not github.modo_local:
        data = {
            "escuelas": escuelas.escuelas,
            "usuarios": usuarios.usuarios,
            "bitacoras": bitacora.entradas,
            "regularizacion": regularizacion.material,
            "planes": organizador.planes,
            "tareas": organizador.tareas,
            "director": {"avisos": director.avisos, "bajas": director.bajas, "bitacora_director": director.bitacora_director},
            "primaria": {"grupos": primaria.grupos, "anuncios_padres": primaria.anuncios_padres, "muro_tareas": primaria.muro_tareas, "padres": primaria.padres, "fichas": primaria.fichas},
            "juegos": juegos.juegos,
            "buzon": buzon.mensajes,
            "fecha": __import__('datetime').datetime.now().isoformat()
        }
        github.guardar_datos(data)

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
            return self.json({"version": "2.2", "usuarios": len(usuarios.usuarios), "escuelas": len(escuelas.escuelas), "grupos": len(primaria.grupos)})

        # ──── CHESS LOGIN ────
        if path == '/api/chess-login':
            uid = q('user_id', '')
            if uid:
                u = usuarios.login(uid)
                if u:
                    return self.json({"valido": True, "user": u})
                if uid == 'SANA-ADMIN-2025' or uid.startswith('ADM-'):
                    nuevo = usuarios.registrar("Administrador", "admin")
                else:
                    nuevo = usuarios.registrar("Jugador", "alumno")
                sync_all()
                return self.json({"valido": True, "user": nuevo})
            return self.json({"valido": False})

        # ──── REGISTRO / LOGIN ────
        if path == '/api/registro':
            n = q('nombre', ''); t = q('tipo', 'alumno'); cod = q('codigo', '')
            if not n: return self.json({"error": "Falta nombre"}, 400)
            cod_esc = None
            if cod and (cod.startswith('DOC-') or cod.startswith('ADM-') or cod.startswith('ESC-')):
                val = escuelas.validar_codigo(cod)
                if val.get('valido'): cod_esc = val.get('codigo_escuela')
            user = usuarios.registrar(n, t, cod_esc, cod if t in ('docente','director') else None)
            sync_all(); return self.json({"user": user})

        if path == '/api/login':
            uid = q('user_id', ''); cod = q('codigo', '')
            if uid:
                u = usuarios.login(uid)
                if u:
                    return self.json({"valido": True, "user": u, "buzon": buzon.no_leidos(uid)})
                return self.json({"valido": False})
            if cod.startswith('ESC-'):
                esc = escuelas.obtener_escuela(cod)
                if esc: return self.json({"valido": True, "tipo": "director", "escuela": esc["nombre"], "codigo_escuela": cod})
                return self.json({"valido": False})
            if cod.startswith('PAD-'):
                p = primaria.login_padre(cod)
                return self.json({"valido": True, "tipo": "padre", "padre": p}) if p else self.json({"valido": False})
            if cod.startswith('DOC-') or cod.startswith('ADM-'):
                return self.json(escuelas.validar_codigo(cod))
            return self.json({"valido": False})

        if path == '/api/perfil':
            u = usuarios.obtener_por_id(q('user_id', ''))
            return self.json({"user": u}) if u else self.json({"error": "No encontrado"}, 404)

        if path == '/api/escuelas/lista': return self.json({"escuelas": escuelas.listar_escuelas()})
        if path == '/api/escuelas/registrar':
            esc = escuelas.registrar_escuela(q('nombre', ''), int(q('docentes', '0')), int(q('admin', '0')))
            sync_all(); return self.json({"escuela": esc})
        if path == '/api/escuelas/borrar':
            cod = q('codigo', '')
            if cod in escuelas.escuelas: del escuelas.escuelas[cod]; escuelas._guardar(); sync_all(); return self.json({"ok": True})
            return self.json({"error": "No encontrada"}, 404)

        if path == '/api/director/avisos': return self.json({"avisos": director.obtener_avisos(q('escuela', ''))})
        if path == '/api/director/publicar-aviso':
            director.publicar_aviso(q('escuela', ''), q('titulo', ''), q('mensaje', ''), q('autor', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/director/dar-baja':
            cod = q('codigo_docente', '')
            esc_data = escuelas.obtener_escuela(q('escuela', ''))
            if esc_data and cod in esc_data.get("codigos_docentes", []): esc_data["codigos_docentes"].remove(cod); escuelas._guardar()
            director.dar_baja_docente(q('escuela', ''), cod, q('motivo', ''), q('autor', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/director/nuevo-codigo':
            import random, string
            nuevo = f"DOC-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
            esc_data = escuelas.obtener_escuela(q('escuela', ''))
            if esc_data: esc_data["codigos_docentes"].append(nuevo); escuelas._guardar()
            sync_all(); return self.json({"nuevo_codigo": nuevo})
        if path == '/api/director/reporte': return self.json({"reporte": director.generar_reporte_mensual(q('escuela', ''))})
        if path == '/api/director/bitacora': return self.json({"entradas": director.obtener_bitacora(q('escuela', ''))})
        if path == '/api/director/bitacora-agregar':
            director.agregar_bitacora(q('escuela', ''), q('texto', ''), q('autor', ''))
            sync_all(); return self.json({"guardado": True})

        if path == '/api/primaria/grupos': return self.json({"grupos": primaria.obtener_grupos(q('escuela', ''), q('docente', ''))})
        if path == '/api/primaria/crear-grupo':
            try: padres_lista = json.loads(q('padres', '[]'))
            except: padres_lista = []
            g = primaria.crear_grupo(q('escuela', ''), q('nombre', ''), q('docente', ''), padres_lista)
            sync_all(); return self.json({"guardado": True, "grupo": g})
        if path == '/api/primaria/login-padre':
            p = primaria.login_padre(q('codigo', ''))
            return self.json({"valido": True, "padre": p}) if p else self.json({"valido": False})
        if path == '/api/primaria/anuncios-padres': return self.json({"anuncios": primaria.obtener_anuncios_padres(q('escuela', ''))})
        if path == '/api/primaria/publicar-anuncio-padres':
            primaria.publicar_anuncio_padres(q('escuela', ''), q('titulo', ''), q('mensaje', ''), q('autor', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/primaria/tareas': return self.json({"tareas": primaria.obtener_tareas(q('escuela', ''), q('grupo', ''))})
        if path == '/api/primaria/agregar-tarea':
            primaria.agregar_tarea(q('escuela', ''), q('grupo', ''), q('titulo', ''), q('descripcion', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/primaria/fichas': return self.json({"fichas": primaria.obtener_fichas(q('codigo_padre', ''))})
        if path == '/api/primaria/fichas-agregar':
            primaria.agregar_ficha_tarea(q('codigo_padre', ''), q('titulo', ''), int(q('puntos', '1')), q('recompensa', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/primaria/fichas-completar':
            primaria.completar_ficha_tarea(q('codigo_padre', ''), int(q('id', '0'))); sync_all()
            return self.json({"ok": True})

        if path == '/api/juegos/lista': return self.json({"juegos": juegos.obtener_juegos(q('categoria', ''))})
        if path == '/api/juegos/ver':
            j = juegos.obtener_juego(int(q('id', '0')))
            return self.json({"juego": j}) if j else self.json({"error": "No encontrado"}, 404)

        if path == '/api/respiracion/lista':
            return self.json({"ejercicios": [{"clave": c, "nombre": e["nombre"], "nivel": e["nivel"], "ciclos": e["ciclos"]} for c, e in respiracion.EJERCICIOS.items()]})
        if path == '/api/respiracion/info':
            ej = respiracion.obtener_ejercicio(q('ejercicio', '4-7-8'))
            if not ej: return self.json({"error": "No encontrado"}, 404)
            return self.json({"clave": q('ejercicio'), "nombre": ej["nombre"], "pasos": [{"texto": t, "segundos": s} for t, s in ej["pasos"]], "ciclos": ej["ciclos"]})

        if path == '/api/emociones/detectar':
            t = q('texto', ''); return self.json(escucha.detectar_emocion(t)) if t else self.json({"emocion": "neutral"})

        if path == '/api/diario/entradas': return self.json({"entradas": usuarios.obtener_diario(q('user_id', ''))})
        if path == '/api/diario/borrar': usuarios.borrar_diario(q('user_id', ''), int(q('id', '0'))); sync_all(); return self.json({"ok": True})

        if path == '/api/lineas-ayuda/paises': return self.json({"paises": list(lineas_ayuda.PAISES.keys())})
        if path == '/api/lineas-ayuda':
            ld = lineas_ayuda.PAISES.get(q('pais', 'México'), {})
            return self.json({"pais": q('pais'), "lineas": [{"nombre": l[0], "numero": l[1], "categoria": l[3]} for l in ld.get('lineas', [])]})

        if path == '/api/bitacora/entradas': return self.json({"entradas": bitacora.obtener_entradas(q('escuela', ''))})
        if path == '/api/bitacora/agregar':
            bitacora.agregar_entrada(q('tipo', 'observacion'), q('alumno', ''), q('grupo', ''), q('texto', ''), q('autor', ''), q('escuela', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/bitacora/compartir':
            bitacora.compartir_entrada(int(q('id', '0')), q('destino', '')); sync_all(); return self.json({"ok": True})
        if path == '/api/bitacora/borrar': bitacora.eliminar_entrada(int(q('id', '0'))); sync_all(); return self.json({"ok": True})

        if path == '/api/organizador/planes': return self.json({"planes": organizador.obtener_planes(q('escuela', ''))})
        if path == '/api/organizador/planes-publicos': return self.json({"planes": organizador.obtener_planes_publicos()})
        if path == '/api/organizador/planes-alumno': return self.json({"planes": organizador.obtener_planes_alumno(q('alumno_id', ''))})
        if path == '/api/organizador/planes-docente': return self.json({"planes": organizador.obtener_planes_docente(q('autor', ''), q('escuela', ''))})
        if path == '/api/organizador/crear-plan':
            organizador.crear_plan(q('nombre', ''), q('materia', 'General'), q('objetivo', ''), q('actividades', ''), q('escuela', ''), q('autor', ''), q('visibilidad', 'privado'))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/organizador/compartir-plan':
            organizador.compartir_plan(int(q('id', '0')), q('destino', '')); sync_all(); return self.json({"ok": True})

        if path == '/api/regularizacion/materias': return self.json({"materias": regularizacion.obtener_materias()})
        if path == '/api/regularizacion/guias': return self.json({"guias": regularizacion.obtener_guias(q('materia', ''), q('escuela', ''))})

        if path == '/api/alertas/red': return self.json({"red": alertas.obtener_red(q('escuela', ''))})

        if path == '/' or path == '': self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        p = urlparse(self.path); path = p.path; b = self.read_body()
        def v(k, d=''): return b.get(k, [d])[0]
        if path == '/api/chat':
            msg = v('mensaje', '')
            if not msg: return self.json({"error": "Sin mensaje"}, 400)
            try: resp = ia_chat.obtener_respuesta(msg); return self.json({"respuesta": resp, "modo": "ia"})
            except: return self.json({"respuesta": "💬 Estoy aquí para ti. 🌿", "modo": "local"})
        if path == '/api/diario/guardar':
            usuarios.agregar_diario(v('user_id', ''), {"texto": v('texto', ''), "emocion": v('emocion', '')})
            sync_all(); return self.json({"guardado": True})
        if path == '/api/regularizacion/agregar':
            regularizacion.agregar_guia(v('materia', ''), v('titulo', ''), v('contenido', ''), v('autor', ''), v('escuela', ''))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/regularizacion/borrar': regularizacion.eliminar_guia(int(v('id', '0'))); sync_all(); return self.json({"ok": True})
        if path == '/api/juegos/agregar':
            juegos.agregar_juego(v('titulo', ''), v('descripcion', ''), v('html_code', ''), v('categoria', 'general'))
            sync_all(); return self.json({"guardado": True})
        if path == '/api/juegos/borrar': juegos.eliminar_juego(int(v('id', '0'))); sync_all(); return self.json({"ok": True})
        if path == '/api/alertas/agregar':
            alertas.agregar_contacto(v('nombre', ''), v('telefono', ''), v('relacion', ''), v('escuela', ''))
            sync_all(); return self.json({"guardado": True})
        return self.json({"error": "Not found"}, 404)

    def log_message(self, f, *a): print(f"🌿 {self.client_address[0]} - {f % a}")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"🌿 SANA v2.2 :{PUERTO}")
    HTTPServer(('0.0.0.0', PUERTO), SanaHandler).serve_forever()

if __name__ == '__main__':
    main()
