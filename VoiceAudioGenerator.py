from ibm_watson import TextToSpeechV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import AppConfig as config
import os

AUDIO_PATH = "./exports/"
AUDIO_NAME_BASE = "audio "

def write_audio_file_from_text(text, voice, on_completed=None, on_fail=None):
    
    def connect_to_api_service():
        # LOG de depuração das credenciais (remova o print da API Key após testar por segurança)
        print(f"--- Tentando conectar ao IBM Watson ---")
        print(f"URL configurada: {config.config['url']}")
        print(f"API Key configurada: {config.config['api'][:5]}*** (exibindo apenas o início)")

        try:
            auth = IAMAuthenticator(config.config['api'])
            service_text_to_speech = TextToSpeechV1(authenticator=auth)
            service_text_to_speech.set_service_url(config.config['url'])
            return service_text_to_speech
        except Exception as e:
            print(f"ERRO NA CONFIGURAÇÃO DO AUTENTICADOR: {e}")
            raise e

    def file_name():
        if not os.path.isdir(AUDIO_PATH):
            os.makedirs(AUDIO_PATH)
        
        res = [path for path in os.listdir(AUDIO_PATH) if os.path.isfile(os.path.join(AUDIO_PATH, path))]
        return os.path.join(AUDIO_PATH, f"{AUDIO_NAME_BASE}{len(res)}")

    try:
        text_to_speech = connect_to_api_service()
        
        print(f"Solicitando síntese para voz: {voice}...")
        
        # O método synthesize retorna um objeto DetailedResponse
        response = text_to_speech.synthesize(
            text=text, 
            voice='en-US_AllisonV2Voice', 
            accept='audio/mp3'
        )
        
        # O resultado real está no get_result()
        audio_result = response.get_result()

        if audio_result is not None:
            f_name = file_name()
            with open(f_name + ".mp3", 'wb') as file:
                file.write(audio_result.content)
            
            print(f"Áudio gerado com sucesso: {f_name}.mp3")
            if on_completed is not None:
                on_completed()

    except ApiException as e:
        # LOGS específicos da API do Watson (Erro 401, 404, 400, etc)
        print("\n--- ERRO DE API WATSON ---")
        print(f"Status Code: {e.code}")
        print(f"Mensagem: {e.message}")
        if on_fail is not None:
            on_fail(e.code, e.message)
            
    except Exception as e:
        # LOGS de conexão (DNS, Internet fora, URL mal formatada)
        print("\n--- ERRO GENÉRICO/CONEXÃO ---")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Detalhes: {e}")
        if on_fail is not None:
            on_fail(11001, f"Connection Error: {str(e)}")