#!/usr/bin/env python
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import json
import datetime

def saveComments(API, username, media_id, number = ""):
    
    if(not media_id): 
        print("media_id not found")
        media_id = '1878064985478018349'

    now = datetime.datetime.now()
    print(now)
    print("getting comments")
    # stop conditions, the script will end when first of them will be true
    count = 25

    #API.getUsernameInfo()
    has_more_comments = True
    max_id = ''
    comments = []

    while has_more_comments:
        _ = API.getMediaComments(media_id, max_id=max_id)
        # comments' page come from older to newer, lets preserve desc order in full list
        for c in reversed(API.LastJson['comments']):
            comments.append(c)
            
        has_more_comments = API.LastJson.get('has_more_comments', False)
        # evaluate stop conditions
        if count and len(comments) >= count:
            comments = comments[:count]
            # stop loop
            has_more_comments = False
            print("stopped by count")
        # if until_date:
        #     older_comment = comments[-1]
        #     dt = datetime.datetime.utcfromtimestamp(older_comment.get('created_at_utc', 0))
        #     print(dt)
        #     # only check all records if the last is older than stop condition
        #     if dt <= until_date:
        #         print(True)
        #         # keep comments after until_date
        #         comments = [
        #             c
        #             for c in comments
        #             if datetime.datetime.utcfromtimestamp(c.get('created_at_utc', 0)) > until_date
        #         ]
        #         # stop loop
        #         has_more_comments = False
        #         print("stopped by until_date")
        # # next page
        if has_more_comments:
            max_id = API.LastJson.get('next_max_id', '')
            time.sleep(2)

    try:
        import cPickle as pickle
    except ImportError:  
        import pickle

    
    with open('comments/'+'comments '+ username + '(' + str(number) +').p', 'wb') as fp:
        pickle.dump(comments, fp, protocol=pickle.HIGHEST_PROTOCOL)

    new_comment = pickle.load(open('comments/'+'comments '+ username + '(' + str(number) +').p', 'rb'))
    for comment in new_comment:
        try:
            print(comment['user']['username'] + " : " + comment['text'])
        except:
            comment