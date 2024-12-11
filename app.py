from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Diccionario para almacenar usuarios y sus IPs
users = {}

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    user_ip = request.remote_addr  # Obtener IP del usuario
    users[request.sid] = user_ip  # Asociar IP al SID del cliente
    print(f"Usuario conectado desde IP: {user_ip}")

@socketio.on('disconnect')
def handle_disconnect():
    user_ip = users.pop(request.sid, 'Desconocido')
    print(f"Usuario desconectado desde IP: {user_ip}")

@socketio.on('send_message')
def handle_message(data):
    user_ip = users.get(request.sid, 'Desconocido')
    message = data['message']
    time = datetime.now().strftime('%H:%M:%S')
    # Enviar mensaje con IP del usuario y hora
    emit('receive_message', {'message': message, 'user_ip': user_ip, 'time': time}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='192.168.80.30', port=5000, debug=True)
