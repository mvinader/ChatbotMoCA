# Basado en la API de Rasa: https://legacy-docs-oss.rasa.com/docs/rasa/pages/http-api/
import spacy
from text_to_num import text2num
from Configuracion import SPACY_MODELO
from GestorRasa import obtenerJsonTrackerRasa

ultimosIntents = []

print("Cargando el modelo de spaCy...")
nlp = spacy.load(SPACY_MODELO)

def tratarDatosVoz(texto):
    data = obtenerJsonTrackerRasa()
    if data != None:
        ultimoIntent = data.get('latest_message', {}).get('intent', {}).get('name', None)
            
        global ultimosIntents
        ultimosIntents = ultimosIntents + [ultimoIntent]

        doc = nlp(texto)

        numerosAsociacion = { 'dieciseis': '16', 'diecisiete': '17', 'dieciocho': '18', 'diecinueve': '19' }
        cadenaProcesada = ""
        if len(doc) > 0:
            enumeracionDeTodoNumeros = True
            indice = 0
            while enumeracionDeTodoNumeros == True and indice < len(doc):
                if doc[indice].text in numerosAsociacion:
                    numero = numerosAsociacion.get(doc[indice].text)
                    cadenaProcesada = cadenaProcesada + str(numero) + ", "
                    indice = indice + 1
                elif not doc[indice].like_num:
                    enumeracionDeTodoNumeros = False
                    cadenaProcesada = ""
                else:
                    numero = doc[indice].text
                    if indice + 1 < len(doc) and ((text2num(numero, "es") > 29 and doc[indice + 1].text == "y") or doc[indice + 1].text == "mil"):
                        indice, numero = concatenarNumeros(doc, indice, numero)
                    else:
                        numero = text2num(doc[indice].text, "es")
                    cadenaProcesada = cadenaProcesada + str(numero) + ", "
                    indice = indice + 1

            if enumeracionDeTodoNumeros == True:
                cadenaProcesada = eliminarUltimaComaYEspacio(cadenaProcesada)
            else:
                if (ultimoIntent == "afirmación" or ultimoIntent == "negación") and comprobarExistenciaIntent(-2, "presentación_nombre"):
                    cadenaProcesada = procesarEnumeracionAlfanumerica(doc)
                elif ultimoIntent == "serie_números":
                    if comprobarExistenciaIntent(-2, "serie_números"):
                        cadenaProcesada = procesarOracion(doc) # frase_1
                    else:
                        cadenaProcesada = procesarEnumeracion(doc) # enumeración de 'lista_objetos'
                elif ultimoIntent == "animales" and comprobarExistenciaIntent(-2, "animales") and comprobarExistenciaIntent(-3, "animales"):
                    cadenaProcesada = procesarEnumeracion(doc) # 1ª enumeración de 'memoria'
                elif ultimoIntent == "memoria" and comprobarExistenciaIntent(-2, "memoria"):
                    cadenaProcesada = procesarCentroSanitario(doc) # centro sanitario
                elif ultimoIntent == "memoria" or ultimoIntent == "para_medir":
                    cadenaProcesada = procesarEnumeracion(doc) # 2ª y 3ª enumeración de 'memoria'
                elif ultimoIntent == "frase_2":
                    cadenaProcesada = procesarEnumeracion(doc) # enumeración de 'palabras_F'
                else:
                    cadenaProcesada = procesarOracion(doc)

            if cadenaProcesada == "":
                cadenaProcesada = texto
            if cadenaProcesada and cadenaProcesada[-1] == " ":
                cadenaProcesada = cadenaProcesada.rstrip() # elimina cualquier carácter al final de la cadena
        else:
            print("Doc obtenido a través de Spacy está vacío.")
    return cadenaProcesada

def concatenarNumeros(doc, indice, primeraPartenumero):
    palabraEnlace = doc[indice + 1].text
    indice = indice + 2
    segundaParteNumero = doc[indice].text
    numeroCompleto = primeraPartenumero + " " + palabraEnlace + " " + segundaParteNumero
    numero = text2num(numeroCompleto, "es")
    return indice, numero

