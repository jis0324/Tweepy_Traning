import os
import tweepy
import csv
import json
import traceback
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
output_csv_path = base_dir + '/output/result.csv'
secrets = json.loads(open(base_dir + '/secrets.json').read())
consumer_key = secrets['api_key']
consumer_secret = secrets['api_secret_key']
access_token = secrets['access_token']
access_token_secret = secrets['access_token_secret']

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class Followers:
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
  
  # insert follower data to csv
  def insert_to_csv(self, follower_dict):
    file_exist = os.path.isfile(output_csv_path)
    with open(output_csv_path, "a", encoding="latin1", errors="ignore", newline="") as f:
      fieldnames = ["whose_follower", "user_id", "screen_name", "name", "location", "description", "url", "protected", "followers_count", "friends_count", "listed_count", "statuses_count", "favourites_count", "account_created_at", "verified", "profile_url", "profile_expanded_url", "account_lang", "profile_banner_url", "profile_background_url", "profile_image_url"]
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      if not file_exist:
        writer.writeheader()
      writer.writerow(follower_dict)

  # get profile of user
  def get_followers_data(self, username):
  # try with user_lookup

  # try with itmes
    # try:
    #   print("Finding followers of {}...".format(username))
    #   users = tweepy.Cursor(api.followers, screen_name=username).items()
          
    #   i = 0
    #   while True:
    #     try:
    #       user = next(users)
    #       time.sleep(4)
    #     except tweepy.TweepError: #taking extra care of the "rate limit exceeded"
    #       print("sleeping for 15mins...")
    #       time.sleep(60*15) 
    #       user = next(users)
    #     except StopIteration:
    #       break

    #     i += 1
    #     print("----- {} followers Found -----".format(i))
    #     follower_dict = dict()
    #     follower_dict["whose_follower"] = username
    #     follower_dict["user_id"] = user.id_str
    #     follower_dict["screen_name"] = user.screen_name
    #     follower_dict["name"] = user.name
    #     follower_dict["location"] = user.location
    #     follower_dict["description"] = user.description
    #     follower_dict["url"] = user.url
    #     follower_dict["protected"] = user.protected
    #     follower_dict["followers_count"] = user.followers_count
    #     follower_dict["friends_count"] = user.followers_count
    #     follower_dict["listed_count"] = user.listed_count
    #     follower_dict["statuses_count"] = user.statuses_count
    #     follower_dict["favourites_count"] = user.favourites_count
    #     follower_dict["account_created_at"] = str(user.created_at)
    #     follower_dict["verified"] = user.verified
    #     follower_dict["profile_url"] = ""
    #     follower_dict["profile_expanded_url"] = ""
    #     if "url" in user.entities:
    #       if "urls" in user.entities["url"] and user.entities["url"]["urls"]:
    #         if "url" in user.entities["url"]["urls"][0]:
    #           follower_dict["profile_url"] = user.entities["url"]["urls"][0]["url"]
    #         if "expanded_url" in user.entities["url"]["urls"][0]:
    #           follower_dict["profile_expanded_url"] = user.entities["url"]["urls"][0]["expanded_url"]

    #     follower_dict["account_lang"] = user.lang
    #     follower_dict["profile_banner_url"] = ""
    #     try:
    #       follower_dict["profile_banner_url"] = user.profile_banner_url
    #     except:
    #       pass

    #     follower_dict["profile_background_url"] = user.profile_background_image_url
    #     follower_dict["profile_image_url"] = user.profile_image_url

    #     print(json.dumps(follower_dict, indent=2))
    #     if follower_dict:
    #       # insert follower data to csv
    #       self.insert_to_csv(follower_dict)
    
    #   print("----- Total {} followers found -----".format(i))
    #   print("-----------------------------------")

    # except:
    #   print(traceback.print_exc())

  # try with pages  
    try:
      print("Finding followers of {}...".format(username))

      pages = tweepy.Cursor(api.followers, screen_name=username, count=200).pages()

      i = 0
      while True:
        try:
          page = next(pages)
          time.sleep(4)
        except tweepy.TweepError: #taking extra care of the "rate limit exceeded"
          print("manually, Sleeping for 15mins...")
          time.sleep(60*15) 
          page = next(pages)
        except StopIteration:
          break
        except:
          continue

        for user in page:
          i += 1
          print("----- {} followers Found -----".format(i))
          follower_dict = dict()
          follower_dict["whose_follower"] = username
          follower_dict["user_id"] = user.id_str
          follower_dict["screen_name"] = user.screen_name
          follower_dict["name"] = user.name
          follower_dict["location"] = user.location
          follower_dict["description"] = user.description
          follower_dict["url"] = user.url
          follower_dict["protected"] = user.protected
          follower_dict["followers_count"] = user.followers_count
          follower_dict["friends_count"] = user.followers_count
          follower_dict["listed_count"] = user.listed_count
          follower_dict["statuses_count"] = user.statuses_count
          follower_dict["favourites_count"] = user.favourites_count
          follower_dict["account_created_at"] = str(user.created_at)
          follower_dict["verified"] = user.verified
          follower_dict["profile_url"] = ""
          follower_dict["profile_expanded_url"] = ""
          if "url" in user.entities:
            if "urls" in user.entities["url"] and user.entities["url"]["urls"]:
              if "url" in user.entities["url"]["urls"][0]:
                follower_dict["profile_url"] = user.entities["url"]["urls"][0]["url"]
              if "expanded_url" in user.entities["url"]["urls"][0]:
                follower_dict["profile_expanded_url"] = user.entities["url"]["urls"][0]["expanded_url"]

          follower_dict["account_lang"] = user.lang
          follower_dict["profile_banner_url"] = ""
          try:
            follower_dict["profile_banner_url"] = user.profile_banner_url
          except:
            pass

          follower_dict["profile_background_url"] = user.profile_background_image_url
          follower_dict["profile_image_url"] = user.profile_image_url

          print(json.dumps(follower_dict, indent=2))
          if follower_dict:
            # insert follower data to csv
            self.insert_to_csv(follower_dict)
    
      print("----- Total {} followers found From {} -----".format(i, username))
      print("-----------------------------------")

    except:
      print(traceback.print_exc())

  # convert seconds to hhmmss
  def format_seconds_to_hhmmss(self, seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

  # main
  def main(self):
    if self.users_list:
      # iterate user list
      start_time = time.time()
      for index, username in enumerate(self.users_list):
        try:
          print("{}th User / Total {} Users : {}".format(index + 1, len(self.users_list), username))
          # get follower data
          follower_dict = self.get_followers_data(username)

        except:
          print(traceback.print_exc())
          continue
      end_time = time.time()
      elapsed_time = self.format_seconds_to_hhmmss(int(end_time-start_time))
      
      print("----- Elapsed Time : {} -----".format(elapsed_time))
    else:
      print("----- Empty Users List, Please Fill Out Users and Try again. -----")
      return

if __name__ == '__main__':
  
  directory_output = base_dir + "/output/"
  if os.path.exists(directory_output):
    # delete output csv
    if os.path.isfile(output_csv_path):
      os.remove(output_csv_path)
  else:
    os.makedirs(directory_output)

  follower_profile = Followers()
  follower_profile.main()