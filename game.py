import math

leftShift = 400
aX = leftShift + 35
bX = leftShift + 745
paddleSize = 100
topWall = 20
botWall = 600
middleX = 400 - 10 + leftShift
middleY = 300 + 10

def rad(x):
	return ((custom_modulus(x,360)) * (math.pi / 180))
def custom_modulus(a, b):
    return (a % b + b) % b
def newBallPosition(aY, bY, ballY, ballX, ballRad, ballVelocity, scoreA, scoreB):
	# print(aY, bY, ballX, ballY, ballVelocity)
	ballX += ballVelocity * math.cos(ballRad)
	ballY += ballVelocity * math.sin(ballRad)
	#ball went off limits
	if (ballX < leftShift or ballX > leftShift + 800):
		if(ballX < leftShift):
			scoreB += 1
			ballX = bX - 10
		else:
			scoreA += 1
			ballX = aX + 10
		ballY = middleY
		ballVelocity = 5
	#hit paddle A
	if ((ballY > aY and ballY < aY + paddleSize) 
	and (ballX > aX - 10 and ballX < aX + 10) ):
		if(ballY > aY + 75):
			ballRad = rad(60)
		elif (ballY < aY + 25):
			ballRad = rad(300)
		else:
			ballRad = rad(180) - ballRad
		if(ballVelocity < 10):
			ballVelocity += 0.25 
	#hit paddle B
	if ((ballY > bY and ballY < bY + paddleSize)
	and (ballX > bX - 10 and ballX < bX + 10)):
		if(ballY > bY + 75):
			ballRad = rad(150)
		elif (ballY < bY + 25):
			ballRad = rad(225)
		else:
			ballRad = rad(180) - ballRad
		if(ballVelocity < 10):
			ballVelocity += 0.25
	#hit wall
	if (ballY <= topWall or ballY >= botWall):
		ballRad = -ballRad

	#bot
	# if(ballY >= 570):
	# 	bY = 520
	# elif(ballY <= 70):
	# 	bY = 20
	# else:
	# 	bY = ballY - 50

	return ({
		'aY':aY,
		'bY':bY,
		'ballY':ballY,
		'ballX':ballX,
		'ballRad':ballRad,
		'ballVelocity':ballVelocity,
		'scoreA':scoreA,
		'scoreB':scoreB
	})