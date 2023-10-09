<script>
	import { onMount } from 'svelte';
	import io from 'socket.io-client';
  
	let socket;
  
	// Define a variable to store incoming messages
	let messages = [];
  
	// Initialize the WebSocket connection
	onMount(() => {
	  socket = io('http://localhost:3000'); // Replace with your server URL
  
	  // Handle incoming messages from the server
	  socket.on('message', (message) => {
		messages = [...messages, message]; // Add the message to the messages array
	  });
	});
  
	// Function to send a message to the server
	function sendMessage() {
	  const messageText = 'Hello, server!';
	  socket.emit('message', messageText);
	}
  </script>
  
  <style>
	/* Your component styles */
  </style>
  
  <div>
	<h1>WebSocket Chat</h1>
  
	<!-- Display incoming messages -->
	<ul>
	  {#each messages as message (message.id)}
		<li>{message}</li>
	  {/each}
	</ul>
  
	<!-- Button to send a message -->
	<button on:click={sendMessage}>Send Message</button>
  </div>
  