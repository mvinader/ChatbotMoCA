# This file contains your custom actions which can be used to run custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, ReminderScheduled, ReminderCancelled
from rasa_sdk.types import DomainDict
import datetime, locale

class ActionMenos12AñosEstudios(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_menos_12_años_estudios"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_años = tracker.latest_message["intent"].get("name")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0
    
        if resultado_años == "afirmación":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba1(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba1"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_1 = tracker.get_slot("serie_números")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_1 == ["1", "A", "2", "B", "3", "C", "4", "D", "5", "E"] or resultado_1 == ["1, A, 2, B, 3, C, 4, D, 5, E"] or resultado_1 == "1, A, 2, B, 3, C, 4, D, 5, E":
            resultado = 1
            
        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionSetReminder1(Action):
    # set a timer for the user
    def name(self) -> Text:
        return "action_set_reminder_1"
    
    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = datetime.datetime.now() + datetime.timedelta(seconds=60)
        #entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled (
            "EXTERNAL_reminder_1",
            trigger_date_time = date,
            #entities = entities
            name = "reminder_1",
            kill_on_user_message = False,
        )

        return [reminder]

class ActionReactToReminder(Action):
    # remind the user to do something
    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(f"Pare.")

        return []

class ActionResultadoPrueba2(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba2"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_2 = tracker.get_slot("lista_objetos")
        palabras = resultado_2.split(", ")
        resultado_final_contenedor = tracker.slots.get("res_final")
        #cuenta = 0
        #for i in range(len(palabras)):
        #    if ("tijeras" or "taza" or "camiseta" or "reloj" or "plátano" or "hoja" or "lámpara" or "llave" or "vela" or "cuchara") == palabras[i]:
        #        cuenta += 1
        #
        #def switch(cuenta):
        lista_solución = ['tijeras','taza','camiseta','reloj','plátano','hoja','lámpara','llave','vela','cuchara']
        element = [x for x in palabras if x in lista_solución]

        n_palabras = len(element)
        def switch(n_palabras):
            resultado_local = 0
            if(n_palabras == 9 or n_palabras == 10):
                resultado_local = 3
            elif(n_palabras == 6 or n_palabras == 7 or n_palabras == 8):
                resultado_local = 2
            elif(n_palabras == 4 or n_palabras == 5):
                resultado_local = 1
            return resultado_local

        resultado = 0
        resultado = switch(n_palabras)
        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoAnimal1(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_animal1"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_león = tracker.get_slot("animales")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_león == "león":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoAnimal2(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_animal2"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_rino = tracker.get_slot("animales")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_rino == "rinoceronte":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoAnimal3(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_animal3"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_camello = tracker.get_slot("animales")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0
        
        if resultado_camello == "camello" or resultado_camello == "dromedario":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoSerieNúmerosDirecto(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_serie_números_directo"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_6_directo = tracker.get_slot("serie_números")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_6_directo == ["2", "1", "8", "5", "4"] or resultado_6_directo == ["2, 1, 8, 5, 4"] or resultado_6_directo == "2, 1, 8, 5, 4":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoSerieNúmerosInverso(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_serie_números_inverso"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_6_inverso = tracker.get_slot("serie_números")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_6_inverso == ["2", "4", "7"] or resultado_6_inverso == ["2, 4, 7"] or resultado_6_inverso == "2, 4, 7":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoSerieLetras(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_serie_letras"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_6_A = tracker.get_slot("serie_números")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_6_A == 11 or resultado_6_A == 10 or resultado_6_A == ["10"] or resultado_6_A == "10" or resultado_6_A == 9:
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionSetReminder2(Action):
    # set a timer for the user
    def name(self) -> Text:
        return "action_set_reminder_2"
    
    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = datetime.datetime.now() + datetime.timedelta(seconds=60)
        #entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled (
            "EXTERNAL_reminder_2",
            trigger_date_time = date,
            #entities = entities
            name = "reminder_2",
            kill_on_user_message = False,
        )

        return [reminder]

class ActionResultadoSerie7(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_serie_7"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        resultado_6_serie = tracker.get_slot("serie_números")
        resultado_final_contenedor = tracker.slots.get("res_final")
        items = resultado_6_serie.split(', ')
        i = int(items[0]) - 7
        cuenta = 0
        while i > 0:
            if str(i) in resultado_6_serie:
                cuenta += 1
            i -= 7
        resultado = 0    
        def switch(cuenta):
            if(cuenta == 1):
                resultado = 1
            elif(cuenta == 2 or cuenta == 3):
                resultado = 2
            elif(cuenta > 3):
                resultado = 3
            return resultado

        resultado = switch(cuenta)
        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba7_1(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba7_1"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
            
        resultado_7 = tracker.get_slot("frase_1")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_7 == "Solo sé que le toca a Juan ayudar hoy." or resultado_7 == "Solo sé que le toca a Juan ayudar hoy" or resultado_7 == "solo se que le toca a Juan ayudar hoy":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba7_2(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba7_2"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
            
        resultado_7 = tracker.get_slot("frase_2")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_7 == "El gato siempre se esconde debajo del sofá cuando hay perros en la habitación." or resultado_7 == "El gato siempre se esconde debajo del sofá cuando hay perros en la habitación." or resultado_7 == "el gato siempre se esconde debajo del sofá cuando hay perros en la habitación" or resultado_7 == "el gato siempre se esconde debajo del sofa cuando hay perros en la habitacion":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionSetReminder2(Action):
    # set a timer for the user
    def name(self) -> Text:
        return "action_set_reminder_3"
    
    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = datetime.datetime.now() + datetime.timedelta(seconds=60)
        #entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled (
            "EXTERNAL_reminder_3",
            trigger_date_time = date,
            #entities = entities
            name = "reminder_3",
            kill_on_user_message = False,
        )

        return [reminder]

class ActionResultadoPrueba8(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba8"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:  Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        resultado_8 = tracker.get_slot("lista_F")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0
        #topicList:['topic_1', 'topic_2']
        
        if len(resultado_8) >= 11:
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba9_2(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba9_2"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:  Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        resultado_9_2 = tracker.get_slot("para_viajar")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_9_2 == "medios de transporte" or resultado_9_2 == "transportes" or resultado_9_2 == "medios de locomoción" or resultado_9_2 == "para viajar":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba9_3(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba9_3"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:  Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        resultado_9_3 = tracker.get_slot("para_medir")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        if resultado_9_3 == "instrumentos de medición" or resultado_9_3 == "instrumentos de medida" or resultado_9_3 == "para medir":
            resultado = 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba10(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba10"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_prueba = tracker.get_slot("lista_memoria")
        palabras = resultado_prueba.split(", ")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0
        #for i in range(len(palabras)):
        #    if ("rostro" or "seda" or "templo" or "clavel" or "rojo") == palabras[i]:
        #        resultado += 1
        lista_solución = ['rostro','seda','templo','clavel','rojo']
        element = [x for x in palabras if x in lista_solución]
        resultado = len(element)

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

#class ValidateFechaForm(FormValidationAction):
#    def name(self) -> Text:
#        return "validate_fecha_form"
#
#    @staticmethod
#    def día_db() -> List[Text]:
#        """Base de datos de días admitidos"""
#
#        return ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo", "miercoles", "sabado" ]
#
#    def validate_día(self, slot_value: Any, dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: DomainDict, ) -> Dict[Text, Any]:
#        """Validar el valor del mes"""
#
#        if slot_value.lower() in self.mes_db():
#            # validation succeeded, set the value of the "día" slot to value
#            return {"día": slot_value}
#        else:
#            # validation failed, set this slot to None so that the user will be asked for the slot again
#            return {"día": None}
#
#    @staticmethod
#    def número_fecha_db() -> List[Text]:
#        """Base de datos de números de fecha admitidos"""
#
#        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#                "28", "29", "30", "31", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
#
#    def validate_número_fecha(self, slot_value: Any, dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: DomainDict, ) -> Dict[Text, Any]:
#        """Validar el valor del mes"""
#
#        if slot_value.lower() in self.mes_db():
#            # validation succeeded, set the value of the "número_fecha" slot to value
#            return {"número_fecha": slot_value}
#        else:
#            # validation failed, set this slot to None so that the user will be asked for the slot again
#            return {"número_fecha": None}
#
#    @staticmethod
#    def mes_db() -> List[Text]:
#        """Base de datos de meses admitidos"""
#
#        return ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
#
#    def validate_mes(self, slot_value: Any, dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: DomainDict, ) -> Dict[Text, Any]:
#        """Validar el valor del mes"""
#
#        if slot_value.lower() in self.mes_db():
#            # validation succeeded, set the value of the "mes" slot to value
#            return {"mes": slot_value}
#        else:
#            # validation failed, set this slot to None so that the user will be asked for the slot again
#            return {"mes": None}
            
#tracker.slots_to_validate OJOOOOOOOOOOOOOOOOO

#class AbstractFormValidatorAction(Action):
#
#  def run(...):
#    slots_to_validate = tracker.form_slots_to_validate()
#    for slot_name, value in slots_to_validate.items():
#       function_name = f"validate_{slot_name}"
#       fn = getattr(self, function_name)
#       fn(value, tracker, bla)

class ActionResultadoFecha(Action):
    def name(self) -> Text:
        return "action_resultado_fecha"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any] ) -> List[Dict[Text, Any]]:

        resultado_día = tracker.get_slot("día")
        resultado_número_día = tracker.get_slot("número_fecha")
        resultado_mes = tracker.get_slot("mes")
        resultado_año = tracker.get_slot("año")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0

        locale.setlocale(locale.LC_ALL, 'es_ES')
        date = datetime.datetime.now()

        día = date.strftime("%A")
        número_día = date.strftime("%d")
        mes = date.strftime("%B")
        año = date.strftime("%Y")
        #entities = tracker.latest_message.get("entities")

        if resultado_día == día:
            resultado += 1
        if resultado_mes == mes:
            resultado += 1
        if resultado_número_día == número_día:
            resultado += 1
            print(resultado)
        else:
            print(resultado_número_día)
            print(número_día)
        if resultado_año == año:
            resultado += 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoLugar(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_lugar"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        lugar_a_almacenar = tracker.get_slot("lugar_a_almacenar")
        lugar = tracker.get_slot("lugar")
        localidad_a_almacenar = tracker.get_slot("localidad_a_almacenar")
        localidad = tracker.get_slot("localidad")
        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado = 0
        if lugar_a_almacenar == lugar and localidad_a_almacenar == localidad:
            resultado += 1

        resultado_final = resultado_final_contenedor + resultado
        print(resultado_final)
        return [SlotSet("res_final", resultado_final)]

class ActionResultadoFinal(Action):
    # return the final result for the user
    def name(self) -> Text:
        return "action_resultado_final"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        res_final = tracker.slots.get("res_final")
        #SlotSet("res_final", resultado_final)
        dispatcher.utter_message(text = f"Su resultado es de {res_final} puntos.")
        if res_final >= 26:
            dispatcher.utter_message(text = "Enhorabuena. Una puntuación igual o superior a 26 se considera normal.")
        else:
            dispatcher.utter_message(text = "Ha obtenido una puntuación inferior a 26. Debería ponerse en contacto con un profesional.")

        return[]