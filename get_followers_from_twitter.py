import tweepy
import csv
from pprint import pprint
import datetime
import time
import requests

def send_simple_message(receiver, subject, message, file_name, mailgun_key):
    return requests.post(
        "https://api.mailgun.net/v3/mikevasiliou.com/messages",
        auth=("api", mailgun_key),
        files=[("attachment", open(file_name))],
        data={"from": "War Room Bot <warroom@mikevasiliou.com>",
              "to": [receiver],
              "subject": subject,
              "html": message})

def get_twitter_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):  
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api    

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

def start_twitter_followers(mailgun_key, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    cand_file = open('candidate_links.csv','r')
    cand_reader = csv.reader(cand_file)
    next(cand_reader)

    date = str(datetime.date.today())
    file_name = 'social_data/followers/followers_' + date + '.csv'
    follow_file = open(file_name, 'w')
    follow_writer = csv.writer(follow_file)
    
    header = ['cand_id','date','camp_followers','camp_following','camp_statuses','camp_favorites','gov_followers','gov_following','gov_statuses', 'gov_favorites']
    follow_writer.writerow(header)

    api = get_twitter_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

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

    error_message = "Good morning Mike,<br><br>"
    if len(error_list) == 0:
        error_message+="Congrats! There were no errors today!"
    else:
        error_message += "Here are today's errors: <br><br>"
        for item in error_list:
            error_message += str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '<br>'
    now = datetime.datetime.now()    
    send_simple_message('mvasiliou94@gmail.com', 'Successfully scraped followers at: '+str(date), error_message, file_name, mailgun_key)
    print('Done')

if __name__ == "__main__":
    start_twitter_followers(mailgun_key, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
