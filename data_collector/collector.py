#!/usr/bin/env python
import time
# -*- coding: utf-8 -*-

# si data_collector ini terima input username trs return komentar follower2 aja
# dalam bentuk :
# [
#   ["komen1", "komen2", ...],  <-- follower 1
#   ["komen1", "komen2", ...]   <-- follower 2
#   ["komen1", "komen2", ...]   <-- follower 3
#    ...
# ]
# ntar si thanos yang proses smua pake classifier yang dipilih user

# Returns commments of a username
def get_all_followers_comments(username, api): # Ini yang bakal dipanggil si thanos, berati InstagramAPI harus di initiate di thanos
    all_follower_comments = []
    followers = get_followers(username,api)

    for follower in followers:
        follower_comments = []

        all_media_id = get_all_media_id(follower,api)
        for media_id in all_media_id:
            media_comments = get_media_comments(media_id,api)

             # semua komen dari semua medianya gabung jadi 1 list
            follower_comments.extend(media_comments)

        # lalu append list ke sini, jadi bentuknya list of list
        # jd tiap list di dalam list ini represents list of comments dari 1 follower
        all_follower_comments.append(follower_comments)

    return all_follower_comments

# Returns list of followers of "username"
def get_followers(username,api):
    followers = []

    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(username, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

# Returns list of media id of a username
def get_all_media_id(username,api):

    all_media_id = []
    # TODO get all media id of a user
    # all_media_id.append(...)

    api.searchUsername(username)
    user_id = (api.LastJson["user"]["pk"])
    api.getUserFeed(user_id)

    # get response json and assignment value to MediaList Variable
    # dict type data 
    mediaList = api.LastJson 

    for media in mediaList['items']:
        all_media_id.append(media['id'])

    return all_media_id

def get_media_comments(media_id,api):
    media_comments = []
    LIMIT = 500

    # TODO get comments of a media
    # media_comments.append(...)

    if(not media_id): 
        print("media_id not found")
        return False

    has_more_comments = True
    max_id = ''

    flag = True

    while has_more_comments and flag:
        _ = api.getMediaComments(media_id, max_id=max_id)
        # comments' page come from older to newer, lets preserve desc order in full list
        try:
            for c in reversed(api.LastJson['comments']):
                media_comments.append(c)
                if len(media_comments) > LIMIT:
                    flag = False
                
        except:
            print(api.LastJson)
            
        has_more_comments = api.LastJson.get('has_more_comments', False)
        
        if has_more_comments:
            max_id = api.LastJson.get('next_max_id', '')
            time.sleep(1)

    return media_comments
