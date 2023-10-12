<!-- Chat.svelte -->
<script>
	import { onMount } from 'svelte';
	import io from 'socket.io-client';
  
	let messages = [];
	let message = '';
  
	const socket = io('http://localhost:5000'); // Replace with your Socket.IO server URL
  
	socket.on('message', (data) => {
	  messages = [...messages, data];
	});
  
	const sendMessage = () => {
	  if (message) {
		socket.emit('message', message);
		message = '';
	  }
	};
  
	onMount(() => {
	  socket.emit('join', 'User has joined the chat');
	});
  </script>
  
  <div>
	<ul>
	  {#each messages as msg (msg.id)}
		<li>{msg}</li>
	  {/each}
	</ul>
  
	<input bind:value={message} on:input={e => message = e.target.value} />
	<button on:click={sendMessage}>Send</button>
  </div>
  