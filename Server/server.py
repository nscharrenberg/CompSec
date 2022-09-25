from aiohttp import web
import socketio
import socket

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

def main():

    print('running')
    web.run_app(app)


main()




