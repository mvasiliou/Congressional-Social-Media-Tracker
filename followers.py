import tweepy
import csv
from pprint import pprint
import datetime
import time
import requests
import helper

def get_follow_counts(api,acc_id, cand_id, error_list):
    if acc_id == '?':
        return None, None, None, None
    elif acc_id == 'n/a':
        return 'n/a', 'n/a', 'n/a','n/a'

    try:
        user = api.get_user(acc_id)
        following = user._json['friends_count']
        followers = user._json['followers_count']
        status_count = user._json['statuses_count']
        favorites = user._json['favourites_count']
        return following, followers, status_count, favorites

    except Exception as e:
        error_list.append([cand_id, e, e.args])
        return 'ERROR','ERROR','ERROR','ERROR'

def start_twitter_followers():
    cand_file = open('candidate_links.csv','r')
    cand_reader = csv.reader(cand_file)
    next(cand_reader)

    date = str(datetime.date.today())
    file_name = 'social_data/followers/followers_' + date + '.csv'
    follow_file = open(file_name, 'w')
    follow_writer = csv.writer(follow_file)
    
    header = ['cand_id','date','camp_followers','camp_following','camp_statuses','camp_favorites','gov_followers','gov_following','gov_statuses', 'gov_favorites']
    follow_writer.writerow(header)

    api = helper.twitter_log_in()

    error_list = []
    print("Variables set up for scraping Twitter followers...scraping now!")
    for i, row in enumerate(cand_reader):
        cand_id = row[0]
        camp_twitter = row[7]
        gov_twitter = row[8]
        camp_following, camp_followers, camp_statuses,camp_favorites = get_follow_counts(api,camp_twitter, cand_id, error_list)
        gov_following, gov_followers, gov_statuses,gov_favorites = get_follow_counts(api,gov_twitter, cand_id, error_list)
        write_row = [cand_id, date, camp_followers, camp_following, camp_statuses,camp_favorites, gov_followers, gov_following,gov_statuses, gov_favorites]
        follow_writer.writerow(write_row)

if __name__ == "__main__":
    start_twitter_followers()
