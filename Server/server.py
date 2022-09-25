import json
from transactionmanager import TransactionManager
from fileutils import FileUtil
from aiohttp import web
import socketio
import rsa

counter_file_path = 'counter.json'
server_io = socketio.AsyncServer()
app = web.Application()
server_io.attach(app)
connected_clients=[]

transaction_manager = TransactionManager(counter_file_path, 'private.pem', 'public.pem')

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

@server_io.on('action')
def action(sid, data):
    data_array = data.split()

    if data_array[0].__contains__('increase'):
        value = 1
        if len(data_array) > 1:
            value = data_array[1]

        transaction_manager.increase(value)

        server_io.emit('action', {'data': 'Balance has been increased'})
        return "OK", "Balance has been increased"
    elif data_array[0].__contains__('decrease'):
        value = 1
        if len(data_array) > 1:
            value = data_array[1]

        transaction_manager.decrease(value)

        server_io.emit('action', {'data': 'Balance has been decreased'})
        return "OK", "Balance has been decreased"
    else:
        raise Exception("Invalid action given")

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
