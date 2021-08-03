from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_login import LoginManager, login_manager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager() 
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatroom')
def chatroom():
    user = request.args.get('user')
    room = request.args.get('room')
    if user and room:
        try:
            room = int(room)
            return render_template('chatroom.html', user=user, room=room)
        except:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@socketio.on('send_message')
def handle_message(data):
    user = data['user']
    room = data['room']
    message = data['message']
    app.logger.info('{} has send a message to the room {}: {}'.format(user, room, message))
    socketio.emit('receive_message', data, room=room)


@socketio.on('join_room')
def on_join(data):
    user = data['user']
    room = data['room']
    app.logger.info('{} has join to room {}'.format(user, room))
    join_room(room)
    socketio.emit('join_room_message', data)

@socketio.on('leave_room')
def on_leave(data):
    user = data['user']
    room = data['room']
    app.logger.info('{} has left room {}'.format(user, room))
    leave_room(room)
    socketio.emit('leave_room_message', data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
