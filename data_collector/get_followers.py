from InstagramAPI import InstagramAPI
import urllib
from get_media import getUsersPictures
from azure.face_detection import getFaceAttributes
from parameter import get_password, get_username, get_target_username
import argparse


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


def collect_data(args, targetUsername):
    username = args.username
    password = args.password

    API = InstagramAPI(username, password)
    API.login()

    # get other users' id
    API.searchUsername(targetUsername)
    TargetUserId = (API.LastJson["user"]["pk"])

    # get followings
    followers = getTotalFollowers(API, TargetUserId)
    followers.reverse()

    print("getting followers")

    # print followers id if user is public

    for index, follower in enumerate(followers):
        try:
            if(follower['is_private'] == False):
                print(follower['username'])
                getUsersPictures(API, follower['username'])
        except:
            print("error when collecting data for " + follower['username'])


def main(args):

    targets = get_target_username()

    for targetUsername in targets:
        print("target : " + targetUsername)
        collect_data(args, targetUsername)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # Access Key
    parser.add_argument("username", help="insert instagram username")
    parser.add_argument("password", help="insert instagram password")

    args = parser.parse_args()
    main(args)
