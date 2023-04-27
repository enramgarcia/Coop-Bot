import json

class Response():

    def __init__(self):
        file = open('jsons/responses.json')
        self.data = json.load(file)

    def get(self, id, **kwargs):
        return self.data.get(id).format(**kwargs)

