import socketio
from game import newBallPosition
import time
import math
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

recv = 0
timeA = int(time.time() * 1000)
emits = 0

#create a hashmap or list, that receives the SID as key, to access current gamedata
# preferabble with O(1). like, gamedata[sid].ballY, or something
# that will enable multiclient play our games
gamedata = {}
leftShift = 400

def calcTime(sid):
	global recv, timeA, emits
	recv = recv + 1
	timeB = int(time.time() * 1000)
	if (timeB - timeA >= 1000):
		print(f"sid: {sid} requests/s: {recv}, response/s:{emits}")
		timeA = timeB
		emits = 0
		recv = 0

def gameloop(sid, data):
	global gamedata, emits
	if(gamedata.get(sid) is None):
		gamedata[sid] = {}
		gamedata[sid]['aY'] = data['aY']
		gamedata[sid]['bY'] = data['bY']
		gamedata[sid]['ballY'] = 300 + 10
		gamedata[sid]['ballX'] = 400 - 10 + leftShift
		gamedata[sid]['ballRad'] = math.radians(315)
		gamedata[sid]['ballVelocity'] = 5
		gamedata[sid]['scoreA'] = 0
		gamedata[sid]['scoreB'] = 0
	else:
		gamedata[sid]['aY'] = data['aY']
		gamedata[sid]['bY'] = data['bY']

	gamedata[sid] = newBallPosition(
		gamedata[sid]['aY'], gamedata[sid]['bY'],
		gamedata[sid]['ballY'], gamedata[sid]['ballX'], gamedata[sid]['ballRad'], gamedata[sid]['ballVelocity'],
		gamedata[sid]['scoreA'], gamedata[sid]['scoreB'])

	sio.emit('game', {'data': gamedata[sid]}, room=sid)
	emits += 1
	calcTime(sid)

@sio.event
def game(sid, data):
	gameloop(sid, data)
	#if not set in localhost, it get 1000 recv in the front, but in ngrok only 30 recv
	#this happens because it only ASKS when it comes, so the backend should send even
	#if the front dont asks for it. so, there will be N frames with the same front data

@sio.event
def connect(sid, environ):
	print(f"Client connected with ID: {sid}")

@sio.event
def disconnect(sid):
	print(f"Client disconnected: {sid}, deleting gamedata")
	del gamedata[sid] #TODO that can cause major bugs when multiplayer is enabled

@sio.event
def message(sid, data):
	print(f"Received message: {data}")
	sio.emit('message', {'data':data})

if __name__ == '__main__':
	import eventlet
	eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)