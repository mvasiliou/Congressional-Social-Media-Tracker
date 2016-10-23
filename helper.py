import requests
import facebook
import tweepy

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