import socketio
from game import newBallPosition
import time
import math
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

recv = 0
timeA = int(time.time() * 1000)
emits = 0

leftShift = 400
ballY = 300 + 10
ballX = 400 - 10 + leftShift
ballRad = math.radians(315)
ballVelocity = 5
scoreA = 0
scoreB = 0

def gameloop(sid, data):
	global emits, ballY, ballX, ballRad, ballVelocity, scoreA, scoreB

	time.sleep(1/(60))

	newData = newBallPosition(
		data['aY'], data['bY'],
		ballY, ballX, ballRad, ballVelocity,
		scoreA, scoreB)
	
	ballY = newData['ballY']
	ballX = newData['ballX']
	ballRad =  newData['ballRad']
	ballVelocity = newData['ballVelocity']
	scoreA = newData['scoreA']
	scoreB = newData['scoreB']

	sio.emit('game', {'data': newData}, room=sid)
	emits += 1

@sio.event
def game(sid, data):
	global recv
	global timeA
	global calc
	global emits
	calc = False
	recv = recv + 1
	timeB = int(time.time() * 1000)
	if (timeB - timeA >= 1000):
		print(f"recv: {recv}, emits:{emits}")
		timeA = timeB
		emits = 0
		recv = 0
	#set game fps
	#if not set in localhost, it get 1000 recv in the front, but in ngrok only 30 recv
	#this happens because it only ASKS when it comes, so the backend should send even
	#if the front dont asks for it. so, there will be N frames with the same front data
	gameloop(sid, data)

@sio.event
def connect(sid, environ):
	print(f"Client connected with ID: {sid}")

@sio.event
def disconnect(sid):
	print(f"Client disconnected: {sid}")

@sio.event
def message(sid, data):
	print(f"Received message: {data}")
	sio.emit('message', {'data':data})

if __name__ == '__main__':
	import eventlet
	eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)