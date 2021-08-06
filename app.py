"""Flask Web Financial Chat Application """

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from db import get_user, save_user, save_message, get_messages
from pymongo.errors import DuplicateKeyError
import datetime as dt
from bot import bot_answer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    message = ''
    if current_user.is_authenticated:
        message = 'Join or create a new room by a number.'
        return render_template('index.html', user=current_user.user, message=message)
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    status = ''
    if request.method == 'POST':
        user_login = request.form.get('user')
        password_login = request.form.get('password')
        check_user = get_user(user_login)
        if check_user and check_user.unhash_password(password_login):
            login_user(check_user)
            return redirect(url_for('index'))
        else:
            status = "Login error, user does not exist or password is incorrect."
    return render_template('login.html', message=status)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    status = ''
    if request.method == 'POST':
        user_signup = request.form.get('user')
        email_signup = request.form.get('email')
        password_signup = request.form.get('password')
        try:
            save_user(user_signup, email_signup, password_signup)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            status = "User already exists."
    return render_template('signup.html', message=status)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user):
    return get_user(user)


@app.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
    user = request.args.get('user')
    room = request.args.get('room')
    if user and room:
        try:
            room = int(room)
            if len(get_messages(str(room))) > 0:
                messages = get_messages(str(room))
            else:
                messages = ""
            return render_template('chatroom.html', user=user, room=room, messages=messages)
        except:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@socketio.on('send_message')
def handle_message(data):
    user = data['user']
    room = data['room']
    message = data['message']
    data['created_at'] = dt.datetime.now().strftime("%d %b, %H:%M")
    app.logger.info(
        '{} has send a message to the room {}: {}'.format(user, room, message))
    socketio.emit('receive_message', data, room=room)
    if data['message'].startswith('/stock='):
        stock_code = data['message'].split('=')[1]
        bot_message = {}
        bot_message["message"] = bot_answer(stock_code)
        bot_message["created_at"] = dt.datetime.now().strftime("%d %b, %H:%M")
        app.logger.info('Bot has send a message to the room {}: {}'.format(
            room, bot_message["message"]))
        socketio.emit('bot_message_response', data=bot_message, room=room)
    else:
        save_message(data['room'], data['user'], data['message'])


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
