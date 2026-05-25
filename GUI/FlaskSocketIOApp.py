from flask import Flask, render_template, request # importar clase Flask desde package flask
from flask_socketio import SocketIO, emit
import requests
from Configuracion import FLASK_CLAVE
from Configuracion import RASA_TRACKER
from TextToSpeech import reproducirTextoPorVoz
from SpeechToText import procesarAudio
from SpeechToText import stream
from GestorRasa import obtenerJsonTrackerRasa
from GestorRasa import enviarMensajeAChatbot

print("Cargando la app de Flask...")
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_CLAVE

print("Cargando SocketIO...")
#socketio = SocketIO(app) # para pruebas en local
socketio = SocketIO(app, cors_allowed_origins="*") # si el navegador carga el frontend desde un origen distinto al backend, el servidor debe permitir esas conexiones

@app.route('/')
def index():
    return render_template('index.html')

usuariosActivos = set()
@socketio.on('connect')
def reaccionarAConexion():
    userId = request.args.get("user_id")
    if userId in usuariosActivos:
        print("Reconexión de:", userId)
        # En el cliente escuchas 'socket.on("nombre_evento", ...)'
        emit('debug', {'data': 'Reconexión', 'userId': userId}) # sirve para enviar un mensaje a la consola (abrir con F12 o 'Inspeccionar')
    else:
        print("Nueva conexión de:", userId)
        emit('debug', {'data': 'Nueva conexión', 'userId': userId}) # sirve para enviar un mensaje a la consola (abrir con F12 o 'Inspeccionar')
        usuariosActivos.add(userId)

        reproducirTextoPorVoz("¡Bienvenido/a!")
        reproducirTextoPorVoz("Pulse en el botón para comenzar la conversación.")

@socketio.on('empezarConversacion')
def gestionarConversacionInicial():
    try:
        requests.post(RASA_TRACKER + "/events", json={"event": "session_started"})
        requests.post(RASA_TRACKER + "/events", json={"event": "restart"})
    except requests.exceptions.RequestException as error:
        print(f"Error al conectar con el servidor: {error}")
        emit(f"Error al conectar con el servidor: {error}")
        exit(1)
    
    enviarMensajeAChatbot("Hola")
    emit('conversacionEmpezada')
    #stream.start()
    continuarConversacion()

def continuarConversacion():
    emit('debug', 'continuarConversacion')
    data = obtenerJsonTrackerRasa()

    terminarConversacion = False
    for event in data.get("events", []):
        if event.get("event") == "bot":
            accion = event.get("metadata", {}).get("utter_action")
            if accion == "utter_despedida":
                terminarConversacion = True
                break
    if terminarConversacion == False:
        #textoRespuestaBot = procesarAudio(cola)
        textoRespuestaBot = procesarAudio()
        print('Mensaje salida: ' + textoRespuestaBot)
    else:
        stream.stop()
        print('Conversación terminada')
        emit('conversacionTerminada')

@socketio.on('pararConversacion')
def gestionarTerminarConversación():
    stream.stop()
    emit('debug', 'pararConversacion')
    enviarMensajeAChatbot("Adiós")

if __name__ == '__main__':
    #socketio.run(app) # para pruebas en local
    socketio.run(app, host="0.0.0.0", port=5000) # "0.0.0.0" para que tanto mi PC como ngrok y otros dispositivos puedan conectarse