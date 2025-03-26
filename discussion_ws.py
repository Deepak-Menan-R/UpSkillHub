#discussion_ws.py

from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)
