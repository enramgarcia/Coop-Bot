import cooper_utils as coop

def handler(event):
    intent = coop.get_intent(event)
    active_contexts = coop.get_active_contexts(event)
    session_attributes = coop.get_session_attributes(event)

    messages = [
      {
           "contentType": "ImageResponseCard",
           "imageResponseCard": {
               "title": "Calendario de Licenciaturas",
               "imageUrl": "https://lex-cooper-images.s3.amazonaws.com/announcements/calendario_licenciatura.png"
           }
      },
      {
           "contentType": "ImageResponseCard",
           "imageResponseCard": {
               "title": "Calendario de Maestrias",
               "imageUrl": "https://lex-cooper-images.s3.amazonaws.com/announcements/calendario_maestrias.png"
           }
      }
    ]

    return coop.close(active_contexts, session_attributes, intent, messages)
