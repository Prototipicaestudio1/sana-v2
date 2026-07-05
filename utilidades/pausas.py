"""
🌿 Sana - Módulo de Pausas y Temporización Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Gestor de pausas, temporizadores, cronómetros y ciclos de
respiración con callbacks para la UI. Diseñado para ejercicios
de respiración guiada, Pomodoro, cuenta regresiva y más.
═══════════════════════════════════════════════════════════════
"""

import time
import threading
from datetime import datetime, timedelta


class Pausas:
    """
    Maestro del tiempo de Sana.
    
    Capacidades:
    - Pausas simples (corta, media, larga, personalizada)
    - Cuenta regresiva con callbacks por segundo y al finalizar
    - Cronómetro en segundo plano (threading)
    - Ciclos de respiración completos (inhalar, retener, exhalar)
    - Temporizador Pomodoro (trabajo/descanso)
    - Formateo de tiempo legible y amigable
    - Barras de progreso para UI
    - Estimación de finalización
    """

    def __init__(self):
        self._pausa_activa = False
        self._segundos_transcurridos = 0
        self._hilo = None
        self._pomodoro_activo = False
        self._pomodoro_tipo = None  # 'trabajo' o 'descanso'
        self._pomodoro_ciclo = 0
        self._historial = []

    # ═══════════════════════════════════════════════════════════
    # PAUSAS SIMPLES
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def pausa_corta():
        """Pausa breve de 1 segundo. Ideal entre mensajes."""
        time.sleep(1)

    @staticmethod
    def pausa_media():
        """Pausa de 2 segundos. Para transiciones suaves."""
        time.sleep(2)

    @staticmethod
    def pausa_larga():
        """Pausa de 3 segundos. Para momentos de reflexión."""
        time.sleep(3)

    @staticmethod
    def pausa_personalizada(segundos: float):
        """Pausa de duración exacta. Acepta decimales."""
        if segundos > 0:
            time.sleep(segundos)

    @staticmethod
    def pausa_respiracion(tipo: str = "normal"):
        """
        Pausas predefinidas para ejercicios de respiración.
        Tipos: 'normal' (1s), 'profunda' (2s), 'transicion' (1.5s).
        """
        pausas = {"normal": 1.0, "profunda": 2.0, "transicion": 1.5}
        time.sleep(pausas.get(tipo, 1.0))

    # ═══════════════════════════════════════════════════════════
    # CUENTA REGRESIVA
    # ═══════════════════════════════════════════════════════════

    def cuenta_regresiva(self, segundos: int, callback_segundo=None, 
                         callback_fin=None, callback_progreso=None) -> bool:
        """
        Ejecuta cuenta regresiva con callbacks.
        
        Args:
            segundos: Duración total.
            callback_segundo: Llamado cada segundo (recibe: segundo_actual).
            callback_fin: Llamado al finalizar.
            callback_progreso: Llamado con (actual, total) para barras.
        
        Returns:
            True si completó, False si fue detenida.
        """
        self._pausa_activa = True
        completada = True
        
        for i in range(segundos, 0, -1):
            if not self._pausa_activa:
                completada = False
                break
            if callback_segundo:
                callback_segundo(i)
            if callback_progreso:
                callback_progreso(segundos - i + 1, segundos)
            time.sleep(1)
        
        self._pausa_activa = False
        if completada and callback_fin:
            callback_fin()
        return completada

    def detener_cuenta_regresiva(self):
        """Detiene la cuenta regresiva en curso."""
        self._pausa_activa = False

    def cuenta_regresiva_con_mensajes(self, segundos: int, 
                                       mensajes: list, callback_mensaje=None) -> bool:
        """
        Cuenta regresiva con mensajes personalizados en segundos específicos.
        
        Args:
            segundos: Duración total.
            mensajes: Lista de tuplas (segundo, mensaje).
            callback_mensaje: Función que recibe el mensaje.
        """
        mensajes_dict = {s: m for s, m in mensajes}
        
        def on_segundo(s):
            if callback_mensaje and s in mensajes_dict:
                callback_mensaje(mensajes_dict[s])
        
        return self.cuenta_regresiva(segundos, callback_segundo=on_segundo)

    # ═══════════════════════════════════════════════════════════
    # CRONÓMETRO
    # ═══════════════════════════════════════════════════════════

    def iniciar_cronometro(self):
        """Inicia cronómetro en segundo plano (threading)."""
        self._segundos_transcurridos = 0
        self._pausa_activa = True
        
        def _contar():
            while self._pausa_activa:
                time.sleep(1)
                self._segundos_transcurridos += 1
        
        self._hilo = threading.Thread(target=_contar, daemon=True)
        self._hilo.start()

    def detener_cronometro(self) -> int:
        """Detiene cronómetro y retorna segundos transcurridos."""
        self._pausa_activa = False
        if self._hilo:
            self._hilo.join(timeout=2)
        return self._segundos_transcurridos

    def pausar_cronometro(self):
        """Pausa el cronómetro sin reiniciarlo."""
        self._pausa_activa = False

    def reanudar_cronometro(self):
        """Reanuda el cronómetro desde donde estaba."""
        if not self._pausa_activa:
            self._pausa_activa = True
            def _contar():
                while self._pausa_activa:
                    time.sleep(1)
                    self._segundos_transcurridos += 1
            self._hilo = threading.Thread(target=_contar, daemon=True)
            self._hilo.start()

    def reiniciar_cronometro(self):
        """Reinicia el cronómetro a cero."""
        self._pausa_activa = False
        self._segundos_transcurridos = 0

    def obtener_tiempo_cronometro(self) -> int:
        """Retorna segundos transcurridos sin detener el cronómetro."""
        return self._segundos_transcurridos

    # ═══════════════════════════════════════════════════════════
    # POMODORO
    # ═══════════════════════════════════════════════════════════

    def iniciar_pomodoro(self, trabajo: int = 25, descanso: int = 5,
                         ciclos: int = 4, callback_cambio=None, callback_fin=None) -> bool:
        """
        Inicia un ciclo Pomodoro completo.
        
        Args:
            trabajo: Minutos de trabajo (default 25).
            descanso: Minutos de descanso (default 5).
            ciclos: Número de ciclos (default 4).
            callback_cambio: Llamado al cambiar entre trabajo/descanso.
            callback_fin: Llamado al finalizar todos los ciclos.
        
        Returns:
            True si completó todos los ciclos.
        """
        self._pomodoro_activo = True
        
        for ciclo in range(1, ciclos + 1):
            if not self._pomodoro_activo:
                return False
            
            self._pomodoro_ciclo = ciclo
            self._pomodoro_tipo = "trabajo"
            if callback_cambio:
                callback_cambio("trabajo", ciclo, ciclos)
            
            # Fase de trabajo
            self.cuenta_regresiva(trabajo * 60)
            
            if ciclo < ciclos:
                self._pomodoro_tipo = "descanso"
                if callback_cambio:
                    callback_cambio("descanso", ciclo, ciclos)
                self.cuenta_regresiva(descanso * 60)
        
        self._pomodoro_activo = False
        self._pomodoro_tipo = None
        if callback_fin:
            callback_fin()
        return True

    def detener_pomodoro(self):
        """Detiene el ciclo Pomodoro."""
        self._pomodoro_activo = False
        self.detener_cuenta_regresiva()

    def estado_pomodoro(self) -> dict:
        """Retorna el estado actual del Pomodoro."""
        return {
            "activo": self._pomodoro_activo,
            "tipo": self._pomodoro_tipo,
            "ciclo": self._pomodoro_ciclo
        }

    # ═══════════════════════════════════════════════════════════
    # CICLOS DE RESPIRACIÓN
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def ciclo_respiracion(inhalar: int, retener: int, exhalar: int, 
                          callback=None, callback_progreso=None) -> dict:
        """
        Ejecuta un ciclo de respiración completo.
        
        Args:
            inhalar: Segundos para inhalar.
            retener: Segundos para retener (0 para omitir).
            exhalar: Segundos para exhalar.
            callback: Función(nombre_fase, segundos) en cada fase.
            callback_progreso: Función(progreso_decimal) para barras.
        
        Returns:
            Diccionario con resumen del ciclo.
        """
        fases = []
        if inhalar > 0:
            fases.append(("Inhala", inhalar))
        if retener > 0:
            fases.append(("Retén", retener))
        if exhalar > 0:
            fases.append(("Exhala", exhalar))
        
        total = sum(s for _, s in fases)
        transcurrido = 0
        
        for nombre, segundos in fases:
            if callback:
                callback(nombre, segundos)
            time.sleep(segundos)
            transcurrido += segundos
            if callback_progreso:
                callback_progreso(transcurrido / total)
        
        return {
            "fases": len(fases),
            "tiempo_total": total,
            "completado": True
        }

    @staticmethod
    def ciclo_completo(ejercicio: dict, callback_fase=None, 
                       callback_ciclo=None, callback_fin=None) -> bool:
        """
        Ejecuta múltiples ciclos de un ejercicio completo.
        
        Args:
            ejercicio: Diccionario con 'pasos' y 'ciclos'.
            callback_fase: (texto, segundos) en cada fase.
            callback_ciclo: (ciclo_actual, total_ciclos) al terminar cada ciclo.
            callback_fin: Al finalizar todos los ciclos.
        """
        pasos = ejercicio.get("pasos", [])
        ciclos = ejercicio.get("ciclos", 1)
        
        for c in range(ciclos):
            for texto, segundos in pasos:
                if callback_fase:
                    callback_fase(texto, segundos)
                time.sleep(segundos)
            if callback_ciclo:
                callback_ciclo(c + 1, ciclos)
        
        if callback_fin:
            callback_fin()
        return True

    # ═══════════════════════════════════════════════════════════
    # FORMATEO DE TIEMPO
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def formatear_tiempo(segundos: int) -> str:
        """Convierte segundos a formato legible: '1h 2m 30s'."""
        if segundos < 0:
            return "0s"
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segs = segundos % 60
        partes = []
        if horas > 0:
            partes.append(f"{horas}h")
        if minutos > 0 or horas > 0:
            partes.append(f"{minutos}m")
        partes.append(f"{segs}s")
        return " ".join(partes)

    @staticmethod
    def formatear_para_ejercicio(segundos: int) -> str:
        """Formato amigable: '4 segundos', '1 segundo'."""
        if segundos == 1:
            return "1 segundo"
        return f"{segundos} segundos"

    @staticmethod
    def formatear_minutos(segundos: int) -> str:
        """Formato en minutos: '2:30'."""
        minutos = segundos // 60
        segs = segundos % 60
        return f"{minutos}:{segs:02d}"

    @staticmethod
    def formatear_digital(segundos: int) -> str:
        """Formato digital: '01:30:45'."""
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segs = segundos % 60
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"

    @staticmethod
    def estimar_finalizacion(segundos_restantes: int) -> str:
        """Estima la hora de finalización: 'Terminará a las 14:35'."""
        final = datetime.now() + timedelta(seconds=segundos_restantes)
        return f"Terminará a las {final.strftime('%H:%M')}"

    # ═══════════════════════════════════════════════════════════
    # BARRAS DE PROGRESO
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def barra_progreso(actual: int, total: int, ancho: int = 20, 
                       lleno: str = "█", vacio: str = "░") -> str:
        """Genera una barra de progreso: '[████░░░░░░] 40%'."""
        if total == 0:
            return f"[{vacio * ancho}] 0%"
        porcentaje = min(100, int((actual / total) * 100))
        lleno_count = int((actual / total) * ancho)
        vacio_count = ancho - lleno_count
        return f"[{lleno * lleno_count}{vacio * vacio_count}] {porcentaje}%"

    @staticmethod
    def barra_respiracion(segundos: int, transcurrido: float, 
                          ancho: int = 15) -> str:
        """Barra animada para ejercicios de respiración."""
        if segundos == 0:
            return ""
        porcentaje = transcurrido / segundos
        lleno_count = int(porcentaje * ancho)
        vacio_count = ancho - lleno_count
        return f"[{'●' * lleno_count}{'○' * vacio_count}]"


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    """Suite de pruebas completa para Pausas v3.0"""
    print("\n" + "=" * 60)
    print("  🧪 TESTS: utilidades/pausas.py (v3.0 - Hiper-Evolución)")
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

    ps = Pausas()

    # ─── BÁSICOS ───
    t(isinstance(ps, Pausas), "Instancia creada")
    t(not ps._pausa_activa, "Sin pausa activa al inicio")
    t(ps._segundos_transcurridos == 0, "Cronómetro en 0")

    # ─── PAUSAS ───
    t(ps.pausa_corta is not None, "Método pausa_corta existe")
    t(ps.pausa_media is not None, "Método pausa_media existe")
    t(ps.pausa_larga is not None, "Método pausa_larga existe")
    t(ps.pausa_respiracion is not None, "Método pausa_respiracion existe")
    inicio = time.time()
    ps.pausa_personalizada(0.1)
    t(time.time() - inicio >= 0.09, "Pausa personalizada funciona")

    # ─── CUENTA REGRESIVA ───
    segs = []
    ps.cuenta_regresiva(3, callback_segundo=lambda s: segs.append(s))
    t(segs == [3, 2, 1], "Cuenta regresiva: [3, 2, 1]")

    fin = []
    ps.cuenta_regresiva(2, callback_fin=lambda: fin.append(True))
    t(len(fin) > 0, "Callback fin ejecutado")

    # Cuenta regresiva con progreso
    progresos = []
    ps.cuenta_regresiva(2, callback_progreso=lambda a, t: progresos.append((a, t)))
    t(len(progresos) == 2, "Callback progreso: 2 llamadas")
    t(progresos[-1] == (2, 2), "Progreso final (2, 2)")

    # Detener cuenta regresiva
    detenida = []
    def contar_largo(s):
        detenida.append(s)
        if s == 3:
            ps.detener_cuenta_regresiva()
    completada = ps.cuenta_regresiva(5, callback_segundo=contar_largo)
    t(detenida == [5, 4, 3], "Cuenta detenida en 3")
    t(not completada, "Retorna False al ser detenida")

    # Cuenta regresiva con mensajes
    mensajes_recibidos = []
    ps.cuenta_regresiva_con_mensajes(3, [(3, "Empieza"), (1, "Último")], 
                                      callback_mensaje=lambda m: mensajes_recibidos.append(m))
    t("Empieza" in mensajes_recibidos and "Último" in mensajes_recibidos, "Mensajes en segundos específicos")

    # ─── CRONÓMETRO ───
    ps2 = Pausas()
    ps2.iniciar_cronometro()
    time.sleep(0.5)
    t(ps2.obtener_tiempo_cronometro() >= 0, "Obtener tiempo sin detener")
    transcurrido = ps2.detener_cronometro()
    t(transcurrido >= 0, f"Cronómetro: {transcurrido}s")

    ps3 = Pausas()
    ps3.iniciar_cronometro()
    time.sleep(0.3)
    ps3.pausar_cronometro()
    pausado = ps3.obtener_tiempo_cronometro()
    time.sleep(0.3)
    t(ps3.obtener_tiempo_cronometro() == pausado, "Cronómetro pausado no avanza")
    ps3.reanudar_cronometro()
    time.sleep(0.3)
    t(ps3.detener_cronometro() > pausado, "Cronómetro reanudado avanza")

    ps4 = Pausas()
    ps4.iniciar_cronometro()
    time.sleep(0.3)
    ps4.reiniciar_cronometro()
    time.sleep(0.3)
    t(ps4.detener_cronometro() <= 1, "Cronómetro reiniciado")

    # ─── CICLO RESPIRACIÓN ───
    fases = []
    resultado = ps.ciclo_respiracion(4, 7, 8, 
                                     callback=lambda n, s: fases.append((n, s)))
    t(len(fases) == 3, "Ciclo: 3 fases")
    t(fases[0] == ("Inhala", 4), "Fase 1: Inhala 4s")
    t(fases[1] == ("Retén", 7), "Fase 2: Retén 7s")
    t(fases[2] == ("Exhala", 8), "Fase 3: Exhala 8s")
    t(resultado["completado"], "Ciclo completado")

    fases_sr = []
    ps.ciclo_respiracion(5, 0, 5, callback=lambda n, s: fases_sr.append(n))
    t("Retén" not in fases_sr, "Sin Retén cuando es 0")
    t(len(fases_sr) == 2, "2 fases con retención 0")

    # Ciclo completo (ejercicio)
    fases_comp = []
    ejercicio = {"pasos": [("Inhala", 1), ("Exhala", 1)], "ciclos": 2}
    ps.ciclo_completo(ejercicio, callback_fase=lambda t, s: fases_comp.append(t))
    t(len(fases_comp) == 4, "Ciclo completo: 2 ciclos x 2 pasos = 4 fases")

    # ─── FORMATEO ───
    t(ps.formatear_tiempo(0) == "0s", "0s = '0s'")
    t(ps.formatear_tiempo(45) == "45s", "45s = '45s'")
    t(ps.formatear_tiempo(90) == "1m 30s", "90s = '1m 30s'")
    t(ps.formatear_tiempo(3661) == "1h 1m 1s", "3661s = '1h 1m 1s'")
    t(ps.formatear_tiempo(-5) == "0s", "Negativo = '0s'")
    t(ps.formatear_para_ejercicio(1) == "1 segundo", "1 = '1 segundo'")
    t(ps.formatear_para_ejercicio(4) == "4 segundos", "4 = '4 segundos'")
    t(ps.formatear_minutos(150) == "2:30", "150s = '2:30'")
    t(ps.formatear_digital(3661) == "01:01:01", "3661s = '01:01:01'")
    t("Terminará" in ps.estimar_finalizacion(300), "Estimación de finalización")

    # ─── BARRAS ───
    barra = ps.barra_progreso(5, 10, ancho=10)
    t("50%" in barra and "█" in barra and "░" in barra, f"Barra progreso: {barra}")
    barra_resp = ps.barra_respiracion(8, 4)
    t("●" in barra_resp and "○" in barra_resp, f"Barra respiración: {barra_resp}")

    # ─── POMODORO (estado) ───
    t(not ps.estado_pomodoro()["activo"], "Pomodoro inactivo al inicio")

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Pausas v3.0 validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()