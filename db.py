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
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")

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

def save_room(room_number, created_by):
    room_id = rooms_collection.insert_one(
        {'room_number': room_number, 'created_by': created_by, 'created_at': dt.datetime.now()}).inserted_id
    add_room_member(room_id, room_number, created_by, created_by, is_room_admin=True)
    return room_id

def add_room_member(room_id, room_name, user, added_by, is_room_admin=False):
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'user': user}, 'room_name': room_name, 'added_by': added_by,
         'added_at': dt.datetime.now(), 'is_room_admin': is_room_admin})

def get_room_members(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))

def get_rooms_for_user(user):
    return list(room_members_collection.find({'_id.user': user}))

def is_room_member(room_id, user):
    return room_members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'user': user}})

def is_room_admin(room_id, user):
    return room_members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'user': user}, 'is_room_admin': True})

MESSAGE_FETCH_LIMIT = 3

def get_messages(room_id, page=0):
    offset = page * MESSAGE_FETCH_LIMIT
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(MESSAGE_FETCH_LIMIT).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages[::-1]


if __name__ == '__main__':
    save_user('testname', 'test@test.com', "testpassword") #prueba
