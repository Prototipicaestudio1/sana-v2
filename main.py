"""
🌿 SANA v2.0 - Servidor Principal para Render
═══════════════════════════════════════════════════════════════
Servidor HTTP que sirve el frontend y conecta los módulos.
═══════════════════════════════════════════════════════════════
"""

import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

# Agregar directorios al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Puerto de Render o 8080 por defecto
PUERTO = int(os.environ.get('PORT', 8080))


class SanaHandler(SimpleHTTPRequestHandler):
    """Manejador personalizado para SANA."""

    def do_GET(self):
        """Maneja peticiones GET."""
        # API Stats
        if self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            stats = {
                "tests": 983,
                "modulos": 27,
                "emociones": 11,
                "ejercicios": 7,
                "lineas_ayuda": 45,
                "lineas_codigo": 13779,
                "version": "2.0",
                "status": "online"
            }
            self.wfile.write(json.dumps(stats).encode())
            return

        # API Status
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "modulos": "todos"}).encode())
            return

        # Servir archivos estáticos
        if self.path == '/':
            self.path = '/index.html'

        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        """Log personalizado."""
        print(f"🌿 {self.client_address[0]} - {format % args}")


def main():
    """Inicia el servidor SANA."""
    # Cambiar al directorio del proyecto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("🌿 SANA v2.0 - Iniciando servidor...")
    print(f"📁 Directorio: {os.getcwd()}")
    print(f"🔌 Puerto: {PUERTO}")
    print(f"🌐 Abre: http://localhost:{PUERTO}")
    print("═" * 50)

    server = HTTPServer(('0.0.0.0', PUERTO), SanaHandler)

    try:
        print("✅ Servidor activo. Presiona Ctrl+C para detener.")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")
        server.server_close()


if __name__ == '__main__':
    main()
