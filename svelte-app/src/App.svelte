<!-- App.svelte -->
<div class="paddle"			style="top: {paddleAy}px;	left: {paddleAx}px;"></div>
<div class="paddle"			style="top: {paddleBy}px;	left: {paddleBx}px;"></div>

<div class="ball"			style="top: {ball.y}px;	left: {ball.x}px;"></div>

<div class="horizontalWall" style="top: {0}px;		left: {leftShift + 0}px;"></div>
<div class="horizontalWall" style="top: {310}px;	left: {leftShift + 0}px; background-color: rgba(200,200,200,0.2);"></div>
<div class="horizontalWall" style="top: {620}px;	left: {leftShift + 0}px;"></div>

<div class="verticalWall"	style="top: {20}px;		left: {leftShift + 390}px;"></div>

<div class="score"			style="top: {60}px;		left: {leftShift + 250}px;">{scoreA}</div>
<div class="score"			style="top: {60}px;		left: {leftShift + 460}px;">{scoreB}</div>

<div class="info"			style="top: {650}px;	left: {leftShift + 0}px;">800x600px object width 20px, paddle 100px</div>
<div class="info"			style="top: {650}px;	left: {leftShift + 900}px;">{ball.velocity} deg:{toDegre(ball.radians)} \n angle:{rad(ball.radians)}</div>
<!-- <div>
	<Socket />
</div> -->

<script lang="ts">
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
	var ball = {
			x: resetx,
			y: resety,
			radians: rad(315),
			velocity: 5
		};

	function sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

	function rad(x) {
    	return (x % 360) * (Math.PI / 180);
	}

	function toDegre(x) {
		return (x / Math.PI) * 180;
	}

	function newBallPosition() {
		ball.x += ball.velocity * Math.cos(ball.radians);
		ball.y += ball.velocity * Math.sin(ball.radians);
		if (ball.x < leftShift || ball.x > leftShift + 800) {
		// Reflect horizontally
			if(ball.x < leftShift) {
				scoreB += 1;
				ball.x = leftShift + 735;
			}
			else {
				scoreA += 1;
				ball.x = leftShift + 45;
			}
			ball.y = resety;
			ball.velocity = 5;
		}

		if ( (ball.y > paddleAy && ball.y < paddleAy + paddleSize ) 
		&& (ball.x > paddleAx - 10 && ball.x < paddleAx + 10)) {
			
			if(ball.y > paddleAy + 75)
				ball.radians = rad(45);
			else if (ball.y < paddleAy + 25)
				ball.radians = rad(315);
			else
				ball.radians = Math.PI - ball.radians;
			if(ball.velocity < 10)
				ball.velocity += 0.25;
		}
	
		if ( (ball.y > paddleBy && ball.y < paddleBy + paddleSize ) 
		&& (ball.x > paddleBx - 10 && ball.x < paddleBx + 10)) {
			if(ball.y > paddleBy + 75)
				ball.radians = rad(135);
			else if (ball.y < paddleBy + 25)
				ball.radians = rad(225);
			else
				ball.radians = Math.PI - ball.radians;

			if(ball.velocity < 10)
				ball.velocity += 0.25;
		}

		if (ball.y <= topWall || ball.y >= botWall) {
			ball.radians = -ball.radians;
			console.log("HIT X");
		}
		//TO DO, add hitbox upper e lower paddle, more on hit pedal angles
	}

	async function gameloop() {
		while(1) {
			if(scoreA > 10 || scoreB > 10) {
				scoreA = 0;
				scoreB = 0;
			}
			newBallPosition();
			if(ball.y >= 570)
				paddleBy = 520
			else if(ball.y <= 70)
				paddleBy = 20
			else
				paddleBy = ball.y - 50; //BOT IMPLEMENTATION
			await sleep(10);
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
			}, 15); // Adjust the interval as needed for desired speed
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
	}
	// Attach keydown and keyup event listeners to the document
	document.addEventListener('keydown', handleKeyDown);
	document.addEventListener('keyup', handleKeyUp);
</script>
