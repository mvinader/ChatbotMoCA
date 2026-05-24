# Basado en la API de Rasa: https://legacy-docs-oss.rasa.com/docs/rasa/pages/http-api/
import requests
from flask_socketio import emit
from Configuracion import RASA_TRACKER
from Configuracion import RASA_REST_WEBHOOK
from Configuracion import EXPLICACIONES_OCULTAR
from TextToSpeech import crearTTSEngineInstance

def obtenerJsonTrackerRasa():
    data = None
    try:
        rasaTrackerRespuestas = requests.get(RASA_TRACKER)
        rasaTrackerRespuestas.raise_for_status()
        try:
            data = rasaTrackerRespuestas.json()
        except:
            print("La respuesta del tracker no es un JSON válido.")
            print("Respuesta recibida:", rasaTrackerRespuestas.text)
            raise
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor Rasa.")
        emit('debug', "No se pudo conectar con el servidor Rasa.")
    except requests.exceptions.Timeout:
        print("El servidor Rasa tardó demasiado en responder.")
        emit('debug', "El servidor Rasa tardó demasiado en responder.")
    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP {rasaTrackerRespuestas.status_code}: {error}")
        emit('debug', f"Error HTTP {rasaTrackerRespuestas.status_code}: {error}")
    except Exception as error:
        print("Error al obtener el tracker:", type(error).__name__, str(error))
        emit('debug', "Error al obtener el tracker:", type(error).__name__, str(error))
    return data

def enviarMensajeAChatbot(mensajeUsuario):
    respuestasBotJSON = ""
    try:
        respuestasBotJSON = requests.post(RASA_REST_WEBHOOK, json={"message": mensajeUsuario})
    except requests.exceptions.RequestException as error:
        print(f"Error al conectar con el servidor: {error}")
        emit(f"Error al conectar con el servidor: {error}")
        return ""
    
    textoRespuestaBot = ""
    for respuestaChatbotJSON in respuestasBotJSON.json(): # Por si hay varias respuestas
        if respuestaChatbotJSON.get('text', '').strip():
            textoRespuestaBot = respuestaChatbotJSON['text']
            print(f"El chatbot dice: {textoRespuestaBot}")

            if textoRespuestaBot not in EXPLICACIONES_OCULTAR:
                emit('gestionarMensajeChatbot', textoRespuestaBot)

            ttsEngineInstance = crearTTSEngineInstance()
            ttsEngineInstance.say(textoRespuestaBot) # Reproducir el texto
            ttsEngineInstance.runAndWait()
        elif respuestaChatbotJSON.get('image', '').strip():
            emit('gestionarImagenChatbot', respuestaChatbotJSON['image'])
    return respuestasBotJSON