#!/usr/bin/env python
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import json
import datetime
from user_handler import getAge, getGender
import _pickle as pickle
import parameter as param

all_comments = {}

def saveComments(username):

    print("saving comments for "+username)
        
    if username not in all_comments:
        print("data not found")
        return 

    print("data found")
    print("number of comments: " +str(len(all_comments[username])))

    data = {}
    
    data['comments']=all_comments[username]
    data['user']=username
    data['age']=str(getAge(username))
    data['gender']=str(getGender(username))

    #focus cari cowo
    if data['gender'] != 'male':
        return

    with open('comments/'+'comments '+ username+'('+str(getAge(username))+', '+str(getGender(username))+')' + '.json', 'w') as fp:
        json.dump(data, fp)

    new_comment = json.load(open('comments/'+'comments '+ username+'('+str(getAge(username))+', '+str(getGender(username))+')' + '.json', 'r'))
    print("reading data for : " + new_comment['user'] + " " + new_comment['age'] + " " + new_comment['gender'])
    for index, comment in enumerate(new_comment['comments']):
        try:
            print(index +". "+comment['user']['username'] + " : " + comment['text'])
        except:
            comment

    print("number of comments read: " +str(len(new_comment['comments'])))

def getComments(API, username, media_id):
    
    if(not media_id): 
        print("media_id not found")
        return False

    print("getting comments")

    if(not (username in all_comments)):
        print("buat baru")
        all_comments[username] = []

    #API.getUsernameInfo()
    has_more_comments = True
    max_id = ''

    flag = True

    while has_more_comments and flag:
        _ = API.getMediaComments(media_id, max_id=max_id)
        # comments' page come from older to newer, lets preserve desc order in full list
        try:
            for c in reversed(API.LastJson['comments']):
                all_comments[username].append(c)
                if len(all_comments[username]) > 500:
                    flag = False
                
        except:
            print(API.LastJson)
            
        has_more_comments = API.LastJson.get('has_more_comments', False)
        
        if has_more_comments:
            max_id = API.LastJson.get('next_max_id', '')
            time.sleep(2)

    print("number of comments: " +str(len(all_comments[username])))

    