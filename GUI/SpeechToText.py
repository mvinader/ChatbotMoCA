from flask_socketio import emit
import os
from vosk import Model, KaldiRecognizer
import queue
import sounddevice
import json
from Configuracion import KALDI_FRECUENCIA_MUESTREO
from Configuracion import AUDIO_FRECUENCIA_MUESTREO
from Configuracion import AUDIO_TAMANYO_BLOQUE
from Configuracion import AUDIO_DATA_TYPE
from Configuracion import AUDIO_N_CANALES
from Configuracion import MAX_SILENCIOS_PERMITIDOS
from Configuracion import TIEMPO_POR_BLOQUE_MS
from GestorRasa import enviarMensajeAChatbot
from SpeechToTextTratamientoDatos import tratarDatosVoz

print("Cargando el modelo de reconocimiento de voz...")
rutaModeloVoz = os.environ["RUTA_MODELO_VOSK"]
if not os.path.exists(rutaModeloVoz):
    print ("Por favor, descargue el modelo desde https://alphacephei.com/vosk/models y descomprima en " + rutaModeloVoz)
    exit(1)
modelo = Model(rutaModeloVoz)
recognizer = KaldiRecognizer(modelo, KALDI_FRECUENCIA_MUESTREO)
print("Modelo de reconocimiento de voz cargado.")

cola = queue.Queue()
def callback(indata, status):
    if status:
        print(status)
    cola.put(bytes(indata))
    #cola.task_done()

# Configurar la entrada de audio usando constantes
stream = sounddevice.RawInputStream(
    samplerate=AUDIO_FRECUENCIA_MUESTREO,
    blocksize=AUDIO_TAMANYO_BLOQUE,
    dtype=AUDIO_DATA_TYPE,
    channels=AUDIO_N_CANALES,
    callback=callback
)

#def procesarAudio(cola):
def procesarAudio():
    continuarProcesado = True
    contadorSilencios = 0
    textoRespuestaBot = ""

    # Abrir el flujo de entrada
    with stream: #used to wrap the execution of a block with methods defined by a context manager
        try:
            #while True:
            while continuarProcesado == True:
                #stream.start()
                data = cola.get()
                #try:
               #      data = cola.get(timeout=1)
               #  except queue.Empty:
               #      print("No audio data available, esperando...")
               #      continue

                # Asegurarse de que los datos sean de tipo bytes
                if not isinstance(data, bytes):
                    data = bytes(data)  # Convertir a bytes si es necesario

                if len(data) > 0 and isinstance(data, bytes): # Asegurar que los datos sean de tipo byte
                    if recognizer.AcceptWaveform(data):
                        jsonDeserializado = json.loads(recognizer.Result()) # Obtener diccionario python
                        textoDeserialisedJSONData = jsonDeserializado.get('text', '').strip()

                        # Verificar si el JSON no está vacío y el campo 'text' contiene texto
                        if 'text' in jsonDeserializado and jsonDeserializado['text'].strip():
                            emit('debug', "Audio detectado: {}".format(textoDeserialisedJSONData))
                            print("Usted ha dicho: {}".format(textoDeserialisedJSONData))
                            contadorSilencios = 0 # Si se reconoce texto, reinicia el contador de silencio
                            if jsonDeserializado['text'] != "":
                                datosVozTratados = tratarDatosVoz(jsonDeserializado['text'])
                                print("Texto a procesar por chatbot: {}".format(datosVozTratados))
                                emit('gestionarMensajeUsuario', datosVozTratados)
                                textoRespuestaBot = enviarMensajeAChatbot(datosVozTratados) #Respuesta del bot
                                while not cola.empty():
                                    try:
                                        cola.get_nowait()
                                    except queue.Empty:
                                        break
                        else:                            
                            contadorSilencios += 1 # Incrementa el contador de bloques de silencio
                            print("Silencio detectado...")
                            emit('debug', "Silencio detectado...")
                            sounddevice.sleep(TIEMPO_POR_BLOQUE_MS) # espera solo cuando hay silencio
                    if contadorSilencios >= MAX_SILENCIOS_PERMITIDOS: # Detener la grabación si se excede el umbral de silencio
                        print("Detección de silencio prolongado. Terminando grabación...")
                        emit("Detección de silencio prolongado. Terminando grabación...")
                        continuarProcesado = False
                        stream.stop()
        except KeyboardInterrupt:
            stream.stop()
            print("Flujo de audio detenido.")
    return textoRespuestaBot
