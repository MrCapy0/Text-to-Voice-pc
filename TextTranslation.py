from googletrans import Translator 

def translate_text(text, from_lang='auto', to_lang='en', on_fail=None):
    try:
        if not text.strip(): return ""
        
        translator = Translator(service_urls=['translate.googleapis.com'])
        
        result = translator.translate(text, dest=to_lang, src=from_lang)
        return result.text
    except Exception as e:
        if on_fail is not None:
            on_fail(e)
        print(f"Erro na tradução: {e}")
    return ""