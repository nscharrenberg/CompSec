import json

import socketio
import asyncio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.on('action')
def action(data):
    print('message received with ', data)


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print('disconnected from server')


def connect_to_server(user):
    asyncio.get_event_loop().run_until_complete(execute_actions(user))


async def execute_actions(user):
    ip, port = user.get_server()
    url = "http://" + ip + ":" + port

    sio.connect(url, auth=json.dumps({"id": user.get_id(), "password": user.get_password()}))
    steps, delay = user.get_actions()
    for step in steps:
        sio.emit('action', step)
        sio.sleep(int(delay))

    sio.disconnect()