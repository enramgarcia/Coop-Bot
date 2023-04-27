import json
import requests


class DataHandler():
    def __init__(self):
        self.server = "http://ec2-44-208-26-78.compute-1.amazonaws.com/api"

    def info(self):
        try:
            response = requests.get(f"{self.server}/data")

            if response.status_code != 200:
                return None

            return response.json()
        except Exception as e:
            print(e)
            return None

    def payment_link(self, student_id):
        return f"{self.server}/pay?student={student_id}"

    def find_student_by_email(self, email):
        try:
            response = requests.post(f"{self.server}/students", {
                "email": email
            })

            if response.status_code != 200:
                print("No se pudo encontrar la información peticionada.")
                return None

            return response.json()
        except Exception as e:
            print(e)
            return None

    def find_grades(self, student_id):
        try:
            response = requests.get(f"{self.server}/students/{student_id}/data")

            if response.status_code != 200:
                return None, None

            data = response.json()

            careers = data['careers']
            courses = data['courses']

            if len(careers) == 0:
                return None, None

            return careers[0], courses
        except Exception as e:
            print(e)
            return None, None
