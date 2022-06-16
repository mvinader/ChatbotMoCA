# This file contains your custom actions which can be used to run custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, ReminderScheduled, ReminderCancelled

import datetime

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
class ActionMenos12AñosEstudios(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_menos_12_años_estudios"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_final_contenedor = tracker.slots.get("res_final")
        resultado_final = resultado_final_contenedor + 1

        return [SlotSet("res_final", resultado_final)]

class ActionResultadoPrueba1(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba1_bien"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_prueba = tracker.get_slot("serie_alfanumérica")
        resultado_final_contenedor = tracker.slots.get("res_final")

        if resultado_prueba == ["1, A, 2, B, 3, C, 4, D, 5, E"]:
            #resultado = (int(resultado_prueba)+1)
            resultado = 1
            resultado_final = resultado_final_contenedor + resultado

        return [SlotSet("res_prueba1", resultado), SlotSet("res_final", resultado_final)]

class ActionResultadoAnimal1(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_animal1"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_prueba = tracker.get_slot("animal1")
        resultado_final_contenedor = tracker.slots.get("res_final")

        if resultado_prueba == "león":
            resultado = 1
            resultado_final = resultado_final_contenedor + resultado

        return [SlotSet("res_final", resultado_final)]

class ActionResultadoAnimal2(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_animal2"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_prueba = tracker.get_slot("animal2")
        resultado_final_contenedor = tracker.slots.get("res_final")

        if resultado_prueba == "rinoceronte":
            resultado = 1
            resultado_final = resultado_final_contenedor + resultado

        return [SlotSet("res_final", resultado_final)]

class ActionResultadoAnimal3(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_animal3"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_prueba = tracker.get_slot("animal3")
        resultado_final_contenedor = tracker.slots.get("res_final")

        if resultado_prueba == "camello" | resultado_prueba == "dromedario":
            resultado = 1
            resultado_final = resultado_final_contenedor + resultado

        return [SlotSet("res_final", resultado_final)]

class ActionSetReminder(Action):
    # set a timer for the user
    def name(self) -> Text:
        return "action_set_reminder"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = datetime.datetime.now() + datetime.timedelta(seconds=60)
        #entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled (
            "palabras_F",
            trigger_date_time = date,
            #entities = entities
            name = "my_reminder",
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

class ActionResultadoPrueba10(Action):
    # return the name of the action
    def name(self) -> Text:
        return "action_resultado_prueba10"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_prueba = tracker.get_slot("lista_memoria")
        resultado_final_contenedor = tracker.slots.get("res_final")

        numero_palabras_espontáneas = 0
        numero_palabras_1pista = 0
        numero_palabras_pista_elección_múltiple = 0
        palabras_espontáneas = (int(numero_palabras_espontáneas)*3)
        palabras_1pista = (int(numero_palabras_1pista)*2)
        palabras_pista_elección_múltiple = (int(numero_palabras_pista_elección_múltiple)*1)

        resultado = palabras_espontáneas + palabras_1pista + palabras_pista_elección_múltiple

        if resultado_prueba == ["1, A, 2, B, 3, C, 4, D, 5, E"]:
            #resultado = (int(resultado_prueba)+1)
            resultado = resultado + 1
            resultado_final = resultado_final_contenedor + resultado

        return [SlotSet("res_prueba10", resultado), SlotSet("res_final", resultado_final)]

class ActionResultadoFinal(Action):
    # return the final result for the user
    def name(self) -> Text:
        return "action_resultado_final"

    #register info in a slot
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resultado_final = tracker.slots.get("res_final")
        #SlotSet("res_final", resultado_final)
        dispatcher.utter_message(text = "Su resultado es de {res_final} puntos.")
        if resultado_final >= 26:
            dispatcher.utter_message(text = "Enhorabuena. Una puntuación igual o superior a 26 se considera normal.")
        else:
            dispatcher.utter_message(text = "Ha obtenido una puntuación inferior a 26. Debería ponerse en contacto con un profesional.")

        return[]