def comprobarExistenciaIntent(indice, nombreIntent):
    intentExiste = False
    if ultimosIntents and -len(ultimosIntents) <= indice < len(ultimosIntents):
        if ultimosIntents[indice] == nombreIntent:
            intentExiste = True
    return intentExiste

def procesarOracion(doc):
    palabrasProhibidasComoNombresPropios = {"eh", "tijeras", "taza", "camiseta", "reloj", "plátano", "hoja",
                                            "lámpara", "llave", "vela", "cuchara",
                                            "rostro", "seda", "templo", "clavel", "rojo"}
    cadenaProcesada = ""
    for palabra in doc:
        if (not palabra.text in palabrasProhibidasComoNombresPropios) and palabra.tag_ == "PROPN":
            nombrePropioTexto = palabra.text.capitalize()
            cadenaProcesada = cadenaProcesada + nombrePropioTexto + " "
        elif palabra.like_num:
            numero = text2num(palabra.text, "es")
            cadenaProcesada = cadenaProcesada + str(numero) + " "
        else:
            cadenaProcesada = cadenaProcesada + palabra.text + " "
    return cadenaProcesada
    
def eliminarUltimaComaYEspacio(cadenaProcesada):
    if len(cadenaProcesada) >= 2 and cadenaProcesada[-2:] == ", ":
        cadenaProcesada = cadenaProcesada[:-2] # slicing para eliminar la última coma y espacio
    return cadenaProcesada # los strings son inmutables

def procesarEnumeracionAlfanumerica(doc):
    fonemasLetrasAsociacion = {
        'a': 'A', 'be': 'B', 've': 'B', 'ce': 'C', 'se': 'C', 'seh': 'C', 'sí': 'C', 'si': 'C', 'fe': 'C',
        'de': 'D', 'e': 'E', 'eh': 'E', 'efe': 'F', 'ge': 'G', 'haʧe': 'H', 'ache': 'H', 'i': 'I',
        'jota': 'J', 'ka': 'K', 'ele': 'L', 'eme': 'M', 'ene': 'N', 'o': 'O', 'pe': 'P', 'ku': 'Q',
        'erre': 'R', 'ese': 'S', 'te': 'T', 'u': 'U', 'ube': 'V', 'ubedoble': 'W', 'ekis': 'X',
        'igriega': 'Y', 'θeta': 'Z', 'ceta': 'Z'
    }
    cadenaProcesada = ""
    letra = ""
    for palabra in doc:
        if palabra.like_num:
            numero = text2num(palabra.text, "es")
            cadenaProcesada = cadenaProcesada + str(numero) + ", "
        elif palabra.text in fonemasLetrasAsociacion:
            letra = fonemasLetrasAsociacion.get(palabra.text)
            cadenaProcesada = cadenaProcesada + str(letra) + ", "
    return eliminarUltimaComaYEspacio(cadenaProcesada)

def procesarEnumeracion(doc):
    cadenaProcesada = ""
    for palabra in doc:
        cadenaProcesada = cadenaProcesada + str(palabra.text) + ", "
    return eliminarUltimaComaYEspacio(cadenaProcesada)

def procesarCentroSanitario(doc):
    cadenaProcesada = ""
    indice = 0
    while indice < len(doc):
        if doc[indice].tag_ == "PROPN":
            nombrePropioTexto = doc[indice].text.capitalize()
            cadenaProcesada = cadenaProcesada + nombrePropioTexto + " "
        elif doc[indice].text == "hospital" and (indice + 1 < len(doc) and doc[indice + 1].text == "de" or doc[indice + 1].text == "del"):
            indice, cadenaProcesada = concatenarPalabras(doc, indice, doc[indice].text)
        else:
            cadenaProcesada = cadenaProcesada + doc[indice].text + " "
        indice = indice + 1
    return cadenaProcesada

def concatenarPalabras(doc, indice, primeraPalabra):
    palabraEnlace = doc[indice + 1].text
    indice = indice + 2
    segundaPalabra = doc[indice].text.capitalize()
    palabraCompleta = primeraPalabra + " " + palabraEnlace + " " + segundaPalabra
    return indice, palabraCompleta