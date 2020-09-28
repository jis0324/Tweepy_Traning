import os
import tweepy
import csv
import json
import time
import traceback

base_dir = os.path.dirname(os.path.abspath(__file__))
output_json_path = base_dir + '/output/result.json'
secrets = json.loads(open(path + 'secrets.json').read())
consumer_key = ecrets['api_key']
consumer_secret = secrets['api_secret_key']
access_token = secrets['access_token']
access_token_secret = secrets['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class Profile:
  # init
  def __init__(self):
    self.users_list = list()
    self.get_users_list()

  # get users list
  def get_users_list(self):
    users_list_file = "{}/userlist.txt".format(base_dir)
    if os.path.isfile(users_list_file):
      with open(users_list_file, 'r') as users_list_txt:
        self.users_list=[row.rstrip('\n') for row in users_list_txt]
    else:
      print("----- Not Fount userlists.txt File -----")

   # insert profile to csv
  def insert_to_json(self, profile_dict):
    print(profile_dict)
    with open(output_json_path, "a") as f:
      f.write(json.dumps(profile_dict))

  # get follower data
  def get_follower_data(self, follower_id):
    try:
      follower = api.get_user(follower_id)
      follower_dict = dict()
      follower_dict["user_id"] = follower.id_str
      follower_dict["status_id"] = ""
      follower_dict["created_at"] = str(follower.created_at)
      follower_dict["screen_name"] = follower.screen_name
      follower_dict["name"] = follower.name
      follower_dict["location"] = follower.location
      follower_dict["description"] = follower.description
      follower_dict["url"] = follower.url
      follower_dict["protected"] = follower.protected
      follower_dict["followers_count"] = follower.followers_count
      follower_dict["friends_count"] = follower.followers_count
      follower_dict["listed_count"] = follower.listed_count
      follower_dict["statuses_count"] = follower.statuses_count
      follower_dict["favourites_count"] = follower.favourites_count
      follower_dict["account_created_at"] = str(follower.created_at)
      follower_dict["verified"] = follower.verified
      follower_dict["profile_url"] = ""
      follower_dict["profile_expanded_url"] = ""
      if "url" in follower.entities:
        if "urls" in follower.entities["url"] and follower.entities["url"]["urls"]:
          if "url" in follower.entities["url"]["urls"][0]:
            follower_dict["profile_url"] = follower.entities["url"]["urls"][0]["url"]
          if "expanded_url" in follower.entities["url"]["urls"][0]:
            follower_dict["profile_expanded_url"] = follower.entities["url"]["urls"][0]["expanded_url"]

      follower_dict["account_lang"] = follower.lang
      follower_dict["profile_banner_url"] = follower.profile_banner_url
      follower_dict["profile_background_url"] = follower.profile_background_image_url
      follower_dict["profile_image_url"] = follower.profile_image_url

      return follower_dict
    except:
      return None

  # get profile of user
  def get_user_profile(self, username):
    try:
      user = api.get_user(username)

      profile_dict = dict()
      profile_dict["user_id"] = user.id_str
      profile_dict["status_id"] = ""
      profile_dict["created_at"] = str(user.created_at)
      profile_dict["screen_name"] = user.screen_name
      profile_dict["name"] = user.name
      profile_dict["location"] = user.location
      profile_dict["description"] = user.description
      profile_dict["url"] = user.url
      profile_dict["protected"] = user.protected
      profile_dict["followers_count"] = user.followers_count
      profile_dict["friends_count"] = user.followers_count
      profile_dict["listed_count"] = user.listed_count
      profile_dict["statuses_count"] = user.statuses_count
      profile_dict["favourites_count"] = user.favourites_count
      profile_dict["account_created_at"] = str(user.created_at)
      profile_dict["verified"] = user.verified
      profile_dict["profile_url"] = ""
      profile_dict["profile_expanded_url"] = ""
      if "url" in user.entities:
        if "urls" in user.entities["url"] and user.entities["url"]["urls"]:
          if "url" in user.entities["url"]["urls"][0]:
            profile_dict["profile_url"] = user.entities["url"]["urls"][0]["url"]
          if "expanded_url" in user.entities["url"]["urls"][0]:
            profile_dict["profile_expanded_url"] = user.entities["url"]["urls"][0]["expanded_url"]

      profile_dict["account_lang"] = user.lang
      profile_dict["profile_banner_url"] = user.profile_banner_url
      profile_dict["profile_background_url"] = user.profile_background_image_url
      profile_dict["profile_image_url"] = user.profile_image_url

      profile_dict["followers"] = dict()
      follower_ids = []
      for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
        follower_ids.extend(page)
        # time.sleep(60)

      for index, follower_id in enumerate(follower_ids):
        try:
          print("{}th Follower / Total {} Followers Of {}".format(index + 1, profile_dict["followers_count"], username))
          if str(follower_id) not in profile_dict["followers"]:
            follower_data = self.get_follower_data(follower_id)
            profile_dict["followers"][str(follower_id)] = follower_data
        except:
          print(traceback.print_exc())
          continue

      print(json.dumps(profile_dict, indent=2))
      return profile_dict
    except:
      print(traceback.print_exc())
      return None

  # main
  def main(self):
    if self.users_list:
      for index, username in enumerate(self.users_list):
        try:
          print("{}th User / Total {} Users : {}".format(index+1, len(self.users_list), username))
          profile_dict = self.get_user_profile(username)
          if profile_dict:
            self.insert_to_json(profile_dict)
        except:
          print(traceback.print_exc())
          continue

    else:
      print("----- Empty Users List, Please Fill Out Users and Try again. -----")
      return

if __name__ == '__main__':
  # delete output csv
  if os.path.isfile(output_json_path):
    os.remove(output_json_path)

  profile = Profile()
  profile.main()