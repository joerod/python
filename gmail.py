from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#configure scopes and get token
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#Credential function
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
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

#create session
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

#start script

#finds all messages labeled as SPAM
#need to add pagination
def delete_spam():
    try:
        SPAM  = service.users().messages().list(userId='me',labelIds='SPAM').execute()['messages']
        for delete in SPAM:
            service.users().messages().delete(userId='me', id=delete['id']).execute()
        print("{:d} SPAM emails have been deleted".format(len(SPAM)))
    except:
        print("No Unread messages found")

delete_spam()

#finds all messages labeled as Unread
#need to add pagination
def mark_as_read():
    try:
        Unread = service.users().messages().list(userId='me',labelIds='UNREAD').execute()['messages']
        for markread in Unread:
                service.users().messages().modify(userId='me',id=markread['id'], body={'removeLabelIds' : ['UNREAD']}).execute()
        print ("{:d} emails have been marked as read".format(len(Unread)))
    except:
        print("No SPAM messages found")
mark_as_read()
