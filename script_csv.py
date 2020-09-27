
import os
import tweepy
import csv
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
output_csv_path = base_dir + '/result.csv'

consumer_key = ""
consumer_secret = ""
access_token = "-6PfKl38gPSLljpGWMjmRdFXpn5q8Sv"
access_token_secret = ""

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
  def insert_to_csv(self, profile_dict):
    file_exist = os.path.isfile(output_csv_path)
    with open(output_csv_path, "a", newline="") as f:
      fieldnames = ["user_id", "status_id", "created_at", "screen_name", "name", "location", "description", "url", "protected", "followers_count", "friends_count", "listed_count", "statuses_count", "favourites_count", "account_created_at", "verified", "profile_url", "profile_expanded_url", "account_lang", "profile_banner_url", "profile_background_url", "profile_image_url"]
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      if not file_exist:
        writer.writeheader()
      writer.writerow(profile_dict)

  # get profile of user
  def get_user_profile(self, username):
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

    print(json.dumps(profile_dict, indent=2))
    return profile_dict

  # main
  def main(self):
    if self.users_list:
      for index, username in enumerate(self.users_list):
        print("{}th User / Total {} Users : {}".format(index+1, len(self.users_list), username))
        profile_dict = self.get_user_profile(username)
        self.insert_to_csv(profile_dict)

    else:
      print("----- Empty Users List, Please Fill Out Users and Try again. -----")
      return

if __name__ == '__main__':
  # delete output csv
  if os.path.isfile(output_csv_path):
    os.remove(output_csv_path)

  profile = Profile()
  profile.main()