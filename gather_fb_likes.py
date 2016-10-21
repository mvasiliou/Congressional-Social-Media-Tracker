import facebook
import csv
import datetime
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

def get_likes(page_id, graph, error_list):
    if page_id == '?' or page_id == '':
        likes = None
    elif page_id == 'n/a':
        likes = 'n/a'
    else:
        try:
            if page_id[0] == "'":
                page_id = page_id[1:-1]
            page = graph.get_object(id = page_id, fields = 'fan_count')
            likes = page['fan_count']
        except Exception as error:
            likes = 'ERROR CHECK MANUALLY'
            print(error, error.args)
            error_list.append([page_id, str(error), str(error.args)])
    return likes 

def log_in(user_token):
    graph = facebook.GraphAPI(access_token = user_token, version = '2.6')
    return graph

def start_fb_likes(fb_token, mailgun_key):
    graph = log_in(fb_token)
    candfile = open('candidate_links.csv')
    candreader = csv.reader(candfile)
    date = str(datetime.date.today())
    file_name = 'social_data/likes/likes_'+date+'.csv'
    likesfile = open(file_name, 'w')
    likeswriter = csv.writer(likesfile)
    head = ['cand_id', 'date', 'camp_likes', 'gov_likes']
    likeswriter.writerow(head)
    next(candreader)
    error_list = []
    print('Variables set up for FB likes...counting now!')
    for line in candreader:
        cand_id = line[0]
        campaign_id = line[5]
        gov_id = line[6]
        campaign_likes = get_likes(campaign_id, graph, error_list)
        gov_likes = get_likes(gov_id, graph, error_list)
        row = [cand_id,date,campaign_likes,gov_likes]
        likeswriter.writerow(row)

    error_message = "Good afternoon Mike,<br><br>"
    if len(error_list) == 0:
        error_message+="Congrats! There were no errors today!"
    else:
        error_message += "Here are today's errors: <br><br>"
        for item in error_list:
            error_message += item[0] + ',' + item[1] + ',' + item[2] + '<br>'
    now = str(datetime.datetime.now())	
    send_simple_message('mvasiliou94@gmail.com', 'Successfully scraped likes at: '+ now, error_message, file_name, mailgun_key)
    print('Done')
    
if __name__ =="__main__":
    start_fb_likes(fb_token)
