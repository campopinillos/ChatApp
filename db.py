from pymongo import MongoClient, DESCENDING
from werkzeug.security import generate_password_hash
from user import User
from bson import ObjectId
import datetime as dt

client = MongoClient(
    "mongodb+srv://chatdb:jobsity@cluster0.jdq0d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
messages_collection = chat_db.get_collection("messages")


def save_user(user, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one(
        {'_id': user, 'email': email, 'password': password_hash})

def get_user(user):
	user_data = users_collection.find_one({'_id': user})
	if user_data:
		user_data_output = User(user_data['_id'], user_data['email'], user_data['password'])
		return user_data_output
	return None

def save_message(room_id, sender, text):
    messages_collection.insert_one({'room_id': room_id, 'sender': sender, 'text': text, 'created_at': dt.datetime.now()})

MESSAGE_FETCH_LIMIT = 50

def get_messages(room_id):
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(MESSAGE_FETCH_LIMIT).skip(0))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages[::-1]

if __name__ == '__main__':
    # save_user('testname', 'test@test.com', "testpassword") # test for new user
    print(get_messages("1")) # test for get messages 
    # print(get_user("test")) # test for get user
