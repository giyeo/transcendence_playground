<!-- App.svelte -->
<div class="paddle"			style="top: {paddleAy}px;	left: {paddleAx}px;"></div>
<div class="paddle"			style="top: {paddleBy}px;	left: {paddleBx}px;"></div>

<div class="ball"			style="top: {ball.y}px;	left: {ball.x}px;"></div>

{#each ballPositionHistory as item, index (item)}
  <div class="ball" style="top: {item.y}px; left: {item.x}px; opacity: 0.1;"></div>
{/each}

<div class="horizontalWall" style="top: {0}px;		left: {leftShift + 0}px;"></div>
<div class="horizontalWall" style="top: {310}px;	left: {leftShift + 0}px; background-color: rgba(200,200,200,0.2);"></div>
<div class="horizontalWall" style="top: {620}px;	left: {leftShift + 0}px;"></div>

<div class="verticalWall"	style="top: {20}px;		left: {leftShift + 390}px;"></div>

<div class="score"			style="top: {60}px;		left: {leftShift + 250}px;">{scoreA}</div>
<div class="score"			style="top: {60}px;		left: {leftShift + 460}px;">{scoreB}</div>

<div class="info"			style="top: {650}px;	left: {leftShift + 0}px;">{stop} 800x600px object width 20px, paddle 100px</div>
<div class="info"			style="top: {650}px;	left: {leftShift + 900}px;">vel:{ball.velocity} deg:{toDegre(ball.radians)} \n angle:{rad(ball.radians)}</div>
<!-- <div>
	<Socket />
</div> -->
<audio id="paddle" src="./paddle.mp3"></audio>
<audio id="wall" src="./wall.mp3"></audio>
<audio id="score" src="./score.mp3"></audio>

<script lang="js">
	import { onMount } from 'svelte';
	import io from 'socket.io-client';
	let framerate = 12; //16 = 60fps
	let player = 'A'
	let leftShift = 400;
	let scoreA = 0;
	let scoreB = 0;
	let paddleAx = leftShift + 35;
	let paddleBx = leftShift + 745;
	let paddleAy = 20 + 300 - 50;
	let paddleBy = 20 + 300 - 50;
	let paddleSize = 100;
	let topWall = 20;
	let botWall = 600;
	let resetx = 400 - 10 + leftShift
	let resety = 300 + 10
	var stop = 1;
	var ball = {
			x: resetx,
			y: resety,
			radians: rad(315),
			velocity: 5
		};
	var ballPositionHistory = [];
	
	// const socket = io('0.tcp.sa.ngrok.io:19720'); // Replace with your Socket.IO server URL
	// const socket = io('34.95.142.132:5000')
	const socket = io('localhost:5000');
	async function goToPosition(newX, newY) {//interpolation, adding frames between
		var oldX = ball.x;
		var oldY = ball.y;
		var DLSS = 4;
		var i = 0
		if(Math.abs(newX-oldX) < 300 ) {
			while(i < DLSS) {
				ball.x += ((newX - oldX) / DLSS );
				ball.y += ((newY - oldY) / DLSS );
				await sleep(framerate / DLSS );
				i++;
			}
		}
		ball.x = newX;
		ball.y = newY;
	}

	socket.on('game', (data) => {
		if(player === 'B')
			paddleAy = data.data.aY;//i dont receive myself, only if i'm player B
		else
			paddleBy = data.data.bY;
		// ball.x = data.data.ballX;
		// ball.y = data.data.ballY;
		goToPosition(data.data.ballX, data.data.ballY)
		ball.radians = data.data.ballRad;
		ball.velocity = data.data.ballVelocity;
		scoreA = data.data.scoreA;
		scoreB = data.data.scoreB;
		if(scoreA > 10 || scoreB > 10) {
				scoreA = 0;
				scoreB = 0;
		}
	});

	const game = () => {
		socket.emit('game', {
			aY: paddleAy,//
			bY: paddleBy
		});
	};

	onMount(() => {
		socket.emit('join', 'User has joined the game');
	});

	function playAudio(name) {
		const audio = document.getElementById(name);
		audio.play();
  	}

	function rad(x) {
    	return ((x % 360) * (Math.PI / 180)) % 360;
	}

	function toDegre(x) {
		return (x / Math.PI) * 180;
	}

	// Function to add a new point to the list
	//create client predict tail
	function addPosition(x, y) {
		if (ballPositionHistory.length >= 25) {
		// If the list has 10 or more elements, remove the oldest element
			ballPositionHistory.shift();
		}
		ballPositionHistory = [...ballPositionHistory, { x, y }];
	}

	function soundByPosition() {
		if (ball.x < leftShift || ball.x > leftShift + 800) {
			playAudio("score");
		}

		if ( (ball.y > paddleAy && ball.y < paddleAy + paddleSize ) 
		&& (ball.x > paddleAx - 10 && ball.x < paddleAx + 20)) {
			playAudio("paddle");
		}
	
		if ( (ball.y > paddleBy && ball.y < paddleBy + paddleSize ) 
		&& (ball.x > paddleBx - 20 && ball.x < paddleBx + 10)) {
			playAudio("paddle");
		}

		if (ball.y <= topWall || ball.y >= botWall) {
			playAudio("wall");
		}
	}

	function sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

	async function gameloop() {
		while(1) {
			game()
			addPosition(ball.x, ball.y);
			soundByPosition();
			await sleep(framerate);
		}
	}

	gameloop();
	//800px x 600px //////////////////////////////////////////////////////////////////////q

	let keyDownInterval = null;
	let isKeyDown = false; // Flag to track key press
	function startContinuousMove(direction) {
		if (!isKeyDown) {
			isKeyDown = true;
			keyDownInterval = setInterval(() => {
				if (direction === 'up' && paddleAy >= 30) {
					paddleAy -= 10; // Move rectangle 1 upward
					// paddleBy -= 10;
				} else if (direction === 'down' && paddleAy < 520) {
					paddleAy += 10; // Move rectangle 2 downward
					// paddleBy += 10;
				}
			}, 16); // Adjust the interval as needed for desired speed
		}
	}

	function stopContinuousMove() {
		clearInterval(keyDownInterval);
		isKeyDown = false; // Reset the flag
	}

	// Handle keydown and keyup events
	function handleKeyDown(event) {
		if (event.key === 'ArrowUp') {
			startContinuousMove('up');
		} else if (event.key === 'ArrowDown') {
			startContinuousMove('down');
		}
	}

	function handleKeyUp(event) {
		if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
			stopContinuousMove();
		}
		if (event.code === 'Space') {
			if(stop < 0)
				gameloop();
			stop = stop * -1;
		}
	}
	// Attach keydown and keyup event listeners to the document
	document.addEventListener('keydown', handleKeyDown);
	document.addEventListener('keyup', handleKeyUp);
</script>