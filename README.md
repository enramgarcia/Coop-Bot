# Coop-Bot

## Introducción

Funciones lambda para Coop Bot, un chatbot hecho en AWS Lex como proyecto final de la UIP.

## Requerimientos

Se debe de crear un bot en lex con los siguientes intents:
- FindGrades: Para buscar las notas en el API.
- FindContactInfo: Para buscar la información de contacto de la universidad en el API.
- FindPayments: Para buscar la información de cuotas por pagar a la universidad en el API.
- Calendar: Para mostrar imagenes del calendario universitario desde AWS S3.

Ademas se debe crear un layer que contenga la libreria de requests de python para llamar al API en AWS EC2 y se debe de apuntar al servidor del mismo en el archivo cooper_db.py, ejemplo:
```class DataHandler():
    def __init__(self):
        self.server = "http://ec2-44-208-26-78.compute-1.amazonaws.com/api"
```

Más por venir a medida que lo siga modificando.

