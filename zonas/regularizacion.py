"""
🌿 Sana - Módulo de Regularización Académica
═══════════════════════════════════════════════════════════════
Material de estudio personalizado, planes de estudio, ejercicios
y recursos educativos. Los profesores pueden subir material y
los alumnos acceder a planes personalizados.
100% local · Persistencia JSON · Test integrado.
═══════════════════════════════════════════════════════════════
"""

import json
import os
from datetime import datetime


class Regularizacion:
    """
    Sistema de regularización académica de Sana.
    
    Capacidades:
    - Crear planes de estudio personalizados por alumno
    - Subir material de estudio por materia
    - Registrar ejercicios y recursos
    - Seguimiento de progreso del alumno
    - Categorías: matemáticas, español, ciencias, historia, inglés
    - Niveles de dificultad
    - Evaluaciones y retroalimentación
    """

    MATERIAS = [
        "Matemáticas", "Español", "Ciencias Naturales",
        "Historia", "Geografía", "Inglés", "Física",
        "Química", "Biología", "Formación Cívica", "Otra"
    ]

    NIVELES = ["Básico", "Intermedio", "Avanzado"]

    def __init__(self):
        self.materiales = []
        self.planes = []
        self.ejercicios = []
        self._asegurar_directorio()
        self.cargar()

    def _asegurar_directorio(self):
        if not os.path.exists("datos"):
            os.makedirs("datos", exist_ok=True)

    def cargar(self):
        try:
            if os.path.exists("datos/regularizacion.json"):
                with open("datos/regularizacion.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.materiales = datos.get("materiales", [])
                    self.planes = datos.get("planes", [])
                    self.ejercicios = datos.get("ejercicios", [])
        except (json.JSONDecodeError, IOError):
            self.materiales = []
            self.planes = []
            self.ejercicios = []

    def guardar(self):
        self._asegurar_directorio()
        with open("datos/regularizacion.json", "w", encoding="utf-8") as f:
            json.dump({
                "materiales": self.materiales,
                "planes": self.planes,
                "ejercicios": self.ejercicios,
                "ultima_actualizacion": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════════════
    # MATERIAL DE ESTUDIO
    # ═══════════════════════════════════════════════════════════

    def agregar_material(self, titulo: str, materia: str, contenido: str,
                         autor: str, nivel: str = "Básico",
                         etiquetas: list = None, escuela: str = "") -> dict:
        """
        Agrega material de estudio.
        
        Args:
            titulo: Título del material
            materia: Materia (debe estar en MATERIAS)
            contenido: Texto completo del material
            autor: Nombre del profesor que lo sube
            nivel: Básico, Intermedio o Avanzado
            etiquetas: Lista de palabras clave
            escuela: Clave de la escuela (opcional)
        
        Returns:
            Diccionario con el material creado.
        """
        if materia not in self.MATERIAS:
            materia = "Otra"
        if nivel not in self.NIVELES:
            nivel = "Básico"

        material = {
            "id": len(self.materiales) + 1,
            "titulo": titulo.strip(),
            "materia": materia,
            "contenido": contenido.strip(),
            "autor": autor.strip(),
            "nivel": nivel,
            "etiquetas": etiquetas or [],
            "escuela": escuela.strip(),
            "fecha_creacion": datetime.now().isoformat(),
            "descargas": 0,
            "favorito": False
        }
        self.materiales.append(material)
        self.guardar()
        return material

    def obtener_materiales(self, materia: str = None, nivel: str = None,
                           autor: str = None, etiqueta: str = None,
                           escuela: str = None, busqueda: str = None) -> list:
        """
        Filtra materiales por múltiples criterios.
        """
        resultado = self.materiales.copy()

        if materia:
            resultado = [m for m in resultado if m.get("materia") == materia]
        if nivel:
            resultado = [m for m in resultado if m.get("nivel") == nivel]
        if autor:
            resultado = [m for m in resultado if autor.lower() in m.get("autor", "").lower()]
        if etiqueta:
            resultado = [m for m in resultado if etiqueta in m.get("etiquetas", [])]
        if escuela:
            resultado = [m for m in resultado if m.get("escuela", "").upper() == escuela.upper()]
        if busqueda:
            busqueda = busqueda.lower()
            resultado = [m for m in resultado 
                        if busqueda in m.get("titulo", "").lower() 
                        or busqueda in m.get("contenido", "").lower()]

        return sorted(resultado, key=lambda m: m.get("fecha_creacion", ""), reverse=True)

    def obtener_material_por_id(self, id_material: int) -> dict:
        for m in self.materiales:
            if m["id"] == id_material:
                return m
        return None

    def eliminar_material(self, id_material: int) -> dict:
        for i, m in enumerate(self.materiales):
            if m["id"] == id_material:
                self.materiales.pop(i)
                self.guardar()
                return {"exito": True, "mensaje": "Material eliminado."}
        return {"exito": False, "mensaje": "Material no encontrado."}

    def marcar_favorito(self, id_material: int) -> dict:
        for m in self.materiales:
            if m["id"] == id_material:
                m["favorito"] = not m.get("favorito", False)
                self.guardar()
                return {"exito": True, "favorito": m["favorito"]}
        return {"exito": False}

    def incrementar_descarga(self, id_material: int):
        for m in self.materiales:
            if m["id"] == id_material:
                m["descargas"] = m.get("descargas", 0) + 1
                self.guardar()

    # ═══════════════════════════════════════════════════════════
    # PLANES DE ESTUDIO PERSONALIZADOS
    # ═══════════════════════════════════════════════════════════

    def crear_plan(self, alumno: str, materia: str, objetivo: str,
                   profesor: str, duracion_semanas: int = 4,
                   temas: list = None, escuela: str = "") -> dict:
        """
        Crea un plan de estudio personalizado para un alumno.
        
        Args:
            alumno: Nombre del alumno
            materia: Materia a reforzar
            objetivo: Meta del plan (ej: "Aprobar examen de álgebra")
            profesor: Nombre del profesor que lo crea
            duracion_semanas: Semanas de duración
            temas: Lista de temas a cubrir
            escuela: Clave de la escuela
        
        Returns:
            Diccionario con el plan creado.
        """
        if materia not in self.MATERIAS:
            materia = "Otra"

        plan = {
            "id": len(self.planes) + 1,
            "alumno": alumno.strip(),
            "materia": materia,
            "objetivo": objetivo.strip(),
            "profesor": profesor.strip(),
            "duracion_semanas": duracion_semanas,
            "temas": temas or [],
            "escuela": escuela.strip(),
            "fecha_creacion": datetime.now().isoformat(),
            "progreso": 0.0,
            "completado": False,
            "fecha_completado": None,
            "notas_seguimiento": []
        }
        self.planes.append(plan)
        self.guardar()
        return plan

    def actualizar_progreso(self, id_plan: int, porcentaje: float,
                            nota: str = "") -> dict:
        """Actualiza el progreso de un plan de estudio."""
        for plan in self.planes:
            if plan["id"] == id_plan:
                plan["progreso"] = max(0, min(100, porcentaje))
                if nota:
                    plan["notas_seguimiento"].append({
                        "fecha": datetime.now().isoformat(),
                        "nota": nota.strip(),
                        "progreso": plan["progreso"]
                    })
                if plan["progreso"] >= 100:
                    plan["completado"] = True
                    plan["fecha_completado"] = datetime.now().isoformat()
                self.guardar()
                return {"exito": True, "plan": plan}
        return {"exito": False, "mensaje": "Plan no encontrado."}

    def obtener_planes(self, alumno: str = None, profesor: str = None,
                       materia: str = None, escuela: str = None,
                       solo_pendientes: bool = False) -> list:
        """Filtra planes de estudio."""
        resultado = self.planes.copy()

        if alumno:
            resultado = [p for p in resultado if alumno.lower() in p.get("alumno", "").lower()]
        if profesor:
            resultado = [p for p in resultado if profesor.lower() in p.get("profesor", "").lower()]
        if materia:
            resultado = [p for p in resultado if p.get("materia") == materia]
        if escuela:
            resultado = [p for p in resultado if p.get("escuela", "").upper() == escuela.upper()]
        if solo_pendientes:
            resultado = [p for p in resultado if not p.get("completado", False)]

        return sorted(resultado, key=lambda p: p.get("fecha_creacion", ""), reverse=True)

    def eliminar_plan(self, id_plan: int) -> dict:
        for i, p in enumerate(self.planes):
            if p["id"] == id_plan:
                self.planes.pop(i)
                self.guardar()
                return {"exito": True, "mensaje": "Plan eliminado."}
        return {"exito": False, "mensaje": "Plan no encontrado."}

    # ═══════════════════════════════════════════════════════════
    # EJERCICIOS
    # ═══════════════════════════════════════════════════════════

    def agregar_ejercicio(self, titulo: str, materia: str, enunciado: str,
                          solucion: str = "", nivel: str = "Básico",
                          autor: str = "", escuela: str = "") -> dict:
        """
        Agrega un ejercicio de práctica.
        """
        if materia not in self.MATERIAS:
            materia = "Otra"
        if nivel not in self.NIVELES:
            nivel = "Básico"

        ejercicio = {
            "id": len(self.ejercicios) + 1,
            "titulo": titulo.strip(),
            "materia": materia,
            "enunciado": enunciado.strip(),
            "solucion": solucion.strip(),
            "nivel": nivel,
            "autor": autor.strip(),
            "escuela": escuela.strip(),
            "fecha_creacion": datetime.now().isoformat()
        }
        self.ejercicios.append(ejercicio)
        self.guardar()
        return ejercicio

    def obtener_ejercicios(self, materia: str = None, nivel: str = None) -> list:
        resultado = self.ejercicios.copy()
        if materia:
            resultado = [e for e in resultado if e.get("materia") == materia]
        if nivel:
            resultado = [e for e in resultado if e.get("nivel") == nivel]
        return sorted(resultado, key=lambda e: e.get("fecha_creacion", ""), reverse=True)

    # ═══════════════════════════════════════════════════════════
    # ESTADÍSTICAS
    # ═══════════════════════════════════════════════════════════

    def obtener_estadisticas(self, escuela: str = None) -> dict:
        planes = self.obtener_planes(escuela=escuela)
        materiales = self.obtener_materiales(escuela=escuela)
        ejercicios = self.obtener_ejercicios()

        return {
            "total_materiales": len(materiales),
            "total_planes": len(planes),
            "total_ejercicios": len(ejercicios),
            "planes_completados": len([p for p in planes if p.get("completado")]),
            "planes_en_progreso": len([p for p in planes if not p.get("completado")]),
            "alumnos_con_plan": len(set(p["alumno"] for p in planes)),
            "materia_mas_solicitada": self._materia_mas_comun(planes),
            "descargas_totales": sum(m.get("descargas", 0) for m in materiales),
            "materiales_favoritos": len([m for m in materiales if m.get("favorito")])
        }

    def _materia_mas_comun(self, planes: list) -> str:
        if not planes:
            return "Ninguna"
        from collections import Counter
        conteo = Counter(p["materia"] for p in planes)
        return conteo.most_common(1)[0][0]

    def obtener_materias(self) -> list:
        return self.MATERIAS

    def obtener_niveles(self) -> list:
        return self.NIVELES


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas para Regularizacion"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: zonas/regularizacion.py")
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

    try:
        os.remove("datos/regularizacion.json")
    except:
        pass

    r = Regularizacion()
    t(isinstance(r, Regularizacion), "Instancia creada")
    t(len(r.MATERIAS) >= 10, f"{len(r.MATERIAS)} materias disponibles")
    t(len(r.NIVELES) == 3, "3 niveles de dificultad")

    # Agregar material
    m1 = r.agregar_material(
        titulo="Introducción al Álgebra",
        materia="Matemáticas",
        contenido="El álgebra es la rama de las matemáticas que estudia...",
        autor="Prof. María García",
        nivel="Básico",
        etiquetas=["álgebra", "secundaria", "ecuaciones"],
        escuela="ESBJ001"
    )
    t(m1["titulo"] == "Introducción al Álgebra", "Título guardado")
    t(m1["materia"] == "Matemáticas", "Materia guardada")
    t(m1["nivel"] == "Básico", "Nivel guardado")
    t("álgebra" in m1["etiquetas"], "Etiquetas guardadas")
    t(m1["descargas"] == 0, "Descargas inicia en 0")

    m2 = r.agregar_material(
        titulo="Ejercicios de Factorización",
        materia="Matemáticas",
        contenido="Practica factorización con estos ejercicios...",
        autor="Prof. Juan Pérez",
        nivel="Intermedio",
        escuela="ESBJ001"
    )
    t(len(r.materiales) == 2, "2 materiales registrados")

    # Filtrar materiales
    t(len(r.obtener_materiales(materia="Matemáticas")) == 2, "Filtro por materia: 2")
    t(len(r.obtener_materiales(nivel="Básico")) == 1, "Filtro por nivel: 1")
    t(len(r.obtener_materiales(autor="María")) == 1, "Filtro por autor: 1")
    t(len(r.obtener_materiales(etiqueta="álgebra")) == 1, "Filtro por etiqueta: 1")
    t(len(r.obtener_materiales(escuela="ESBJ001")) == 2, "Filtro por escuela: 2")
    t(len(r.obtener_materiales(busqueda="factorización")) == 1, "Búsqueda: 1")

    # Obtener por ID
    t(r.obtener_material_por_id(1)["titulo"] == "Introducción al Álgebra", "Material por ID")
    t(r.obtener_material_por_id(999) is None, "ID inexistente: None")

    # Favorito
    resultado = r.marcar_favorito(1)
    t(resultado["favorito"], "Marcado como favorito")
    resultado = r.marcar_favorito(1)
    t(not resultado["favorito"], "Desmarcado de favorito")

    # Descarga
    r.incrementar_descarga(1)
    t(r.obtener_material_por_id(1)["descargas"] == 1, "Contador de descargas")

    # Eliminar material
    t(r.eliminar_material(2)["exito"], "Material eliminado")
    t(len(r.materiales) == 1, "1 material restante")

    # Crear plan de estudio
    plan = r.crear_plan(
        alumno="Ana López",
        materia="Matemáticas",
        objetivo="Aprobar examen de álgebra con mínimo 8",
        profesor="María García",
        duracion_semanas=4,
        temas=["Ecuaciones lineales", "Factorización", "Polinomios"],
        escuela="ESBJ001"
    )
    t(plan["alumno"] == "Ana López", "Alumno guardado en plan")
    t(plan["materia"] == "Matemáticas", "Materia guardada en plan")
    t(plan["duracion_semanas"] == 4, "Duración guardada")
    t(len(plan["temas"]) == 3, "3 temas en el plan")
    t(plan["progreso"] == 0.0, "Progreso inicial 0%")
    t(not plan["completado"], "No completado al inicio")

    # Actualizar progreso
    resultado = r.actualizar_progreso(1, 50, "Avanzando bien en ecuaciones")
    t(resultado["exito"], "Progreso actualizado")
    t(resultado["plan"]["progreso"] == 50, "Progreso al 50%")
    t(len(resultado["plan"]["notas_seguimiento"]) == 1, "Nota de seguimiento guardada")

    # Completar plan
    resultado = r.actualizar_progreso(1, 100, "¡Plan completado!")
    t(resultado["plan"]["completado"], "Plan marcado como completado")
    t(resultado["plan"]["fecha_completado"] is not None, "Fecha de completado registrada")

    # Filtrar planes
    t(len(r.obtener_planes(alumno="Ana")) == 1, "Plan de Ana encontrado")
    t(len(r.obtener_planes(profesor="María")) == 1, "Plan de María encontrado")
    t(len(r.obtener_planes(solo_pendientes=True)) == 0, "Sin planes pendientes")
    t(len(r.obtener_planes(escuela="ESBJ001")) == 1, "Filtro por escuela en planes")

    # Agregar ejercicios
    ej = r.agregar_ejercicio(
        titulo="Ecuaciones lineales",
        materia="Matemáticas",
        enunciado="Resuelve: 2x + 5 = 15",
        solucion="x = 5",
        nivel="Básico",
        autor="María García",
        escuela="ESBJ001"
    )
    t(ej["titulo"] == "Ecuaciones lineales", "Ejercicio guardado")
    t(ej["solucion"] == "x = 5", "Solución guardada")
    t(len(r.obtener_ejercicios(materia="Matemáticas")) == 1, "Filtro ejercicios por materia")

    # Estadísticas
    stats = r.obtener_estadisticas(escuela="ESBJ001")
    t(stats["total_materiales"] == 1, "Stats: 1 material")
    t(stats["total_planes"] == 1, "Stats: 1 plan")
    t(stats["planes_completados"] == 1, "Stats: 1 completado")
    t(stats["alumnos_con_plan"] == 1, "Stats: 1 alumno")
    t(stats["total_ejercicios"] == 1, "Stats: 1 ejercicio")

    # Persistencia
    r2 = Regularizacion()
    t(len(r2.materiales) == 1, "Materiales persisten")
    t(len(r2.planes) == 1, "Planes persisten")
    t(len(r2.ejercicios) == 1, "Ejercicios persisten")

    # Limpiar
    try:
        os.remove("datos/regularizacion.json")
    except:
        pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Regularización validada\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()