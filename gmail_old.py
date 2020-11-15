from __future__ import print_function
import httplib2
import os
import base64
import mimetypes

from apiclient import discovery,errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors

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
def delete_spam(service,user_id):
    try:
        SPAM  = service.users().messages().list(userId=user_id,labelIds='SPAM').execute()['messages']
        for delete in SPAM:
            service.users().messages().delete(userId=user_id, id=delete['id']).execute()
        print("{:d} SPAM emails have been deleted".format(len(SPAM)))
    except:
        print("No Unread messages found")

#delete_spam(service,'me')
#finds all messages labeled as Unread
#need to add pagination
def mark_as_read(service,user_id):
    try:
        Unread = service.users().messages().list(userId=user_id,labelIds='UNREAD').execute()['messages']
        for markread in Unread:
                service.users().messages().modify(userId=user_id,id=markread['id'], body={'removeLabelIds' : ['UNREAD']}).execute()
        print ("{:d} emails have been marked as read".format(len(Unread)))
    except:
        print("No SPAM messages found")

#mark_as_read(service,'me')
#Send an email message.
def SendMessage(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

#Create a message for an email.
def CreateMessage(sender, to, subject, message_text):

  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

#Create a message for an email.
def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir, filename):

  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}

#SendMessage(service,'me',CreateMessage('bill.gates@gmail.com','joerod@gmail.com','You are the man','test'))

#Gets profile info
def get_profile(service,user_id):
    profile = service.users().getProfile(userId=user_id).execute()
    for k in profile.keys():
        print(k, ':', profile[k])

get_profile(service,'me')

def ListLabels(service,user_id):
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        for label in labels:
             print('Label id: %s - Label name: %s' % (label['id'], label['name']))
        return labels
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

#ListLabels(service,'me')