"""
🌿 Sana - Módulo de Gestión Escolar
═══════════════════════════════════════════════════════════════
Registro de escuelas, generación de códigos para docentes
y administrativos, verificación de acceso y administración.
100% local · Persistencia JSON · Test integrado.
═══════════════════════════════════════════════════════════════
"""

import json
import os
from datetime import datetime


class Escuelas:
    """
    Sistema de gestión escolar de Sana.
    
    Capacidades:
    - Registrar escuelas con datos completos
    - Generar códigos únicos para docentes (DOC-ESCUELA-001)
    - Generar códigos para administrativos (ADM-ESCUELA-001)
    - Verificar códigos de acceso
    - Código especial de administrador global
    - Persistencia en JSON local
    """

    # Código especial para acceder al panel de administrador
    CODIGO_ADMIN_GLOBAL = "SANA-ADMIN-2025"

    def __init__(self):
        self.escuelas = []
        self.docentes_registrados = []
        self._asegurar_directorio()
        self.cargar()

    def _asegurar_directorio(self):
        if not os.path.exists("datos"):
            os.makedirs("datos", exist_ok=True)

    def cargar(self):
        """Carga datos desde archivo JSON."""
        try:
            if os.path.exists("datos/escuelas.json"):
                with open("datos/escuelas.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.escuelas = datos.get("escuelas", [])
                    self.docentes_registrados = datos.get("docentes_registrados", [])
        except (json.JSONDecodeError, IOError):
            self.escuelas = []
            self.docentes_registrados = []

    def guardar(self):
        """Guarda datos en archivo JSON."""
        self._asegurar_directorio()
        with open("datos/escuelas.json", "w", encoding="utf-8") as f:
            json.dump({
                "escuelas": self.escuelas,
                "docentes_registrados": self.docentes_registrados,
                "ultima_actualizacion": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════════════
    # VERIFICACIÓN DE CÓDIGOS
    # ═══════════════════════════════════════════════════════════

    def verificar_codigo_admin(self, codigo: str) -> bool:
        """
        Verifica si un código es de administrador global.
        El código especial es: SANA-ADMIN-2025
        """
        return codigo.upper().strip() == self.CODIGO_ADMIN_GLOBAL

    def verificar_codigo_docente(self, codigo: str) -> dict:
        """
        Verifica si un código de docente es válido.
        
        Args:
            codigo: Código a verificar (ej: DOC-ESBJ-001)
        
        Returns:
            Diccionario con datos del docente o None si no es válido.
        """
        codigo = codigo.upper().strip()
        
        for escuela in self.escuelas:
            # Buscar en códigos de profesores
            for prof in escuela.get("codigos_profesores", []):
                if prof["codigo"] == codigo and prof.get("activo", True):
                    return {
                        "valido": True,
                        "codigo": codigo,
                        "tipo": "docente",
                        "escuela": escuela["nombre"],
                        "clave_escuela": escuela["clave"],
                        "numero": prof["numero"],
                        "asignado_a": prof.get("asignado_a", "")
                    }
            
            # Buscar en códigos de administrativos
            for adm in escuela.get("codigos_administrativos", []):
                if adm["codigo"] == codigo and adm.get("activo", True):
                    return {
                        "valido": True,
                        "codigo": codigo,
                        "tipo": "administrativo",
                        "escuela": escuela["nombre"],
                        "clave_escuela": escuela["clave"],
                        "numero": adm["numero"],
                        "asignado_a": adm.get("asignado_a", "")
                    }
        
        return None

    # ═══════════════════════════════════════════════════════════
    # REGISTRO DE ESCUELAS (ADMIN)
    # ═══════════════════════════════════════════════════════════

    def registrar_escuela(self, nombre: str, direccion: str = "",
                          telefono: str = "", email: str = "",
                          num_profesores: int = 0,
                          num_administrativos: int = 0) -> dict:
        """
        Registra una nueva escuela y genera códigos para su personal.
        
        Args:
            nombre: Nombre de la institución
            direccion: Dirección física
            telefono: Teléfono de contacto
            email: Correo institucional
            num_profesores: Cantidad de códigos para docentes
            num_administrativos: Cantidad de códigos para administrativos
        
        Returns:
            Diccionario con los datos de la escuela creada.
        """
        clave = self._generar_clave_escuela(nombre)
        
        escuela = {
            "id": len(self.escuelas) + 1,
            "nombre": nombre.strip(),
            "clave": clave,
            "direccion": direccion.strip(),
            "telefono": telefono.strip(),
            "email": email.strip(),
            "num_profesores": num_profesores,
            "num_administrativos": num_administrativos,
            "fecha_registro": datetime.now().isoformat(),
            "codigos_profesores": [],
            "codigos_administrativos": []
        }
        
        # Generar códigos para profesores
        for i in range(1, num_profesores + 1):
            escuela["codigos_profesores"].append({
                "numero": i,
                "codigo": f"DOC-{clave}-{str(i).zfill(3)}",
                "asignado_a": "",
                "activo": True,
                "fecha_generacion": datetime.now().isoformat()
            })
        
        # Generar códigos para administrativos
        for i in range(1, num_administrativos + 1):
            escuela["codigos_administrativos"].append({
                "numero": i,
                "codigo": f"ADM-{clave}-{str(i).zfill(3)}",
                "asignado_a": "",
                "activo": True,
                "fecha_generacion": datetime.now().isoformat()
            })
        
        self.escuelas.append(escuela)
        self.guardar()
        return escuela

    def _generar_clave_escuela(self, nombre: str) -> str:
        """Genera una clave única para la escuela basada en su nombre."""
        # Tomar primeras letras de cada palabra
        palabras = nombre.strip().split()
        iniciales = ''.join([p[0].upper() for p in palabras if len(p) > 2])[:4]
        if len(iniciales) < 2:
            iniciales = nombre.strip()[:4].upper()
        numero = str(len(self.escuelas) + 1).zfill(3)
        return f"{iniciales}{numero}"

    # ═══════════════════════════════════════════════════════════
    # CONSULTAS
    # ═══════════════════════════════════════════════════════════

    def obtener_escuelas(self) -> list:
        """Retorna todas las escuelas registradas."""
        return self.escuelas

    def obtener_escuela_por_clave(self, clave: str) -> dict:
        """Busca una escuela por su clave."""
        for escuela in self.escuelas:
            if escuela["clave"] == clave.upper().strip():
                return escuela
        return None

    def obtener_escuela_por_nombre(self, nombre: str) -> dict:
        """Busca una escuela por su nombre (búsqueda parcial)."""
        nombre = nombre.lower().strip()
        for escuela in self.escuelas:
            if nombre in escuela["nombre"].lower():
                return escuela
        return None

    def obtener_codigos_escuela(self, clave_escuela: str) -> dict:
        """
        Retorna todos los códigos de una escuela.
        Útil para que el admin vea los códigos generados.
        """
        escuela = self.obtener_escuela_por_clave(clave_escuela)
        if not escuela:
            return None
        return {
            "escuela": escuela["nombre"],
            "clave": escuela["clave"],
            "profesores": escuela.get("codigos_profesores", []),
            "administrativos": escuela.get("codigos_administrativos", []),
            "total_profesores": len(escuela.get("codigos_profesores", [])),
            "total_administrativos": len(escuela.get("codigos_administrativos", []))
        }

    def obtener_nombres_escuelas(self) -> list:
        """Retorna lista simple con nombres de escuelas."""
        return [e["nombre"] for e in self.escuelas]

    # ═══════════════════════════════════════════════════════════
    # GESTIÓN DE DOCENTES
    # ═══════════════════════════════════════════════════════════

    def registrar_docente(self, codigo: str, nombre: str,
                          materia: str = "", email: str = "") -> dict:
        """
        Registra un docente con su código y lo asigna.
        
        Args:
            codigo: Código del docente (DOC-ESCUELA-001)
            nombre: Nombre completo
            materia: Materia que imparte
            email: Correo de contacto
        
        Returns:
            Diccionario con resultado y mensaje.
        """
        codigo = codigo.upper().strip()
        
        # Verificar que el código existe
        verificacion = self.verificar_codigo_docente(codigo)
        if not verificacion:
            return {"exito": False, "mensaje": "Código no válido."}
        
        # Registrar docente
        docente = {
            "codigo": codigo,
            "nombre": nombre.strip(),
            "materia": materia.strip(),
            "email": email.strip(),
            "escuela": verificacion["escuela"],
            "clave_escuela": verificacion["clave_escuela"],
            "tipo": verificacion["tipo"],
            "fecha_registro": datetime.now().isoformat()
        }
        self.docentes_registrados.append(docente)
        
        # Marcar código como asignado en la escuela
        for escuela in self.escuelas:
            if escuela["clave"] == verificacion["clave_escuela"]:
                for prof in escuela.get("codigos_profesores", []):
                    if prof["codigo"] == codigo:
                        prof["asignado_a"] = nombre.strip()
                for adm in escuela.get("codigos_administrativos", []):
                    if adm["codigo"] == codigo:
                        adm["asignado_a"] = nombre.strip()
        
        self.guardar()
        return {
            "exito": True,
            "mensaje": f"✅ {nombre} registrado/a exitosamente.",
            "docente": docente
        }

    def obtener_docentes_escuela(self, clave_escuela: str) -> list:
        """Retorna los docentes registrados de una escuela."""
        return [d for d in self.docentes_registrados 
                if d.get("clave_escuela") == clave_escuela.upper().strip()]

    def obtener_docente_por_codigo(self, codigo: str) -> dict:
        """Busca un docente por su código."""
        codigo = codigo.upper().strip()
        for d in self.docentes_registrados:
            if d["codigo"] == codigo:
                return d
        return None

    # ═══════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════

    def desactivar_codigo(self, codigo: str) -> dict:
        """Desactiva un código de docente/administrativo."""
        codigo = codigo.upper().strip()
        for escuela in self.escuelas:
            for lista in ["codigos_profesores", "codigos_administrativos"]:
                for item in escuela.get(lista, []):
                    if item["codigo"] == codigo:
                        item["activo"] = False
                        self.guardar()
                        return {"exito": True, "mensaje": f"Código {codigo} desactivado."}
        return {"exito": False, "mensaje": "Código no encontrado."}

    def reactivar_codigo(self, codigo: str) -> dict:
        """Reactivar un código desactivado."""
        codigo = codigo.upper().strip()
        for escuela in self.escuelas:
            for lista in ["codigos_profesores", "codigos_administrativos"]:
                for item in escuela.get(lista, []):
                    if item["codigo"] == codigo:
                        item["activo"] = True
                        self.guardar()
                        return {"exito": True, "mensaje": f"Código {codigo} reactivado."}
        return {"exito": False, "mensaje": "Código no encontrado."}

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas generales del sistema."""
        total_profesores = 0
        total_administrativos = 0
        codigos_asignados = 0
        
        for escuela in self.escuelas:
            total_profesores += escuela.get("num_profesores", 0)
            total_administrativos += escuela.get("num_administrativos", 0)
            for prof in escuela.get("codigos_profesores", []):
                if prof.get("asignado_a"):
                    codigos_asignados += 1
        
        return {
            "total_escuelas": len(self.escuelas),
            "total_docentes_registrados": len(self.docentes_registrados),
            "total_codigos_profesores": total_profesores,
            "total_codigos_administrativos": total_administrativos,
            "codigos_asignados": codigos_asignados,
            "codigos_disponibles": total_profesores - codigos_asignados
        }


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas para Escuelas"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/escuelas.py")
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

    # Limpiar datos de prueba anteriores
    try:
        os.remove("datos/escuelas.json")
    except:
        pass

    e = Escuelas()
    t(isinstance(e, Escuelas), "Instancia creada correctamente")
    t(len(e.obtener_escuelas()) == 0, "Sin escuelas al inicio")

    # Código admin
    t(e.verificar_codigo_admin("SANA-ADMIN-2025"), "Código admin válido")
    t(e.verificar_codigo_admin("sana-admin-2025"), "Código admin válido (minúsculas)")
    t(not e.verificar_codigo_admin("CODIGO-FALSO"), "Código falso rechazado")
    t(not e.verificar_codigo_admin(""), "Código vacío rechazado")

    # Registrar escuela
    escuela = e.registrar_escuela(
        nombre="Escuela Secundaria Benito Juárez",
        direccion="Av. Reforma 123",
        telefono="555-123-4567",
        email="benitojuarez@escuela.edu.mx",
        num_profesores=3,
        num_administrativos=1
    )
    t(escuela["nombre"] == "Escuela Secundaria Benito Juárez", "Nombre guardado")
    t(escuela["direccion"] == "Av. Reforma 123", "Dirección guardada")
    t(escuela["num_profesores"] == 3, "Número de profesores guardado")
    t(escuela["num_administrativos"] == 1, "Número de administrativos guardado")
    t("clave" in escuela, "Clave generada automáticamente")
    t(len(escuela["codigos_profesores"]) == 3, "3 códigos de profesor generados")
    t(len(escuela["codigos_administrativos"]) == 1, "1 código administrativo generado")

    # Verificar códigos generados
    codigo_prof_1 = escuela["codigos_profesores"][0]["codigo"]
    t("DOC-" in codigo_prof_1, "Código docente tiene prefijo DOC-")
    
    verificacion = e.verificar_codigo_docente(codigo_prof_1)
    t(verificacion is not None, "Código docente verificado correctamente")
    t(verificacion["valido"], "Código marcado como válido")
    t(verificacion["escuela"] == "Escuela Secundaria Benito Juárez", "Escuela correcta en verificación")
    t(verificacion["tipo"] == "docente", "Tipo docente detectado")

    # Código administrativo
    codigo_adm = escuela["codigos_administrativos"][0]["codigo"]
    t("ADM-" in codigo_adm, "Código admin tiene prefijo ADM-")
    verificacion_adm = e.verificar_codigo_docente(codigo_adm)
    t(verificacion_adm["tipo"] == "administrativo", "Tipo administrativo detectado")

    # Código inexistente
    t(e.verificar_codigo_docente("DOC-FALSO-999") is None, "Código falso rechazado")

    # Registrar docente
    resultado = e.registrar_docente(codigo_prof_1, "María García", "Matemáticas", "maria@escuela.edu.mx")
    t(resultado["exito"], "Docente registrado exitosamente")
    t(resultado["docente"]["nombre"] == "María García", "Nombre guardado")
    t(resultado["docente"]["materia"] == "Matemáticas", "Materia guardada")

    # Verificar asignación
    codigos = e.obtener_codigos_escuela(escuela["clave"])
    t(codigos["profesores"][0]["asignado_a"] == "María García", "Código marcado como asignado")

    # Obtener docentes de escuela
    docentes = e.obtener_docentes_escuela(escuela["clave"])
    t(len(docentes) == 1, "1 docente en la escuela")

    # Obtener docente por código
    docente = e.obtener_docente_por_codigo(codigo_prof_1)
    t(docente["nombre"] == "María García", "Docente encontrado por código")

    # Registrar segunda escuela
    escuela2 = e.registrar_escuela("Colegio Miguel Hidalgo", num_profesores=2, num_administrativos=0)
    t(len(e.obtener_escuelas()) == 2, "2 escuelas registradas")
    t(len(e.obtener_nombres_escuelas()) == 2, "2 nombres de escuelas")

    # Estadísticas
    stats = e.obtener_estadisticas()
    t(stats["total_escuelas"] == 2, "Estadísticas: 2 escuelas")
    t(stats["total_docentes_registrados"] == 1, "Estadísticas: 1 docente")
    t(stats["codigos_asignados"] == 1, "Estadísticas: 1 código asignado")

    # Desactivar código
    resultado = e.desactivar_codigo(codigo_prof_1)
    t(resultado["exito"], "Código desactivado")
    t(e.verificar_codigo_docente(codigo_prof_1) is None, "Código desactivado no verifica")

    # Reactivar código
    resultado = e.reactivar_codigo(codigo_prof_1)
    t(resultado["exito"], "Código reactivado")
    t(e.verificar_codigo_docente(codigo_prof_1) is not None, "Código reactivado verifica")

    # Persistencia
    e2 = Escuelas()
    t(len(e2.obtener_escuelas()) == 2, "Datos persisten tras recargar")

    # Limpiar
    try:
        os.remove("datos/escuelas.json")
    except:
        pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Escuelas validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()