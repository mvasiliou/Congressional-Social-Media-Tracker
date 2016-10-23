import tweepy
import csv
import datetime
import time
from email.utils import parsedate_tz
import pytz
import requests
import helper

def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime.datetime(*time_tuple[:6])
    return dt - datetime.timedelta(seconds=time_tuple[-1])

def get_tweets(api, acc_id, cand_id, writer, start_date, end_date, error_list):
    if acc_id == '?' or acc_id =='n/a':
        return []

    tweet_list = []
    try:
        tweets = api.user_timeline(acc_id)
    except Exception as e:
        print(e, e.args)
        error_list.append(cand_id+', ' + str(e) +', ' +str(e.args))
        return []

    for tweet in tweets:
        tweet = tweet._json
        tweet_id = tweet['id']
        created = tweet['created_at']
        utc=pytz.UTC
        created = utc.localize(to_datetime(created))
        if start_date < created < end_date:
            likes = tweet['favorite_count']
            retweets = tweet['retweet_count']
            text = tweet['text']
            text = text.replace('\n', '')
            text = text.encode('ascii', 'ignore')
            source = tweet['source'].split('>')[1].split('<')[0]
            if 'media' in tweet['entities']:
                tweet_type = tweet['entities']['media'][0]['type']
            else:
                tweet_type = 'status'
            tweet_info = [cand_id,tweet_id, created, text, likes, retweets, source, tweet_type]
            try:
                writer.writerow(tweet_info)
            except Exception as e:
                error_list.append(cand_id +','+ str(e)+','+str(e.args))
        if created < start_date:
            break
        if tweet == tweets[-1] and created > start_date:
            print('Need more tweets')
            error_list.append(cand_id + ' Need more tweets')

    return tweet_list

def start_scrape_tweets():
    cand_file = open('candidate_links.csv','r')
    cand_reader = csv.reader(cand_file)
    next(cand_reader)

    utc=pytz.UTC
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days = 3)
    end_date = today - datetime.timedelta(days=2)
    camp_file_name = 'social_data/tweets/camp/camp_tweets_' + str(start_date) + '_test.csv'
    gov_file_name = 'social_data/tweets/gov/gov_tweets_' + str(start_date) +'_test.csv'
    camp_tweets_file = open(camp_file_name, 'w')
    gov_tweets_file = open(gov_file_name, 'w')

    start_date = utc.localize(datetime.datetime.combine(start_date, datetime.datetime.min.time()))
    end_date = utc.localize(datetime.datetime.combine(end_date, datetime.datetime.min.time()))
    camp_tweets_writer = csv.writer(camp_tweets_file)
    gov_tweets_writer = csv.writer(gov_tweets_file) 

    header = ['cand_id', 'tweet_id', 'created', 'text', 'likes','retweets','source','tweets_type']
    camp_tweets_writer.writerow(header)
    gov_tweets_writer.writerow(header)

    error_list = []
    api = helper.twitter_log_in()
    print('Set up variables...scraping tweets now!')

    for i, row in enumerate(cand_reader):
        cand_id = row[0]
        camp_twitter = row[7]
        gov_twitter = row[8]

        camp_tweets = get_tweets(api, camp_twitter, cand_id, camp_tweets_writer,start_date, end_date,error_list)
        gov_tweets = get_tweets(api, gov_twitter, cand_id, gov_tweets_writer,start_date,end_date, error_list)
        break

    message = 'Hello Mike, <br><br>'
    if len(error_list) == 0:
        message += "No errors! Have a great day!"
    else:
        for error in error_list:
            message += error + '<br><br>'
    helper.send_message('mvasiliou94@gmail.com', 'Completed scraping tweets for ' + str(today),message, [("attachment", open(camp_file_name)),("attachment", open(gov_file_name))])

if __name__ == '__main__':
    start_scrape_tweets()
