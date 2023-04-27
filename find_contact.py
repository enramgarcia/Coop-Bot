import cooper_utils as coop
from cooper_db import DataHandler
from cooper_responses import Response

def handler(event):
    response = Response()
    intent = coop.get_intent(event)
    active_contexts = coop.get_active_contexts(event)
    session_attributes = coop.get_session_attributes(event)

    data_handler = DataHandler()
    contact_info = data_handler.info()

    email = contact_info['email']
    phone = contact_info['phone']
    start_date = contact_info['start_day']
    end_date = contact_info['end_day']
    start_time = contact_info['start_time']
    end_time = contact_info['end_time']
    address = contact_info['address']

    messages = [
        coop.msg(response.get("ContactInfoMessage", start_time=start_time, end_time=end_time, start_date=start_date, end_date=end_date, email=email, phone=phone)),
        coop.msg(response.get("ContactAddress", address=address))
    ]

    return coop.close(active_contexts, session_attributes, intent, messages)

