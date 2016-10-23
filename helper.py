import requests
import facebook
import tweepy

def send_message(receiver, subject, message, files = []):
    mailgun_key = get_token('Tokens/mailgun_key.txt')
    return requests.post(
        "https://api.mailgun.net/v3/mikevasiliou.com/messages",
        auth=("api", mailgun_key),
        files = files,
        data={"from": "War Room Bot <warroom@mikevasiliou.com>",
              "to": [receiver],
              "subject": subject,
              "html": message})

def fb_log_in():
    user_token = get_token('Tokens/fb_token.txt')
    graph = facebook.GraphAPI(access_token = user_token, version = '2.6')
    return graph

def twitter_log_in():
    consumer_key = get_token('Tokens/consumer_key.txt')
    consumer_secret = get_token('Tokens/consumer_secret.txt')
    access_key = get_token('Tokens/access_key.txt')
    access_secret   = get_token('Tokens/access_secret.txt')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api    

def get_token(file_name):
    infile = open(file_name, 'r')
    token = infile.readline()
    infile.close()
    return token