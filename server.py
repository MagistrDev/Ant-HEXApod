# pip3 install python-socketio
# pip install "python-socketio[client]"
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://192.168.1.37/keyboard:80')
sio.wait()