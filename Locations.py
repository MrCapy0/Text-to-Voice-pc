class Location():
    def __init__(self, name, google_translation_ref, ibm_voice_location):
        self.name = name
        self.google_translation_ref = google_translation_ref
        self.ibm_voice_location = ibm_voice_location

class Voice():
    def __init__(self, name, ibm_voice_ref):
        self.name = name
        self.ibm_voice_ref = ibm_voice_ref

locations = [
    Location(name="English", 
            google_translation_ref="en", 
            ibm_voice_location=[
                Voice(name="Australian Heidi", ibm_voice_ref="en-AU_HeidiNatural"),
                Voice(name="Australian Jack", ibm_voice_ref="en-AU_JackNatural"),
                Voice(name="Canadian Hannah", ibm_voice_ref="en-CA_HannahNatural"),
                Voice(name="British Chloe", ibm_voice_ref="en-GB_ChloeNatural"),
                Voice(name="EUA Ellie", ibm_voice_ref="en-US_EllieNatural"),
                Voice(name="EUA Emma", ibm_voice_ref="en-US_EmmaNatural"),
                Voice(name="EUA Ethan", ibm_voice_ref="en-US_EthanNatural"),
                Voice(name="EUA Jackson", ibm_voice_ref="en-US_JacksonNatural"),
                Voice(name="EUA Victoria", ibm_voice_ref="en-US_VictoriaNatural")
            ]),

    Location(name="Portuguese", 
            google_translation_ref="pt", 
            ibm_voice_location=[
                Voice(name="Brasil Lucas", ibm_voice_ref="pt-BR_LucasNatural"),
                Voice(name="Brasil Camila", ibm_voice_ref="pt-BR_CamilaNatural")
            ]),

    Location(name="Spanish", 
            google_translation_ref="es", 
            ibm_voice_location=[
                Voice(name="Latino Alejandro", ibm_voice_ref="es-LA_AlejandroNatural"),
                Voice(name="Latino Daniela", ibm_voice_ref="es-LA_DanielaNatural")
            ]),
]

def get_language_by_name(name):
    for l in locations:
        # Removido o índice [0] pois agora 'name' é string pura
        if l.name == name:
            return l
    return None

def get_all_locations_names():
    return [l.name for l in locations]

def get_all_voices_name_by_language_name(language):
    for l in locations:
        if l.name == language:
            return [v.name for v in l.ibm_voice_location]
    return []

def get_ibm_voice_by_voice_name(voice_name):
    for loc in locations:
        for v in loc.ibm_voice_location:
            if v.name == voice_name:
                return v.ibm_voice_ref
    return None