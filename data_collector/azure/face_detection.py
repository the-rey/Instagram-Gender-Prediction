#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "2915e337b58d495f9f85bab8ab2f052c"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

def getFaceAttributes(image_url):
    # Set image_url to the URL of an image that you want to analyze.
    
    faceAttributes = []

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    data = {'url': image_url}
    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    faces = response.json()
    # Display the original image and overlay it with the face information.

    temp = {}
    for face in faces:
        try:
            #print(face['faceAttributes']['gender']+" - "+ str(face['faceAttributes']['age']))
            temp.update({'gender':face['faceAttributes']['gender']})
            temp.update({'age':face['faceAttributes']['age']})
            #print(temp)
            faceAttributes.append(temp)
        except:
            break

    print("Face(s) in frame : "+ str(len(faceAttributes)))

    if(len(faceAttributes) == 1):
        return faceAttributes

    return False