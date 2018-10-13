#!/usr/bin/env python
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import json
import datetime
from user_handler import getAge, getGender

all_comments = {}

def saveComments(username):

    print("saving comments for "+username)

    try:
        import cPickle as pickle
    except ImportError:  
        return
        
    if(not(username in all_comments)):
        print("data not found")
        return 

    print("data found")
    print("number of comments: " +str(len(all_comments[username])))
        

    with open('comments/'+'comments '+ username+'('+str(getAge(username))+', '+str(getGender(username))+')' + '.p', 'wb') as fp:

        pickle.dump(all_comments[username], fp, protocol=pickle.HIGHEST_PROTOCOL)

    new_comment = pickle.load(open('comments/'+'comments '+ username+'('+str(getAge(username))+', '+str(getGender(username))+')' + '.p', 'rb'))
    for index, comment in enumerate(new_comment):
        try:
            print(index +". "+comment['user']['username'] + " : " + comment['text'])
        except:
            comment

    print("number of comments: " +str(len(new_comment)))

def getComments(API, username, media_id):
    
    if(not media_id): 
        print("media_id not found")
        return False

    now = datetime.datetime.now()
    print(now)
    print("getting comments")
    # stop conditions, the script will end when first of them will be true
    count = 30

    if(not (username in all_comments)):
        print("buat baru")
        all_comments[username] = []

    #API.getUsernameInfo()
    has_more_comments = True
    max_id = ''

    while has_more_comments:
        _ = API.getMediaComments(media_id, max_id=max_id)
        # comments' page come from older to newer, lets preserve desc order in full list
        try:
            for c in reversed(API.LastJson['comments']):
                all_comments[username].append(c)
                
        except:
            print(API.LastJson)
            
        has_more_comments = API.LastJson.get('has_more_comments', False)
        
        if has_more_comments:
            max_id = API.LastJson.get('next_max_id', '')
            time.sleep(2)

    print("number of comments: " +str(len(all_comments[username])))

    