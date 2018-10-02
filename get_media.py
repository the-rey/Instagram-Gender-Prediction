#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.face_detection import getFaceAttributes
import urllib

# get Self user feed 
#API.getSelfUserFeed()


#get other user's feed
def getUsersPictures(API, targetUsername):
    
    API.searchUsername(targetUsername)
    user_id = (API.LastJson["user"]["pk"])
    profile_picture_url = API.LastJson["user"]["profile_pic_url"]

    save(profile_picture_url, targetUsername,"pp")

    API.getUserFeed(user_id)
    # get response json and assignment value to MediaList Variable
    # dict type data 
    mediaList = API.LastJson 
    # get all the pictures
    i=0
    for media in mediaList['items']:
        # mediaID = media['id']
        # mediaType = media['media_type']
        try:
            mediaCandidates = media['image_versions2']['candidates'][0]
           
        except:
            try:
                #mediaCandidates = media['carousel_media']['image_versions2']['candidates'][0]
                mediaCandidates = media['carousel_media'][0]['image_versions2']['candidates'][0]
            except:
                print("break")
                break

        mediaUrl = mediaCandidates['url']
        mediaUrl = mediaUrl[:-(len(mediaUrl) - mediaUrl.rfind("?"))]
        
        i+=1
        
        save(mediaUrl, targetUsername,str(i))
        if(i>7): 
            break


def save(mediaUrl, targetUsername, comment):
    faceAttributes = getFaceAttributes(mediaUrl)
    print(faceAttributes)
    if(faceAttributes):
        filename = targetUsername + " - " + comment + " - age " + str(int(faceAttributes[0]['age'])) + " gender "+faceAttributes[0]['gender']+ ".jpg"
        urllib.request.urlretrieve(mediaUrl, "pictures/" + filename)


