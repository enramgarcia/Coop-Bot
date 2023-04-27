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
               [coop.msg(response.get("GetEmail"))])

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

    messages = []

    messages, session_attributes = coop.add_hi(event, student, session_attributes, response, messages)

    coop.set_session_attribute(event, "student", json.dumps(student))
    session_attributes = coop.get_session_attributes(event)

    messages.append(coop.msg(response.get("GeneratingReportCard")))

    print(f"StudentId: {student['id']}")

    career, courses = data_handler.find_grades(student['id'])

    print(f"Career: {career}, Courses: {courses}")

    if career is None:
        messages.append(coop.msg(response.get("NoCareerMsg")))
        return coop.close(active_contexts, session_attributes, intent, messages)

    report_card = f"Carrera Actual: {career['career']['name']}\n"

    for course in courses:
        report_card += f"{course['course']['name']}: {course['grade']}\n"

    messages.append(coop.msg(report_card))

    return coop.close(active_contexts, session_attributes, intent, messages)
