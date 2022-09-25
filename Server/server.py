import json

from aiohttp import web
import socketio
import socket

server_io = socketio.AsyncServer()
app = web.Application()
server_io.attach(app)
connected_clients=[]


# Triggered when a client connects to our socket.
@server_io.event
def connect(sid, socket, auth):
    print(sid, 'connected')
    creds = json.loads(auth)
    room = creds['id']
    if not server_io.manager.rooms['/'].keys().__contains__(room):
        server_io.enter_room(sid, room)
        print(sid, 'in room', room)
        connected_clients.append({"id": sid, "credentials": creds})

    else:
        if find_id(next(iter(server_io.manager.rooms['/'][room])))['credentials']['password'] == creds['password']:
            server_io.enter_room(sid, room)
            print(sid, 'in room', room)

        else:
            print(server_io.manager.rooms['/'][room].keys())


# Triggered when a client disconnects from our socket
@server_io.event
def disconnect(sid):
    print(sid, 'disconnected')
    # connected_clients.remove(find_id(sid))

def find_id(sid):
    for key, element in enumerate(connected_clients):
        if element['id'] == sid:
            return element


# def make_connections_list():
#     server_io.socket.clients =


def main():
    print('running')
    web.run_app(app)


main()
