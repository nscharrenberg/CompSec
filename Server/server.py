import json
from transactionmanager import TransactionManager
from aiohttp import web
import socketio
from passlib.hash import argon2

counter_file_path = 'counter.json'
server_io = socketio.AsyncServer()
app = web.Application()
server_io.attach(app)
connected_clients = []

transaction_manager = TransactionManager(counter_file_path, 'private.pem', 'public.pem')


# Triggered when a client connects to our socket.
@server_io.event
def connect(sid, socket, auth):
    print(sid, 'connected')
    id = json.loads(auth)['id']
    pswd = json.loads(auth)['password']
    id, pswd = check_creds_valid(sid, id, pswd)

    creds = {'id': id, 'password': pswd}
    room = id

    if not server_io.manager.rooms['/'].keys().__contains__(room):
        server_io.enter_room(sid, room)
        creds['password'] = argon2.hash(pswd)
        connected_clients.append({"id": sid, "credentials": creds})

    else:
        if argon2.verify(creds['password'],
                         find_id(next(iter(server_io.manager.rooms['/'][room])))['credentials']['password']):
            server_io.enter_room(sid, room)
            connected_clients.append({"id": sid, "credentials": creds})
        else:
            disconnect(sid)


def check_creds_valid(sid, id, pswd):
    if not isinstance(id, str):
        id = str(id)
    if not isinstance(pswd, str):
        pswd = str(pswd)
    if id == "" or pswd == "" or " " in id or " " in pswd:
        disconnect(sid)
    return id, pswd


# Triggered when a client disconnects from our socket
@server_io.event
def disconnect(sid):
    if find_id(sid):
        connected_clients.remove(find_id(sid))
    print(sid, 'disconnected')


@server_io.on('action')
async def action(sid, data):
    data_array = data.split()

    user_id = find_id(sid)

    value = 1
    if len(data_array) > 1:
        value = data_array[1]

    data = {
        "user_id": user_id['credentials']['id'],
        "session_id": sid,
        "action": data_array[0],
        "value": value
    }

    if data_array[0].__contains__('increase'):
        data['action'] = 'increase'
        try:
            await transaction_manager.increase(data)
        except Exception:
            await server_io.emit('action', {'data': f"failed to increase the balance by {value}"})
            return "ERROR", f"failed to increase the balance by {value}"

        balance = await transaction_manager.get_user_balance(data['user_id'])
        await server_io.emit('action', {'data': f"Balance has been increased by {value} to {balance}"})
        return "OK", f"Balance has been increased by {value} to {balance}"
    elif data_array[0].__contains__('decrease'):
        data['action'] = 'decrease'
        try:
            await transaction_manager.decrease(data)
        except Exception:
            await server_io.emit('action', {'data': f"failed to increase the balance by {value}"})
            return "ERROR", f"failed to increase the balance by {value}"

        balance = await transaction_manager.get_user_balance(data['user_id'])
        await server_io.emit('action', {'data': f"Balance has been decreased by {value} to {balance}"})
        return "OK", f"Balance has been decreased by {value} to {balance}"
    else:
        await server_io.emit('action', {'data': f"ERROR: You tried to perform an invalid action. You naughty person."})
        raise Exception("Invalid action given")


def find_id(sid):
    for key, element in enumerate(connected_clients):
        if element['id'] == sid:
            return element


def main():
    print('running')
    web.run_app(app)


main()
