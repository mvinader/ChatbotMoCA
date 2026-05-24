import pyttsx3
from Configuracion import PYTTSX3_VELOCIDAD_HABLA
from Configuracion import PYTTSX3_VOLUMEN

def crearTTSEngineInstance():
    print("Cargando la instancia de generación de voz...")
    ttsEngineInstance = pyttsx3.init()
    # Configurar propiedades de la voz
    ttsEngineInstance.setProperty('rate', PYTTSX3_VELOCIDAD_HABLA)     
    ttsEngineInstance.setProperty('volume', PYTTSX3_VOLUMEN)
    # Configurar el idioma y la voz (opcional)
    voices = ttsEngineInstance.getProperty('voices')
    for voice in voices:
        if 'spanish' in voice.languages:
            ttsEngineInstance.setProperty('voice', voice.id)
            break
    if ttsEngineInstance._inLoop:
        ttsEngineInstance.endLoop()
    return ttsEngineInstance
