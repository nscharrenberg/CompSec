import json
import time

import websockets
import asyncio


class Client:

    def __init__(self, user):
        self.user = user

    def connect_to_server(self):
        asyncio.get_event_loop().run_until_complete(self.__execute_actions())

    async def __execute_actions(self):
        ip, port = self.user.get_server()
        url = ip + ":" + port

        async with websockets.connect(url) as ws:
            await ws.send(json.dumps({"id": self.user.get_id(), "password": self.user.get_password()}))
            msg = await ws.recv()
            if msg == "Successful authorization":
                steps, delay = self.user.get_actions()
                for step in steps:
                    await ws.send(json.dumps({"action": step}))
                    time.sleep(int(delay))
