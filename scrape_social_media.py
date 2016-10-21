#Saved from Digital Ocean
import download_csv_from_drive as dl_csv
import gather_fb_likes as fb_likes
import get_followers_from_twitter as tw_followers
import gather_fb_statuses as fb_posts
import get_tweets
import datetime

def get_token(file_name):
    infile = open(file_name, 'r')
    token = infile.readline()
    infile.close()
    return token

if __name__ == "__main__":
    today = datetime.date.today()
    start_date_day = today - datetime.timedelta(days = 3)
    end_date = today - datetime.timedelta(days=2)

    fb_token = get_token("/Tokens/fb_token.txt") 
    mailgun_key = get_token('/Tokens/mailgun_key.txt') 
    CONSUMER_KEY = get_token('/Tokens/consumer_key.txt')
    CONSUMER_SECRET = get_token('/Tokens/consumer_secret.txt')
    
    ACCESS_KEY = get_token('/Tokens/access_key.txt')
    ACCESS_SECRET = get_token('/Tokens/access_secret.txt')
    dl_csv.get_csv(mailgun_key)
    fb_likes.start_fb_likes(fb_token, mailgun_key)
    tw_followers.start_twitter_followers(mailgun_key,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    get_tweets.start_scrape_tweets(mailgun_key,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    fb_posts.start_scrape_posts(start_date_day, end_date, fb_token, mailgun_key)
