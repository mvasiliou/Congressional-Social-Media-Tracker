#Moved from Digital Ocean
from __future__ import print_function
import httplib2
import os
import io
import requests

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def send_simple_message(receiver, subject, message, mailgun_key):
    return requests.post(
        "https://api.mailgun.net/v3/mikevasiliou.com/messages",
        auth=("api", mailgun_key),
        data={"from": "War Room Bot <warroom@mikevasiliou.com>",
              "to": [receiver],
              "subject": subject,
              "html": message})

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_csv(mailgun_key):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    file_id = '1czRgaycfHBLzJVSeW4FnghMJH5aV8lDWQDGPNrdkfGY'
    
    request = service.files().export_media(fileId=file_id, mimeType='text/csv')
    fh = io.FileIO('candidate_links.csv', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    send_simple_message('mvasiliou94@gmail.com','Successfully downloaded new Candidate CSV from Google', 'Congrats! We will scrape likes now', mailgun_key)
if __name__ == '__main__':
    get_csv()
