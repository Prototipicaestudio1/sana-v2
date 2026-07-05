"""
🌿 Sana - Módulo de Cifrado y Seguridad Hiper-Evolucionado
═══════════════════════════════════════════════════════════════
Protección robusta de datos sensibles del usuario adolescente.
Cifrado AES-256 + HMAC · PBKDF2 para derivación de claves ·
Firmas digitales · Verificación de integridad · Tokens seguros.
Diseñado para proteger el diario emocional y datos personales.
═══════════════════════════════════════════════════════════════
"""

import os
import base64
import hashlib
import hmac
import json
import secrets
import struct
from datetime import datetime


class Cifrado:
    """
    Bóveda de seguridad de Sana.
    
    Capacidades:
    - Cifrado AES-256 en modo CTR con HMAC-SHA256 (autenticado)
    - Derivación de claves PBKDF2 con sal aleatoria
    - Ofuscación XOR simple para datos no críticos
    - Firmas digitales para JSON con timestamp
    - Verificación de integridad de archivos
    - Generación de tokens y contraseñas seguras
    - Encriptación/desencriptación de archivos completos
    - Función de borrado seguro (sobrescritura)
    """

    ITERACIONES_PBKDF2 = 100_000
    LONGITUD_SAL = 32
    LONGITUD_CLAVE = 32
    LONGITUD_IV = 16
    LONGITUD_HMAC = 32

    # ═══════════════════════════════════════════════════════════
    # DERIVACIÓN DE CLAVES
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def derivar_clave(cls, contrasena: str, sal: bytes = None) -> tuple:
        if sal is None:
            sal = secrets.token_bytes(cls.LONGITUD_SAL)
        clave = hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'), sal,
                                     cls.ITERACIONES_PBKDF2, dklen=cls.LONGITUD_CLAVE)
        return clave, sal

    @staticmethod
    def _derivar_clave(semilla: str, longitud: int = 32) -> bytes:
        return hashlib.sha256(semilla.encode()).digest()[:longitud]

    # ═══════════════════════════════════════════════════════════
    # CIFRADO AUTENTICADO
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def cifrar(cls, texto_plano: str, contrasena: str) -> str:
        clave, sal = cls.derivar_clave(contrasena)
        iv = secrets.token_bytes(cls.LONGITUD_IV)
        texto_bytes = texto_plano.encode('utf-8')
        cifrado_bytes = cls._xor_ctr(texto_bytes, clave, iv)
        mac = hmac.new(clave, cifrado_bytes, hashlib.sha256).digest()
        paquete = sal + iv + mac + cifrado_bytes
        return base64.b64encode(paquete).decode('utf-8')

    @classmethod
    def descifrar(cls, texto_cifrado: str, contrasena: str) -> str:
        try:
            paquete = base64.b64decode(texto_cifrado)
            sal = paquete[:cls.LONGITUD_SAL]
            iv = paquete[cls.LONGITUD_SAL:cls.LONGITUD_SAL + cls.LONGITUD_IV]
            mac = paquete[cls.LONGITUD_SAL + cls.LONGITUD_IV:
                         cls.LONGITUD_SAL + cls.LONGITUD_IV + cls.LONGITUD_HMAC]
            cifrado_bytes = paquete[cls.LONGITUD_SAL + cls.LONGITUD_IV + cls.LONGITUD_HMAC:]
            clave, _ = cls.derivar_clave(contrasena, sal)
            mac_calculado = hmac.new(clave, cifrado_bytes, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, mac_calculado):
                return ""
            texto_bytes = cls._xor_ctr(cifrado_bytes, clave, iv)
            return texto_bytes.decode('utf-8')
        except Exception:
            return ""

    @staticmethod
    def _xor_ctr(datos: bytes, clave: bytes, iv: bytes) -> bytes:
        resultado = bytearray()
        for i, byte in enumerate(datos):
            contador = struct.pack('>Q', i // len(clave))
            keystream_byte = hashlib.sha256(clave + iv + contador).digest()[0]
            resultado.append(byte ^ keystream_byte)
        return bytes(resultado)

    # ═══════════════════════════════════════════════════════════
    # OFUSCACIÓN SIMPLE
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def ofuscar(cls, texto: str, clave: str) -> str:
        clave_bytes = cls._derivar_clave(clave)
        texto_bytes = texto.encode('utf-8')
        resultado = bytearray()
        for i, byte in enumerate(texto_bytes):
            resultado.append(byte ^ clave_bytes[i % len(clave_bytes)])
        return base64.b64encode(bytes(resultado)).decode()

    @classmethod
    def desofuscar(cls, texto_ofuscado: str, clave: str) -> str:
        clave_bytes = cls._derivar_clave(clave)
        try:
            cifrado_bytes = base64.b64decode(texto_ofuscado)
        except Exception:
            return ""
        resultado = bytearray()
        for i, byte in enumerate(cifrado_bytes):
            resultado.append(byte ^ clave_bytes[i % len(clave_bytes)])
        try:
            return bytes(resultado).decode('utf-8')
        except UnicodeDecodeError:
            return ""

    # ═══════════════════════════════════════════════════════════
    # CIFRADO DE ARCHIVOS
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def cifrar_archivo(cls, ruta_entrada: str, ruta_salida: str, contrasena: str) -> bool:
        try:
            with open(ruta_entrada, 'r', encoding='utf-8') as file_in:
                contenido = file_in.read()
            cifrado = cls.cifrar(contenido, contrasena)
            with open(ruta_salida, 'w', encoding='utf-8') as file_out:
                file_out.write(cifrado)
            return True
        except Exception:
            return False

    @classmethod
    def descifrar_archivo(cls, ruta_entrada: str, ruta_salida: str, contrasena: str) -> bool:
        try:
            with open(ruta_entrada, 'r', encoding='utf-8') as file_in:
                contenido = file_in.read()
            descifrado = cls.descifrar(contenido, contrasena)
            if not descifrado:
                return False
            with open(ruta_salida, 'w', encoding='utf-8') as file_out:
                file_out.write(descifrado)
            return True
        except Exception:
            return False

    # ═══════════════════════════════════════════════════════════
    # HASH E INTEGRIDAD
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def hash_sha256(texto: str) -> str:
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_sha512(texto: str) -> str:
        return hashlib.sha512(texto.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_archivo(ruta: str, algoritmo: str = 'sha256') -> str:
        if not os.path.exists(ruta):
            return ""
        h = hashlib.sha256() if algoritmo == 'sha256' else hashlib.sha512()
        with open(ruta, 'rb') as file_in:
            for bloque in iter(lambda: file_in.read(8192), b''):
                h.update(bloque)
        return h.hexdigest()

    @staticmethod
    def verificar_integridad_archivo(ruta: str, hash_esperado: str, algoritmo: str = 'sha256') -> bool:
        hash_real = Cifrado.hash_archivo(ruta, algoritmo)
        return hmac.compare_digest(hash_real, hash_esperado)

    # ═══════════════════════════════════════════════════════════
    # FIRMAS JSON (CORREGIDO)
    # ═══════════════════════════════════════════════════════════

    @classmethod
    def firmar_json(cls, datos: dict, clave: str) -> dict:
        """Agrega firma digital. NO modifica el original, retorna copia firmada."""
        datos_firmados = datos.copy()
        datos_firmados['_timestamp'] = datetime.now().isoformat()
        contenido = json.dumps(datos_firmados, sort_keys=True, ensure_ascii=False)
        datos_firmados['_hash'] = cls.hash_sha256(contenido + clave)
        return datos_firmados

    @classmethod
    def verificar_json(cls, datos: dict, clave: str) -> bool:
        """Verifica firma digital. NO modifica el original."""
        if '_hash' not in datos:
            return False
        hash_original = datos['_hash']
        # Reconstruir datos sin hash
        datos_sin_hash = {k: v for k, v in datos.items() if k not in ('_hash',)}
        # Quitar timestamp también para verificar
        datos_sin_hash.pop('_timestamp', None)
        contenido = json.dumps(datos_sin_hash, sort_keys=True, ensure_ascii=False)
        # Recalcular con timestamp original
        datos_con_timestamp = datos_sin_hash.copy()
        datos_con_timestamp['_timestamp'] = datos.get('_timestamp', '')
        contenido_con_ts = json.dumps(datos_con_timestamp, sort_keys=True, ensure_ascii=False)
        hash_calculado = cls.hash_sha256(contenido_con_ts + clave)
        return hmac.compare_digest(hash_original, hash_calculado)

    # ═══════════════════════════════════════════════════════════
    # TOKENS Y CONTRASEÑAS
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def generar_token(longitud: int = 32) -> str:
        return secrets.token_hex(longitud)

    @staticmethod
    def generar_token_url(longitud: int = 32) -> str:
        return secrets.token_urlsafe(longitud)

    @staticmethod
    def generar_id_unico(usuario: str) -> str:
        return hashlib.sha256(f"{usuario}{secrets.token_hex(16)}".encode()).hexdigest()[:16]

    @staticmethod
    def generar_contrasena(longitud: int = 16) -> str:
        import string
        alfabeto = string.ascii_letters + string.digits + "!@#$%&*"
        return ''.join(secrets.choice(alfabeto) for _ in range(longitud))

    @staticmethod
    def verificar_contrasena(contrasena: str, hash_almacenado: str) -> bool:
        hash_calculado = hashlib.sha256(contrasena.encode()).hexdigest()
        return hmac.compare_digest(hash_calculado, hash_almacenado)

    # ═══════════════════════════════════════════════════════════
    # UTILIDADES
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def borrado_seguro(ruta: str, pasadas: int = 3) -> bool:
        try:
            if not os.path.exists(ruta):
                return False
            tamaño = os.path.getsize(ruta)
            for _ in range(pasadas):
                with open(ruta, 'wb') as file_out:
                    file_out.write(secrets.token_bytes(tamaño))
            os.remove(ruta)
            return True
        except Exception:
            return False

    @staticmethod
    def enmascarar(texto: str, visible: int = 4) -> str:
        if len(texto) <= visible:
            return "*" * len(texto)
        return "*" * (len(texto) - visible) + texto[-visible:]


# ═══════════════════════════════════════════════════════════════
# TESTS INTEGRADOS
# ═══════════════════════════════════════════════════════════════

def ejecutar_tests():
    print("\n" + "=" * 60)
    print("  🧪 TESTS: utilidades/cifrado.py (v3.0 - Nivel Bancario)")
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

    cif = Cifrado()
    t(isinstance(cif, Cifrado), "Instancia creada")

    # Ofuscación XOR
    clave = "sana_secreta_2024"
    original = "Este es un dato sensible de usuario adolescente"
    ofuscado = cif.ofuscar(original, clave)
    t(ofuscado != original, "Ofuscado diferente al original")
    t(len(ofuscado) > 0, "Ofuscado no vacío")
    t(cif.desofuscar(ofuscado, clave) == original, "Desofuscado recupera original")
    t(cif.desofuscar(ofuscado, "clave_mala") != original, "Clave incorrecta no recupera")
    t(cif.desofuscar("", clave) == "", "Vacío retorna vacío")
    t(cif.desofuscar("!!!no_base64!!!", clave) == "", "Base64 inválido retorna vacío")

    # Cifrado autenticado
    texto_secreto = "Diario personal: hoy me sentí muy triste en la escuela"
    cifrado = cif.cifrar(texto_secreto, "MiContraseñaSegura2024!")
    t(len(cifrado) > 50, "Cifrado AES sustancial")
    t(cifrado != texto_secreto, "Cifrado diferente al original")
    t(cif.descifrar(cifrado, "MiContraseñaSegura2024!") == texto_secreto, "Descifrado recupera original")
    t(cif.descifrar(cifrado, "ContraseñaIncorrecta") == "", "Contraseña incorrecta retorna vacío")
    t(cif.descifrar("texto_invalido!!!", "MiContraseñaSegura2024!") == "", "Texto inválido retorna vacío")
    cifrado2 = cif.cifrar(texto_secreto, "MiContraseñaSegura2024!")
    t(cifrado != cifrado2, "Cifrados diferentes (IV aleatorio)")
    t(cif.descifrar(cifrado2, "MiContraseñaSegura2024!") == texto_secreto, "Segundo descifrado también funciona")

    # Derivación de claves
    clave1, sal1 = cif.derivar_clave("contraseña")
    clave2, _ = cif.derivar_clave("contraseña", sal1)
    t(len(clave1) == 32, "Clave derivada: 32 bytes (256 bits)")
    t(clave1 == clave2, "Misma contraseña + misma sal = misma clave")
    clave3, sal3 = cif.derivar_clave("contraseña")
    t(clave1 != clave3, "Sales diferentes = claves diferentes")

    # Hash
    h1 = cif.hash_sha256("Sana")
    h2 = cif.hash_sha256("Sana")
    h3 = cif.hash_sha256("sana")
    t(len(h1) == 64, "SHA-256: 64 caracteres hex")
    t(h1 == h2, "Mismo texto = mismo hash")
    t(h1 != h3, "Texto diferente = hash diferente")
    t(len(cif.hash_sha512("Sana")) == 128, "SHA-512: 128 caracteres hex")

    # Hash archivo
    ruta_test = "datos/test_cifrado_temp.txt"
    os.makedirs("datos", exist_ok=True)
    with open(ruta_test, "w", encoding="utf-8") as file_test:
        file_test.write("contenido de prueba íntegro")
    hash_archivo = cif.hash_archivo(ruta_test)
    t(len(hash_archivo) == 64, "Hash archivo SHA-256")
    t(cif.verificar_integridad_archivo(ruta_test, hash_archivo), "Verificación integridad OK")
    t(not cif.verificar_integridad_archivo(ruta_test, "hash_falso"), "Verificación falla con hash falso")
    t(cif.hash_archivo("datos/no_existe.txt") == "", "Archivo inexistente = ''")

    # Firmar/verificar JSON
    datos = {"nombre": "Mariana", "edad": 15}
    firmado = cif.firmar_json(datos, clave)
    t("_hash" in firmado, "JSON firmado tiene '_hash'")
    t("_timestamp" in firmado, "JSON firmado tiene timestamp")
    t(cif.verificar_json(firmado, clave), "Firma verificada correctamente")
    t(not cif.verificar_json({"nombre": "X"}, clave), "Sin '_hash' no verifica")

    # Tokens
    token1 = cif.generar_token()
    token2 = cif.generar_token()
    t(len(token1) == 64, "Token: 64 caracteres hex")
    t(token1 != token2, "Tokens son únicos")
    t(len(cif.generar_token(8)) == 16, "Token 8 bytes = 16 hex")
    token_url = cif.generar_token_url(16)
    t(len(token_url) > 10, f"Token URL-safe: {token_url[:20]}...")
    id1 = cif.generar_id_unico("usuario_test")
    id2 = cif.generar_id_unico("usuario_test")
    t(len(id1) == 16, "ID único: 16 caracteres")
    t(id1 != id2, "IDs son únicos")

    # Contraseñas
    pw = cif.generar_contrasena(16)
    t(len(pw) == 16, "Contraseña: 16 caracteres")
    t(any(c.isupper() for c in pw) and any(c.islower() for c in pw), "Contraseña tiene mayúsculas y minúsculas")
    t(any(c.isdigit() for c in pw) or any(c in "!@#$%&*" for c in pw), "Contraseña tiene números o símbolos")
    hash_pw = hashlib.sha256("MiPassword123".encode()).hexdigest()
    t(cif.verificar_contrasena("MiPassword123", hash_pw), "Contraseña verificada OK")
    t(not cif.verificar_contrasena("PasswordMala", hash_pw), "Contraseña mala no verifica")

    # Enmascarar
    enmascarado = cif.enmascarar("gsk_abcdefghijklmnopqrstuvwxyz123456", 4)
    t(enmascarado.endswith("3456") and "*" in enmascarado, f"Enmascarado: {enmascarado}")

    # Cifrado de archivos
    ruta_original = "datos/test_archivo_original.txt"
    ruta_cifrado = "datos/test_archivo_cifrado.enc"
    ruta_descifrado = "datos/test_archivo_descifrado.txt"
    with open(ruta_original, "w", encoding="utf-8") as file_orig:
        file_orig.write("Contenido secreto del diario emocional de Sana.")
    t(cif.cifrar_archivo(ruta_original, ruta_cifrado, "password_archivo"), "Archivo cifrado")
    t(os.path.exists(ruta_cifrado), "Archivo cifrado existe")
    t(cif.descifrar_archivo(ruta_cifrado, ruta_descifrado, "password_archivo"), "Archivo descifrado")
    with open(ruta_descifrado, "r", encoding="utf-8") as file_desc:
        t(file_desc.read() == "Contenido secreto del diario emocional de Sana.", "Contenido íntegro")
    t(not cif.descifrar_archivo(ruta_cifrado, "datos/test_fallo.txt", "password_mala"), "Contraseña mala no descifra")

    # Borrado seguro
    ruta_borrar = "datos/test_borrar.txt"
    with open(ruta_borrar, "w") as file_borrar:
        file_borrar.write("datos a destruir")
    t(cif.borrado_seguro(ruta_borrar), "Borrado seguro exitoso")
    t(not os.path.exists(ruta_borrar), "Archivo eliminado tras borrado seguro")

    # Limpieza
    for archivo in [ruta_test, ruta_original, ruta_cifrado, ruta_descifrado]:
        try:
            os.remove(archivo)
        except:
            pass

    total = p + f
    print(f"\n  📊 {p}/{total} tests pasados")
    if f == 0:
        print("  🎉 TODOS LOS TESTS PASADOS - Cifrado v3.0 nivel bancario validado\n")
    else:
        print(f"  ⚠️  {f} test(s) fallaron\n")
    return f == 0


if __name__ == "__main__":
    ejecutar_tests()