from pymongo import MongoClient, DESCENDING
from werkzeug.security import generate_password_hash
from user import User

client = MongoClient(
    "mongodb+srv://chatdb:jobsity@cluster0.jdq0d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")


def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one(
        {'_id': username, 'email': email, 'password': password_hash})

def get_user(user):
	user_data = users_collection.find_one({'_id': user})
	if user_data:
		user_data_output = User(user_data['_id'], user_data['email'], user_data['password'])
		return user_data_output
	return None

if __name__ == '__main__':
    save_user('testname', 'test@test.com', "testpassword")
