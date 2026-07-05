"""
🌿 Sana - Módulo de Servidor Local P2P
═══════════════════════════════════════════════════════════════
Compartir bitácora entre docentes de la misma escuela
sin internet, usando WiFi Direct o misma red local.
Microservidor HTTP + Cliente · 100% local · Test integrado.
═══════════════════════════════════════════════════════════════
"""

import socket
import json
import threading
import time
import os


class ServidorBitacora:
    """
    Microservidor local para compartir bitácora entre docentes.
    
    - Un docente inicia el servidor (comparte)
    - Otros docentes se conectan como clientes (reciben)
    - Funciona en la misma red WiFi (sin internet)
    - Puerto predeterminado: 8080
    """

    def __init__(self, puerto: int = 8080):
        self.puerto = puerto
        self.activo = False
        self.bitacora = None
        self.ip = "127.0.0.1"
        self.conexiones = 0
        self.hilo = None

    def iniciar(self, bitacora, escuela: str = "") -> dict:
        """
        Inicia el servidor en segundo plano.
        
        Args:
            bitacora: Instancia de Bitacora para compartir
            escuela: Clave de escuela para filtrar
        
        Returns:
            Diccionario con IP, puerto y estado.
        """
        if self.activo:
            return {"exito": False, "mensaje": "El servidor ya está activo."}

        self.bitacora = bitacora
        self.activo = True
        self.conexiones = 0

        def _servir():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.puerto))
            server.listen(5)
            server.settimeout(1.0)

            while self.activo:
                try:
                    cliente, direccion = server.accept()
                    self.conexiones += 1
                    
                    # Recibir solicitud
                    datos = cliente.recv(4096).decode('utf-8', errors='ignore')
                    
                    # Procesar comando
                    respuesta = self._procesar_comando(datos, escuela)
                    
                    # Enviar respuesta
                    cliente.send(respuesta.encode('utf-8'))
                    cliente.close()
                    
                except socket.timeout:
                    continue
                except Exception:
                    if self.activo:
                        continue
                    break

            try:
                server.close()
            except:
                pass

        self.hilo = threading.Thread(target=_servir, daemon=True)
        self.hilo.start()

        # Obtener IP local
        self.ip = self._obtener_ip_local()

        return {
            "exito": True,
            "mensaje": f"✅ Servidor iniciado en {self.ip}:{self.puerto}",
            "ip": self.ip,
            "puerto": self.puerto
        }

    def _procesar_comando(self, datos: str, escuela: str) -> str:
        """Procesa comandos del cliente."""
        datos = datos.strip()
        
        # Comando: TOTAL
        if datos.upper() == "TOTAL":
            entradas = self.bitacora.obtener_entradas(
                escuela=escuela, solo_publicas=True
            )
            return json.dumps({"total": len(entradas)})
        
        # Comando: TODAS
        if datos.upper() == "TODAS":
            entradas = self.bitacora.obtener_entradas(
                escuela=escuela, solo_publicas=True
            )
            return json.dumps({"entradas": entradas, "total": len(entradas)})
        
        # Comando: ALUMNO:<nombre>
        if datos.upper().startswith("ALUMNO:"):
            alumno = datos[7:].strip()
            entradas = self.bitacora.obtener_entradas(
                escuela=escuela, solo_publicas=True, alumno=alumno
            )
            return json.dumps({"entradas": entradas, "total": len(entradas)})
        
        # Comando: ESTADISTICAS
        if datos.upper() == "ESTADISTICAS":
            stats = self.bitacora.obtener_estadisticas(escuela=escuela)
            return json.dumps(stats)
        
        # Comando no reconocido
        return json.dumps({"error": "Comando no reconocido", "ayuda": "TOTAL, TODAS, ALUMNO:<nombre>, ESTADISTICAS"})

    def detener(self) -> dict:
        """Detiene el servidor."""
        self.activo = False
        if self.hilo:
            self.hilo.join(timeout=2)
        return {"exito": True, "mensaje": "Servidor detenido."}

    def estado(self) -> dict:
        """Retorna el estado actual del servidor."""
        return {
            "activo": self.activo,
            "ip": self.ip,
            "puerto": self.puerto,
            "conexiones": self.conexiones
        }

    def _obtener_ip_local(self) -> str:
        """Obtiene la IP local del dispositivo."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"


class ClienteBitacora:
    """
    Cliente para conectarse a un servidor de bitácora.
    """

    def __init__(self):
        self.conectado = False

    def conectar(self, ip: str, puerto: int = 8080) -> dict:
        """
        Verifica conexión con el servidor.
        
        Args:
            ip: Dirección IP del servidor
            puerto: Puerto del servidor
        
        Returns:
            Diccionario con estado de conexión.
        """
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(3)
            cliente.connect((ip, puerto))
            cliente.close()
            self.conectado = True
            return {"exito": True, "mensaje": f"✅ Conectado a {ip}:{puerto}"}
        except Exception as e:
            self.conectado = False
            return {"exito": False, "mensaje": f"❌ No se pudo conectar: {str(e)}"}

    def obtener_total(self, ip: str, puerto: int = 8080) -> dict:
        """Obtiene el total de entradas públicas."""
        return self._enviar_comando(ip, puerto, "TOTAL")

    def obtener_todas(self, ip: str, puerto: int = 8080) -> dict:
        """Obtiene todas las entradas públicas."""
        return self._enviar_comando(ip, puerto, "TODAS")

    def obtener_por_alumno(self, ip: str, puerto: int, alumno: str) -> dict:
        """Obtiene entradas de un alumno específico."""
        return self._enviar_comando(ip, puerto, f"ALUMNO:{alumno}")

    def obtener_estadisticas(self, ip: str, puerto: int = 8080) -> dict:
        """Obtiene estadísticas de la bitácora remota."""
        return self._enviar_comando(ip, puerto, "ESTADISTICAS")

    def _enviar_comando(self, ip: str, puerto: int, comando: str) -> dict:
        """Envía un comando al servidor y retorna la respuesta."""
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(5)
            cliente.connect((ip, puerto))
            cliente.send(comando.encode('utf-8'))
            
            respuesta = b""
            while True:
                parte = cliente.recv(4096)
                if not parte:
                    break
                respuesta += parte
            
            cliente.close()
            return json.loads(respuesta.decode('utf-8'))
        except Exception as e:
            return {"error": str(e)}


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas para Servidor Local"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/servidor_local.py")
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

    # Crear bitácora de prueba
    from zonas.bitacora import Bitacora
    bitacora = Bitacora()
    bitacora.entradas = []
    bitacora.guardar()
    
    bitacora.agregar_entrada("observacion", "Ana López", "3A",
                             "Excelente", "María", "TEST001", publico=True)
    bitacora.agregar_entrada("reporte", "Carlos Ruiz", "3A",
                             "Faltas", "María", "TEST001", publico=True)
    bitacora.agregar_entrada("calificacion", "Ana López", "3A",
                             "9.5", "María", "TEST001", publico=True, calificacion=9.5)

    # Test Servidor
    servidor = ServidorBitacora(puerto=9876)  # Puerto no estándar para pruebas
    t(isinstance(servidor, ServidorBitacora), "Servidor instancia creada")
    t(not servidor.activo, "Servidor inactivo al inicio")

    # Iniciar servidor
    resultado = servidor.iniciar(bitacora, escuela="TEST001")
    t(resultado["exito"], "Servidor iniciado correctamente")
    t(servidor.activo, "Servidor marcado como activo")
    t("ip" in resultado, "Resultado incluye IP")
    t("puerto" in resultado, "Resultado incluye puerto")

    # Estado
    estado = servidor.estado()
    t(estado["activo"], "Estado: activo")
    t(estado["puerto"] == 9876, "Estado: puerto correcto")

    time.sleep(0.5)  # Esperar a que el servidor esté listo

    # Test Cliente
    cliente = ClienteBitacora()
    t(isinstance(cliente, ClienteBitacora), "Cliente instancia creada")

    # Conectar
    ip = resultado["ip"]
    conexion = cliente.conectar(ip, 9876)
    t(conexion["exito"], f"Cliente conectado a {ip}:9876")

    # Obtener total
    total = cliente.obtener_total(ip, 9876)
    t(total.get("total") == 3, f"Total remoto: {total.get('total')} entradas")

    # Obtener todas
    todas = cliente.obtener_todas(ip, 9876)
    t(todas.get("total") == 3, "Obtener todas: 3 entradas")
    t(len(todas.get("entradas", [])) == 3, "3 entradas en respuesta")

    # Obtener por alumno
    alumno = cliente.obtener_por_alumno(ip, 9876, "Ana")
    t(alumno.get("total") == 2, "Alumno 'Ana': 2 entradas")

    # Obtener estadísticas
    stats = cliente.obtener_estadisticas(ip, 9876)
    t(stats.get("total") == 3, "Estadísticas remotas: 3 total")

    # Detener servidor
    resultado = servidor.detener()
    t(resultado["exito"], "Servidor detenido")
    t(not servidor.activo, "Servidor inactivo tras detener")

    # Intentar conectar con servidor apagado
    conexion = cliente.conectar(ip, 9876)
    t(not conexion["exito"], "No se puede conectar con servidor apagado")

    # Limpiar
    try:
        os.remove("datos/bitacora.json")
    except:
        pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Servidor Local validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()