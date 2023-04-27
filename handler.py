import os
import json
import boto3
# Imports del proyecto
import cooper_utils as coop
import find_student
import find_contact
import find_payments
import calendar_intent

client = boto3.client('lambda')

def router(event):
    intent = coop.get_intent(event)
    fn_name = intent['name']

    active_contexts = coop.get_active_contexts(event)
    session_attributes = coop.get_session_attributes(event)

    print(f"Intent: {intent} -> Lambda: {fn_name} Event: {event}")

    student = coop.get_session_attribute(event, 'student')

    if student:
        event = coop.set_session_attribute(event, 'student', student)

    if fn_name == 'FindGrades':
        return find_student.handler(event)
    elif fn_name == 'FindContactInfo':
        return find_contact.handler(event)
    elif fn_name == 'FindPayments':
        return find_payments.handler(event)
    elif fn_name == 'Calendar':
        return calendar_intent.handler(event)

    print('Interesante')

    messages = [
        {
            "contentType": "PlainText",
            "content": "Muchas gracias."
        }
    ]

    return coop.close(active_contexts, session_attributes, intent, messages)

def main_handler(event, context):
    print(event)
    print(context)
    return router(event)
