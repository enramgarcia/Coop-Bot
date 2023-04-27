import json
import cooper_utils as coop
from cooper_db import DataHandler
from cooper_responses import Response

def handler(event):
    response = Response()
    intent = coop.get_intent(event)
    active_contexts = coop.get_active_contexts(event)
    session_attributes = coop.get_session_attributes(event)
    email = coop.get_slot(intent, "Email")
    show_payment_link = coop.get_slot(intent, "ShowPaymentLink")
    student_attr = coop.get_session_attribute(event, 'student')
    session_student = None

    if student_attr:
        session_student = json.loads(student_attr)

    if email is None and session_student is None:
        return coop.ask_slot(
            "Email",
            active_contexts,
            session_attributes,
            intent,
            [coop.msg(response.get("GetEmail"))]
        )

    data_handler = DataHandler()

    if session_student is None:
        student = data_handler.find_student_by_email(email)
    else:
        student = session_student

    if student is None:
        return coop.close(
            active_contexts,
            session_attributes,
            intent,
            [coop.msg(response.get("InvalidInfo"))])

    if show_payment_link and show_payment_link == 'Sí':
        student_id = student['id']
        payment_link = data_handler.payment_link(student_id)
        return coop.close(
            active_contexts,
            session_attributes,
            intent,
            [ coop.msg(response.get("ShowPaymentLink", payment_link=payment_link))])

    owes = student["owes"]
    installments = student["installments_left"]

    if owes == 0:
        message_str = response.get("NoQuotasLeft")
    else:
        message_str = response.get("PendingQuotas", owes=owes, installments=installments)

    messages = [coop.msg(message_str)]

    messages, session_attributes = coop.add_hi(event, student, session_attributes, response, messages)

    coop.set_session_attribute(event, "student", json.dumps(student))
    session_attributes = coop.get_session_attributes(event)

    return coop.delegate(active_contexts, session_attributes, intent)
