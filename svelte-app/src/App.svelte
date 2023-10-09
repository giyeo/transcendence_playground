<!-- App.svelte -->
<div class="paddle"			style="top: {rect1Y}px;	left: {leftShift + 35}px;"></div>
<div class="paddle"			style="top: {rect2Y}px;	left: {leftShift + 745}px;"></div>

<div class="ball"			style="top: {ballY}px;	left: {ballX}px;"></div>

<div class="horizontalWall" style="top: {0}px;		left: {leftShift + 0}px;"></div>
<div class="horizontalWall" style="top: {310}px;	left: {leftShift + 0}px; background-color: rgba(200,200,200,0.2);"></div>
<div class="horizontalWall" style="top: {620}px;	left: {leftShift + 0}px;"></div>

<div class="verticalWall"	style="top: {20}px;		left: {leftShift + 390}px;"></div>

<div class="score"			style="top: {60}px;		left: {leftShift + 250}px;">0</div>
<div class="score"			style="top: {60}px;		left: {leftShift + 460}px;">0</div>

<div class="info"			style="top: {650}px;	left: {leftShift + 0}px;">800x600px object width 20px, paddle 100px</div>

<!-- <div>
	<Socket />
</div> -->

<script lang="ts">
	// Import the Socket.IO client library
	import Socket from './Socket.svelte';

	let leftShift = 400;
	let rect1Y = 20 + 300 - 50;
	let rect2Y = 20 + 300 - 50;
	let ballY = 300 + 10;
	let ballX = 400 - 10 + leftShift;
	let keyDownInterval = null;
	let isKeyDown = false; // Flag to track key press

	//800px x 600px  
	function startContinuousMove(direction) {
		if (!isKeyDown) {
			isKeyDown = true;
			keyDownInterval = setInterval(() => {
				if (direction === 'up' && rect1Y >= 30) {
					rect1Y -= 10; // Move rectangle 1 upward
					rect2Y -= 10;
					ballX -= 10 * 4/3;
					ballY -= 10;
				} else if (direction === 'down' && rect1Y < 520) {
					rect1Y += 10; // Move rectangle 2 downward
					rect2Y += 10;
					ballX += 10 * 4/3;
					ballY += 10;
				}
			}, 20); // Adjust the interval as needed for desired speed
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
