import pyttsx3
from flask_socketio import emit
from Configuracion import PYTTSX3_VELOCIDAD_HABLA
from Configuracion import PYTTSX3_VOLUMEN
import wave

RESPUESTA_BOT_ARCHIVO = "respuestaBot.wav"

def reproducirTextoPorVoz(textoRespuestaBot):
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

    emit("reproducirAudio", textoRespuestaBot)
