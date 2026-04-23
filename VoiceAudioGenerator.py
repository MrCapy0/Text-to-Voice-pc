import AppConfig as config
import os
import requests
import re

def write_audio_file_from_text(text, voice, on_completed=None, on_fail=None):
    
    service_url = config.config['url']
    api_key = config.config['api']

    # 1. Verificação de Credenciais
    if not api_key or not service_url:
        raise Exception('IBM Watson credentials not configured.')
    
    # 2. Configuração de Diretórios (Equivalente ao FileSystem do JS)
    # No Linux/Windows usamos caminhos padrão do OS
    base_dir = os.path.join(os.getcwd(), 'Text to Speech Project', 'exports')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    # 3. Montagem da URL e Parâmetros
    # O requests aceita um dicionário 'params' que cuida do encodeURIComponent automaticamente
    url = f"{service_url.strip().rstrip('/')}/v1/synthesize"
    query_params = {
        'voice': voice,
        'text': text
    }

    # 4. Execução do Fetch (GET com Basic Auth)
    try:
        # No Python, ('apikey', key) no parâmetro auth faz o encodeBase64 automaticamente
        response = requests.get(
            url, 
            params=query_params,
            headers={'Accept': 'audio/mp3'},
            auth=('apikey', api_key)
        )

        # 5. Tratamento de Erro
        if not response.ok:
            raise Exception(f"IBM TTS error ({response.status_code}): {response.text}")

        # 6. Processamento do Nome do Arquivo (Sanitize)
        safe_name = re.sub(r'[^a-z0-9]', '_', "audio", flags=re.I).lower()
        file_name = f"{safe_name}.mp3"
        file_path = os.path.join(base_dir, file_name)

        # 7. Escrita do Arquivo (Equivalente ao uint8Array/write)
        with open(file_path, 'wb') as audio_file:
            audio_file.write(response.content)

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição: {e}")