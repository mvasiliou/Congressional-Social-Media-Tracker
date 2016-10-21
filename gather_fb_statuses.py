import facebook
import csv
import requests
import datetime 
import dateutil.parser
import pytz
import time

def send_simple_message(receiver, subject, message, file_name,file_name_2, mailgun_key):
    return requests.post(
        "https://api.mailgun.net/v3/mikevasiliou.com/messages",
        auth=("api", mailgun_key),
        files=[("attachment", open(file_name)), ("attachment",open(file_name_2))],
        data={"from": "War Room Bot <warroom@mikevasiliou.com>",
              "to": [receiver],
              "subject": subject,
              "html": message})

def login(user_token):
    graph = facebook.GraphAPI(access_token = user_token, version = '2.6')
    return graph

def count_interactions(graph, post_id,type_int, post, call_count):
    call_count += 1
    interactions = graph.get_connections(id= post_id, connection_name = type_int, summary = 'true')
    num_interactions = interactions['summary']['total_count']
    return num_interactions

def get_posts(page_id, graph, cand_id, writer, start_date, end_date,error_list,call_count):
    accepted_types = ['mobile_status_update','added_photos','added_video','shared_story','created_event']

    if page_id != '' and page_id != '?' and page_id != 'n/a':
        if page_id[0] == "'":
            page_id = page_id[1:-1]
        try:
            call_count += 1
            page = graph.get_object(id = page_id, fields = 'feed')
            posts = page['feed']['data']
        except Exception as e:
            print(e, e.args)
            posts = []
            error_list.append(cand_id +','+ str(e) +','+ str(e.args))
        for post in posts:
            post_id = post['id']
            try:
                call_count += 1
                post = graph.get_object(id = post_id, fields = 'created_time,status_type,message,type')
                created = post['created_time']           
                created_obj = dateutil.parser.parse(created)
                if start_date < created_obj < end_date:
                    if 'status_type' in post:
                        status_type = post['status_type']
                        if status_type in accepted_types:
                            likes = count_interactions(graph, post_id,'likes', post, call_count)
                            comments = count_interactions(graph, post_id,'comments', post, call_count)
                            post_type = post['type']
                            post_id = post['id']
                            if 'message' in post:
                                message = post['message']
                                message = message.replace('\n', '')
                                message = message.encode('ascii', 'ignore')
                            else:
                                message = None
                            created, post_id, post_type, message
                            post = [cand_id, str(created_obj), post_id, post_type, message, likes, comments]
                            writer.writerow(post)
            except Exception as error:
                print(error)
                print(error.args)
                error_list.append(cand_id + str(error) + str(error.args))

def set_up_csvs(start_date):

    candfile = open('candidate_links.csv')
    candreader = csv.reader(candfile)

    camp_path = 'social_data/statuses/camp/camp_statuses_'+str(start_date)+'.csv'
    camp_file = open(camp_path, 'w')
    camp_writer = csv.writer(camp_file)

    gov_path = 'social_data/statuses/gov/gov_statuses_' + str(start_date) +'.csv'
    gov_file = open(gov_path, 'w')
    gov_writer = csv.writer(gov_file)
    
    header = ['cand_id', 'created', 'post_id', 'post_type', 'message', 'likes', 'comments']
    camp_writer.writerow(header)
    gov_writer.writerow(header)
    next(candreader)
    return candreader, camp_writer, gov_writer, camp_path, gov_path

def start_scrape_posts(start_date_day, end_date, fb_token, mailgun_key):
    graph = login(fb_token)

    utc=pytz.UTC
    today = datetime.date.today()

    candreader, camp_writer, gov_writer, camp_path, gov_path = set_up_csvs(start_date_day)
    start_date = utc.localize(datetime.datetime.combine(start_date_day, datetime.datetime.min.time()))
    end_date = utc.localize(datetime.datetime.combine(end_date, datetime.datetime.min.time()))

    error_list = []
    call_count = 0
    print('Collected variables for FB posts...scraping now!')
    for line in candreader:
        cand_id = line[0]
        campaign_id = line[5]
        gov_id = line[6]
        get_posts(campaign_id, graph, cand_id, camp_writer, start_date, end_date,error_list, call_count)
        get_posts(gov_id, graph, cand_id, gov_writer, start_date, end_date,error_list, call_count)
        time.sleep(10)

    message = "Good morning Mike,<br><br>"
    if len(error_list) ==0:
        message += "No errors today! Have a great day!"
    else:
        message+= "Here are today's errors:<br><br>"
        for error in error_list:
            message+= error+'<br><br>'
    send_simple_message('mvasiliou94@gmail.com', 'Collected FB Statuses on ' + str(today), message, camp_path,gov_path, mailgun_key)

if __name__ == "__main__":
    start_date_day = today - datetime.timedelta(days = 3)
    end_date = today - datetime.timedelta(days=2)

    start_scrape_posts(start_date_day, end_date, fb_token, mailgun_key)
