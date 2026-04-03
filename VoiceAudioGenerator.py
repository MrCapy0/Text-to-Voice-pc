from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
import AppConfig as config
import os

AUDIO_PATH = "./exports/"
AUDIO_NAME_BASE = "audio_"

def write_audio_file_from_text(text, voice, on_completed=None, on_fail=None):
    if not os.path.exists(AUDIO_PATH):
        os.makedirs(AUDIO_PATH)

    try:
        authenticator = IAMAuthenticator(config.config['api'])
        text_to_speech = TextToSpeechV1(authenticator=authenticator)
        text_to_speech.set_service_url(config.config['url'])

        count = len([f for f in os.listdir(AUDIO_PATH) if os.path.isfile(os.path.join(AUDIO_PATH, f))])
        file_path = os.path.join(AUDIO_PATH, f"{AUDIO_NAME_BASE}{count}.mp3")

        # Chamada da API
        response = text_to_speech.synthesize(
            text=text,
            voice=voice,
            accept='audio/mp3'
        ).get_result()

        with open(file_path, 'wb') as audio_file:
            audio_file.write(response.content)
            
        if on_completed:
            on_completed()

    except ApiException as ex:
        if on_fail:
            on_fail(ex.code, ex.message)
    except Exception as e:
        if on_fail:
            on_fail(500, str(e))