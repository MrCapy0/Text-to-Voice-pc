import AppConfig as config
import os
import requests
import re

def write_audio_file_from_text(text, voice, on_completed=None, on_fail=None):
    service_url = config.config['url']
    api_key = config.config['api']

    if not api_key or not service_url:
        if on_fail: on_fail(401, "IBM credentals not configured.")
        return
    
    # Export dir.
    base_dir = os.path.join(os.getcwd(), 'exports')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    # Split text by empty lines.
    phrases = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

    if not phrases:
        if on_fail: on_fail(0, "Add a text to process.")
        return

    url = f"{service_url.strip().rstrip('/')}/v1/synthesize"

    try:
        for index, phrase in enumerate(phrases, start=1):
            query_params = {
                'voice': voice,
                'text': phrase
            }

            response = requests.get(
                url, 
                params=query_params,
                headers={'Accept': 'audio/mp3'},
                auth=('apikey', api_key)
            )

            if not response.ok:
                if on_fail: on_fail(response.status_code, response.text)
                return

            clean_name = re.sub(r'[^a-zA-Z0-9à-úÀ-Ú\s]', '', phrase).strip()
            safe_name = clean_name[:50] if len(clean_name) > 50 else clean_name
            
            # Add an index on file name.
            file_name = f"{index}-{safe_name.replace(' ', '_')}.mp3"
            file_path = os.path.join(base_dir, file_name)

            with open(file_path, 'wb') as audio_file:
                audio_file.write(response.content)

        if on_completed:
            on_completed()

    except requests.exceptions.RequestException as e:
        if on_fail: on_fail(11001, f"Connection error: {str(e)}")