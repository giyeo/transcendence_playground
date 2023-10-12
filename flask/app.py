from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key of your choice
socketio = SocketIO(app)

# Create a route to render an HTML page (this is where your Svelte component will be)
@app.route('/')
def index():
    return render_template('index.html')

# Define a SocketIO event to receive and broadcast messages
@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
