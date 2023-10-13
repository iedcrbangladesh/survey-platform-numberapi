import mysql.connector
import pymongo
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os
load_dotenv()


MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_DB = os.environ["MYSQL_DB"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]


cnx = mysql.connector.connect(
	user=MYSQL_USER,
	password=MYSQL_PASSWORD,
	host=MYSQL_HOST,
	port=MYSQL_PORT,
	database=MYSQL_DB
)

cursor = cnx.cursor()
def request_number_for_user():
	query = ("SELECT id,mobile_number from contacts where request_served=0 LIMIT 1")
	cursor.execute(query)
	row = cursor.fetchone()
	if(row):
		return (row[0], row[1])
	else:
		return None

def lock_mobile_number_for_user(user_id, id):
	query = ("UPDATE contacts set request_served=1, request_user=%s where id=%s ")
	val_data =  (user_id, id)
	cursor.execute(query,val_data)
	cnx.commit()


	return cursor.rowcount



MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = os.environ["MONGO_PORT"]
MONGO_USER = os.environ["MONGO_USER"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_URI = os.environ["MONGO_URI"]

#print(MONGO_PORT)
#exit()
''''
myclient = pymongo.MongoClient(
    host = f"{MONGO_HOST}:{MONGO_PORT}",
    username=MONGO_USER,
    password=MONGO_PASSWORD
)
'''
myclient = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))

mydb = myclient["question-data"]

try:
    myclient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def my_col(name):
    return mydb[name]