import json


class User:

    def __init__(self, name_file_json):
        json_user = open(name_file_json)
        user = json.load(json_user)
        self.id = user["id"]
        self.password = user["password"]
        self.ip = user["server"]["ip"]
        self.port = user["server"]["port"]
        self.delay = user["actions"]["delay"]
        self.steps = user["actions"]["steps"]

    def get_id(self):
        return self.id

    def get_password(self):
        return self.password

    def get_server(self):
        return self.ip, self.port

    def get_actions(self):
        return self.steps, self.delay

    def add_action(self, action):
        self.steps.append(action)
