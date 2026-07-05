import os
import json
import base64
from datetime import datetime
import requests

class GitHubSync:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN', '')
        self.repo_name = os.environ.get('GITHUB_REPO', 'sana-bitacora')
        self.owner = os.environ.get('GITHUB_OWNER', '')
        self.modo_local = not self.token
        
        if not self.modo_local:
            self.headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            self.api_base = 'https://api.github.com'
    
    def obtener_escuelas(self):
        if self.modo_local:
            return ['general', 'ejemplo']
        try:
            url = f"{self.api_base}/repos/{self.owner}/{self.repo_name}/contents/bitacoras"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                contents = response.json()
                escuelas = []
                for item in contents:
                    if item['type'] == 'dir':
                        escuelas.append(item['name'])
                return escuelas
        except:
            pass
        return ['general']
    
    def obtener_bitacora(self, escuela):
        if self.modo_local:
            archivo = f"bitacoras/{escuela}/bitacora.json"
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        try:
            path = f"bitacoras/{escuela}/bitacora.json"
            url = f"{self.api_base}/repos/{self.owner}/{self.repo_name}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                content = response.json()
                data = json.loads(base64.b64decode(content['content']).decode('utf-8'))
                return data
        except:
            pass
        return []
    
    def subir_bitacora(self, escuela, entrada):
        if self.modo_local:
            os.makedirs(f"bitacoras/{escuela}", exist_ok=True)
            archivo = f"bitacoras/{escuela}/bitacora.json"
            existente = self.obtener_bitacora(escuela)
            existente.append(entrada)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(existente, f, ensure_ascii=False, indent=2)
            return {'status': 'local', 'archivo': archivo}
        try:
            path = f"bitacoras/{escuela}/bitacora.json"
            existente = self.obtener_bitacora(escuela)
            existente.append(entrada)
            content = json.dumps(existente, ensure_ascii=False, indent=2)
            encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            url_get = f"{self.api_base}/repos/{self.owner}/{self.repo_name}/contents/{path}"
            get_response = requests.get(url_get, headers=self.headers)
            sha = None
            if get_response.status_code == 200:
                sha = get_response.json()['sha']
            
            url_put = f"{self.api_base}/repos/{self.owner}/{self.repo_name}/contents/{path}"
            data = {
                'message': f'Actualización bitácora {escuela} - {datetime.now().isoformat()}',
                'content': encoded,
                'branch': 'main'
            }
            if sha:
                data['sha'] = sha
            
            response = requests.put(url_put, headers=self.headers, json=data)
            if response.status_code in [200, 201]:
                return {'status': 'success', 'escuela': escuela, 'entradas': len(existente)}
        except Exception as e:
            return {'status': 'error', 'mensaje': str(e)}
