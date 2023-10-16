import socketio
from game import newBallPosition
import time

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
	print(f"Client connected with ID: {sid}")

@sio.event
def disconnect(sid):
	print(f"Client disconnected: {sid}")

@sio.event
def game(sid, data):
	# current_time = int(time.time() * 1000)
	newData = newBallPosition(
		data['aY'], data['bY'],
		data['ballY'], data['ballX'], data['ballRad'], data['ballVelocity'],
		data['scoreA'], data['scoreB'])
	sio.emit('game', {'data': newData}, room=sid)
	# print( int(time.time() * 1000) - current_time, "ms")

@sio.event
def message(sid, data):
	print(f"Received message: {data}")
	sio.emit('message', {'data':data})

if __name__ == '__main__':
	import eventlet
	eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)