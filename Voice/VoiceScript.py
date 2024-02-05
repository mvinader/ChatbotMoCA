## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition # import the library
import subprocess
from gtts import gTTS

# Initial payload
# sender = input("What is your name?\n")
# jsonData = requests.post('http://localhost:5002/webhooks/rest/webhook', json = { "sender": sender, "mensajeUsuario": "Hello"} )
jsonData = requests.post('http://localhost:5005/webhooks/rest/webhook', json = { "message": "Hola" })

print("El chatbot dice: ", end = ' ')

mensajeBot = ""
for i in jsonData.json():
    mensajeBot = i['text']
    print(f"{mensajeBot}")

instancia = gTTS(text = mensajeBot, lang = "es")
instancia.save("welcome.mp3")
# Playing the converted file
print("Guardado.")
#subprocess.call(['mpg321', "C:/Users/maviv/anaconda3/envs/rasa3.6/rasa36/welcome.mp3", '--play-and-exit'])
subprocess.call(['mpg321', "welcome.mp3", '--play'])
#subprocess.call(['vlc', "welcome.mp3", '--play-and-exit'])

mensajeUsuario = ""
#while mensajeBot != "Adiós" or mensajeBot!='Chao':
jsonData = speech_recognition.Recognizer()  # initialize recognizer
with speech_recognition.Microphone() as source:  # mention source it will be either Microphone or audio files.
    print("Di algo:")
    audio = jsonData.listen(source)  # listen to the source
    try:
        mensajeUsuario = jsonData.recognize_google(audio)  # use recognizer to convert our audio into text part.
        print("Has dicho : {}".format(mensajeUsuario))
    except:
        print("Lo siento, pero no he podido reconocer lo que has dicho.")  # In case of voice not recognized  clearly
#if len(mensajeUsuario) == 0:
#    continue
print("Enviando el mensaje...")

#Respuesta del bot
jsonData = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": mensajeUsuario})

print("El chatbot dice: ", end = ' ')

for i in jsonData.json():
    mensajeBot = i['text']
    print(f"{mensajeBot}")

instancia = gTTS(text = mensajeBot, lang = "es")
instancia.save("welcome.mp3")
print("Guardado.")
# Playing the converted file
subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])