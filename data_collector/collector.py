#!/usr/bin/env python
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
def get_all_followers_comments(username): # Ini yang bakal dipanggil si thanos
    all_follower_comments = []
    followers = get_followers(username)

    for follower in followers:
        follower_comments = []

        all_media_id = get_all_media_id(follower)
        for media_id in all_media_id:
            media_comments = get_media_comments(media_id)

             # semua komen dari semua medianya gabung jadi 1 list
            follower_comments.extend(media_comments)

        # lalu append list ke sini, jadi bentuknya list of list
        # jd tiap list di dalam list ini represents list of comments dari 1 follower
        all_follower_comments.append(follower_comments)

    return all_follower_comments

# Returns list of followers of "username"
def get_followers(username):
    followers = []

    # TODO
    # followers.append(...)

    return followers

# Returns list of media id of a username
def get_all_media_id(username):
    all_media_id = []

    # TODO get all media id of a user
    # all_media_id.append(...)

    return all_media_id

def get_media_comments(media_id):
    media_comments = []

    # TODO get comments of a media
    # media_comments.append(...)

    return media_comments
