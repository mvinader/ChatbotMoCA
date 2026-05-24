# ============================================================
# CONFIGURACIÓN DE FLASK
# ============================================================
FLASK_CLAVE = 'secret!'

# ============================================================
# CONFIGURACIÓN DE AUDIO
# ============================================================
# Kaldi
KALDI_FRECUENCIA_MUESTREO = 16000  # 16 kHz -> los modelos están entrenados a esta frecuencia

# pyttsx3
PYTTSX3_VELOCIDAD_HABLA = 180 # por defecto es 200
PYTTSX3_VOLUMEN = 1.0 # entre 0.0 y 1.0

# Detección de audio
AUDIO_FRECUENCIA_MUESTREO = 16000  # Frecuencia de muestreo en Hz
AUDIO_TAMANYO_BLOQUE = 8000        # Tamaño de bloque de audio
AUDIO_DATA_TYPE = 'int16'          # Tipo de dato de audio
AUDIO_N_CANALES = 1                # Número de canales de audio

# Detección de silencio
TIEMPO_POR_BLOQUE_MS = 100    # Tiempo en ms por bloque (ajustar según 'AUDIO_TAMANYO_BLOQUE' y 'AUDIO_FRECUENCIA_MUESTREO')
MAX_SILENCIOS_PERMITIDOS = 5

# ============================================================
# CONFIGURACIÓN DE RASA
# ============================================================
RASA_RUTA_SERVIDOR = "localhost:5005"
RASA_REST_WEBHOOK = "http://" + RASA_RUTA_SERVIDOR + "/webhooks/rest/webhook"
RASA_TRACKER = "http://" + RASA_RUTA_SERVIDOR + "/conversations/default/tracker"

# ============================================================
# CONFIGURACIÓN DE SPACY
# ============================================================
#SPACY_MODELO = "es_core_news_md" # modelo mediano
SPACY_MODELO = "es_core_news_lg" # modelo grande

# ============================================================
# LÓGICA DE NEGOCIO
# ============================================================
EXPLICACIONES_OCULTAR = {
    "Rostro, seda, templo, clavel, rojo.",
    "2, 1, 8, 5, 4.",
    "7, 4, 2.",
    "F, B, A, C, M, N, A, A, J, K, L, B, A, F, A, K, D, E, A, A, A, J, A, M, O, F, A, A, B.",
    "Solo sé que le toca a Juan ayudar hoy.",
    "El gato siempre se esconde debajo del sofá cuando hay perros en la habitación."
}