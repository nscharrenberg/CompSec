from aiohttp import web
import socketio
from fileutils import FileUtil

counter_file_path = 'counter.json'

file_util = FileUtil(counter_file_path)

server_io = socketio.AsyncServer()
app = web.Application()
server_io.attach(app)

# Triggered when a client connects to our socket.
@server_io.event
def connect(sid, socket):
    print(sid, 'connected')

# Triggered when a client disconnects from our socket
@server_io.event
def disconnect(sid):
    print(sid, 'disconnected')

@server_io.on('increase')
async def increase_event(sid, data):
    data = await file_util.read()['data']
    print(data)



def main():

    print('running')
    web.run_app(app)


main()




