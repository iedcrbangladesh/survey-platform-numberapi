import os
from flask import Flask,request,jsonify, json
from flask_cors import CORS, cross_origin
from app import app
from db import *
from bson.objectid import ObjectId
from datetime import datetime
import time


@app.route("/numapi/getmobilenumber", methods=['POST'])
async def getmobilenumber():
   if request.method == 'POST':
        data = json.loads(request.data)
        user_id = data['userid']
        
        mobile_no = None
        lock_count = 0
        mobile_data = None

        contactquery = {
          'user_id':ObjectId(user_id),
          'status':0
        }
        user_contact = my_col('user_contact').find_one(contactquery)
        #user_contact_count=my_col('user_contact').count_documents(contactquery)
        #print(user_contact_count)
        if(user_contact):
           mobile_no =  user_contact['mobile_no']
        
        if(user_contact == None):
            mobile_data = request_number_for_user()
            print(str(mobile_data))
            if(mobile_data != None):
                uci = my_col('user_contact').insert_one({
                    'user_id':ObjectId(user_id),
                    'status':0,
                    'dispose_status':None,
                    'created_at':datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                id = uci.inserted_id
                mobile_no = mobile_data[1]
                lock_count = lock_mobile_number_for_user(user_id,mobile_data[0])
                if(lock_count > 0):
                    newvalues = { "$set": { "mobile_no": mobile_no } }
                    myquery = {"_id":id}
                    my_col('user_contact').update_one(myquery, newvalues)

            

        return({
            'userid':user_id,
            'mobile_no':mobile_no        	
            
        })
