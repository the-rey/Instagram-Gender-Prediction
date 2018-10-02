from InstagramAPI import InstagramAPI 
import urllib
from get_media import getUsersPictures
from azure.face_detection import getFaceAttributes
from parameter import getPassword, getUsername

def getTotalFollowers(api, user_id):
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

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def getTotalFollowing(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowing from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

username = getUsername()
password = getPassword()
targetUsername = 'reynaldonathanael'

API = InstagramAPI(username, password)
API.login()

#your own id
#userId = API.username_id

#get other users' id
API.searchUsername(targetUsername)
userId = TargetUserId = (API.LastJson["user"]["pk"])

#get followers
followers = getTotalFollowers(API, userId)

#get followings
followers = getTotalFollowing(API, userId)
#followers.reverse()
print("getting followers")

#print followers id if user is public
for index, follower in enumerate(followers):
    #if(follower['is_private'] == False): 
    print(follower['username'])
    getUsersPictures(API, follower['username'])

    #if(index >= 70): break