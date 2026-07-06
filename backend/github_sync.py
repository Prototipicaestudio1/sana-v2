import os, json, base64
from datetime import datetime
import requests

class GitHubSync:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN', '')
        self.repo_name = os.environ.get('GITHUB_REPO', 'sana-v2')
        self.owner = os.environ.get('GITHUB_OWNER', '')
        self.modo_local = not self.token
        self.data_path = "datos/sana_data.json"

        if not self.modo_local:
            self.headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            self.api_base = 'https://api.github.com'

    def obtener_datos(self):
        if self.modo_local:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            return {}
        try:
            url = f"{self.api_base}/repos/{self.owner}/{self.repo_name}/contents/{self.data_path}"
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                content = r.json()
                return json.loads(base64.b64decode(content['content']).decode('utf-8'))
        except:
            pass
        return {}

    def guardar_datos(self, datos):
        if self.modo_local:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
        try:
            content = json.dumps(datos, indent=2, ensure_ascii=False)
            encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            url = f"{self.api_base}/repos/{self.owner}/{self.repo_name}/contents/{self.data_path}"
            r = requests.get(url, headers=self.headers)
            sha = r.json().get('sha') if r.status_code == 200 else None
            body = {
                'message': f'💾 SANA - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'content': encoded,
                'branch': 'main'
            }
            if sha: body['sha'] = sha
            r = requests.put(url, headers=self.headers, json=body)
            return r.status_code in [200, 201]
        except Exception as e:
            print(f"⚠️ Error guardando: {e}")
        return False

    def sync_all(self, escuelas_obj, usuarios_obj, bitacora_obj, regularizacion_obj, organizador_obj, alertas_obj):
        """Sincroniza TODOS los datos a GitHub"""
        datos = {
            "escuelas": escuelas_obj.escuelas,
            "usuarios": usuarios_obj.usuarios,
            "bitacoras": bitacora_obj.entradas,
            "regularizacion": regularizacion_obj.material,
            "planes": organizador_obj.planes,
            "tareas": organizador_obj.tareas,
            "red_apoyo": alertas_obj.red_apoyo,
            "fecha": datetime.now().isoformat()
        }
        return self.guardar_datos(datos)

    def load_all(self, escuelas_obj, usuarios_obj, bitacora_obj, regularizacion_obj, organizador_obj, alertas_obj):
        """Carga TODOS los datos desde GitHub"""
        datos = self.obtener_datos()
        if datos:
            if "escuelas" in datos:
                escuelas_obj.escuelas = datos["escuelas"]
                escuelas_obj._guardar()
            if "usuarios" in datos:
                usuarios_obj.usuarios = datos["usuarios"]
                usuarios_obj._guardar()
            if "bitacoras" in datos:
                bitacora_obj.entradas = datos["bitacoras"]
                bitacora_obj.guardar()
            if "regularizacion" in datos:
                regularizacion_obj.material = datos["regularizacion"]
                regularizacion_obj._guardar()
            if "planes" in datos:
                organizador_obj.planes = datos["planes"]
            if "tareas" in datos:
                organizador_obj.tareas = datos["tareas"]
            if "red_apoyo" in datos:
                alertas_obj.red_apoyo = datos["red_apoyo"]
                alertas_obj._guardar()
            organizador_obj._guardar()
            return True
        return False
