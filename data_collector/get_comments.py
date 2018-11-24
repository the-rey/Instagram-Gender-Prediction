#!/usr/bin/env python
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import json
import datetime
from user_handler import getAge, getGender
import _pickle as pickle
from naive_bayes import naive_bayes
from statistics import mode

all_comments = []

def classify_nb(comments):

    result = []
    for text in comments:
        result.append(naive_bayes.naive_bayes_classify_from_text(naive_bayes.load_model(),text))
    return mode(result)

def getComments(API, media_id):
    
    if(not media_id): 
        print("media_id not found")
        return False

    print("getting comments")

    has_more_comments = True
    max_id = ''

    flag = True

    while has_more_comments and flag:
        _ = API.getMediaComments(media_id, max_id=max_id)
        # comments' page come from older to newer, lets preserve desc order in full list
        try:
            for c in reversed(API.LastJson['comments']):
                all_comments.append(c)
                if len(all_comments) > 500:
                    flag = False
                
        except:
            print(API.LastJson)
            
        has_more_comments = API.LastJson.get('has_more_comments', False)
        
        if has_more_comments:
            max_id = API.LastJson.get('next_max_id', '')
            time.sleep(1)


    print("number of comments: " +str(len(all_comments)))

    return(all_comments)

