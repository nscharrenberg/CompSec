import json
import time

import socketio
import asyncio


class Client:
    def __init__(self, user):
        self.user = user
        self.sio = socketio.Client()

    def connect_to_server(self):
        asyncio.get_event_loop().run_until_complete(self.__execute_actions())

    async def __execute_actions(self):
        ip, port = self.user.get_server()
        url = "http://" + ip + ":" + port

        self.sio.connect(url, auth=json.dumps({"id": self.user.get_id(), "password": self.user.get_password()}))
        self.sio.wait()
        steps, delay = self.user.get_actions()
        for step in steps:
            self.sio.send(json.dumps({"action": step}))
            self.sio.wait()
            time.sleep(int(delay))
