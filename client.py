import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
	print('Connected to the server')

@sio.on('game')
def on_my_response(data):
	print('Server says:', data)

sio.connect('http://localhost:5000')
sio.emit('game',
	{
		'aY':300,
		'bY':300,
		'ballY':300,
		'ballX':1200,
		'ballRad':2,
		'ballVelocity':5,
		'scoreA':0,
		'scoreB':0
})

sio.wait()