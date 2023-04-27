import json


def close(active_contexts, session_attributes, intent, messages, state='Fulfilled'):
    intent['state'] = state

    return {
        'sessionState': {
            'activeContexts': active_contexts,
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent
        },
        'requestAttributes': {},
        'messages': messages
    }


# Retira el objeto del intent en el caso se encuentre en la estructura del JSON recibido.
def get_intent(event):
    interpretations = event['interpretations']

    if len(interpretations) == 0:
        return None

    return interpretations[0]['intent']


# Retira el contexto activo del request.
def get_active_contexts(event):
    try:
        return event['sessionState'].get('activeContexts')
    except:
        return []


# Elimina los contextos inactivos del request.
def remove_inactive_contexts(contexts):
    if not contexts:
        return contexts

    new_contexts = []

    for context in contexts:
        time_to_live = context.get('timeToLive')

        if time_to_live and time_to_live.get('turnsToLive') != 0:
            new_contexts.append(context)

    return new_contexts


# Retira los atributos de session con las variables globales.
def get_session_attributes(event):
    try:
        return event['sessionState']['sessionAttributes']
    except:
        return None


# Retira una variable global del session attribute
def get_session_attribute(event, attribute):
    try:
        return get_session_attributes(event).get(attribute)
    except:
        return None


# Ingresa el valor de un variable global a la sesión.
def set_session_attribute(event, attribute, value):
    try:
        # Validar si existe una sesión activa con atributos de lo contrario crea una sesión para agregar los atributos.
        if get_session_attributes(event) is None:
            event['sessionState']['sessionAttributes'] = {}

        event['sessionState']['sessionAttributes'][attribute] = value
        return event
    except:
        print('No se pudo ingresar el atributo global')
        return event


# Intent buscar un slot y retorna el valor encontrado si existe.
def get_slot(intent, name):
    try:
        slot = intent['slots'].get(name)

        # No hay slots
        if not slot:
            return None

        value = slot.get('value')

        if value:
            interpreted_value = value.get('interpretedValue')
            original_value = value.get('originalValue')

            if interpreted_value:
                return interpreted_value
            else:
                return original_value
        else:
            return None
    except Exception as err:
        print(f"Error: {err}")
        return None


# Pregunta por un slot.
def ask_slot(
        slot_name,
        active_contexts,
        session_attributes,
        intent,
        messages):
    active_contexts = remove_inactive_contexts(active_contexts)
    intent['state'] = 'InProgress'

    # si no existen los atributos de sesión creamos uno nuevo.
    if not session_attributes:
        session_attributes = {}

    session_attributes['previous_message'] = json.dumps(messages)
    session_attributes['previous_dialog_type'] = 'ElicitSlot'
    session_attributes['previous_slot_to_elicit'] = slot_name

    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'activeContexts': active_contexts,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_name
            },
            'intent': intent
        },
        'requestAttributes': {},
        'messages': messages
    }


def delegate(active_contexts, session_attributes, intent, messages=[]):
    active_contexts = remove_inactive_contexts(active_contexts)

    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'activeContexts': active_contexts,
            'dialogAction': {
                'type': 'Delegate',
            },
            'intent': intent,
            'state': 'ReadyForFulfillment'
        },
        'requestAttributes': {},
        'messages': messages
    }


def add_hi(event, student, session_attributes, response, messages):
    if student is None:
        return messages, session_attributes

    if get_session_attribute(event, "said_hi") is not None:
        return messages, session_attributes

    name = student["name"]
    last_name = student["last_name"]

    messages.insert(0, {"contentType": "PlainText", "content": response.get("SayHi", name=name, last_name=last_name)})

    event = set_session_attribute(event, "said_hi", "True")
    session_attributes = get_session_attributes(event)

    return messages, session_attributes


def msg(message_str, content_type="SSML"):
    return {"contentType": content_type, "content": message_str}
