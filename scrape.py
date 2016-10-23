import likes
import followers
import posts
import tweets
import datetime
from helper import get_token


if __name__ == "__main__":
    today = datetime.date.today()
    start_date_day = today - datetime.timedelta(days = 3)
    end_date = today - datetime.timedelta(days=2)

    likes.start_fb_likes()
    followers.start_twitter_followers()
    tweets.start_scrape_tweets()
    posts.start_scrape_posts(start_date_day, end_date)