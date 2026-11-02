from flask_socketio import emit
    
def reproducirTextoPorVoz(textoRespuestaBot):
    emit("reproducirAudio", textoRespuestaBot)
