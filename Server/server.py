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
            connected_clients.append({"id": sid, "credentials": creds})
            print(sid, 'in room', room)
            print(server_io.manager.rooms['/'][room].keys())
        else:
            disconnect(sid)


# Triggered when a client disconnects from our socket
@server_io.event
def disconnect(sid):
    print(sid, 'disconnected')
    if find_id(sid):
        connected_clients.remove(find_id(sid))
    print(connected_clients)
    # connected_clients.remove(find_id(sid))

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
        await transaction_manager.increase(data)

        balance = await transaction_manager.get_user_balance(data['user_id'])
        await server_io.emit('action', {'data': f"Balance has been increased by {value} to {balance}"})
        return "OK", f"Balance has been increased by {value} to {transaction_manager.get_user_balance(data['user_id'])}"
    elif data_array[0].__contains__('decrease'):
        data['action'] = 'decrease'
        await transaction_manager.decrease(data)

        balance = await transaction_manager.get_user_balance(data['user_id'])
        await server_io.emit('action', {'data': f"Balance has been decreased by {value} to {balance}"})
        return "OK", f"Balance has been decreased by {value} to {transaction_manager.get_user_balance(data['user_id'])}"
    else:
        raise Exception("Invalid action given")

def find_id(sid):
    for key, element in enumerate(connected_clients):
        if element['id'] == sid:
            return element



def main():
    print('running')
    web.run_app(app)


main()
