from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import argparse

def main(scopes,cred_dir,q):
    """
      Will use a gmail search query to find emails based on some criteria
      and delete them in batches of 1000 which is a gmail limitation
      Usage: python3 gmail.py --cred_dir '/home/joerod/Downloads' --q 'older_than:1y category:forums -is:starred' --scopes ['https://mail.google.com/']
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(cred_dir, 'token.pickle')):
        with open(os.path.join(cred_dir, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(cred_dir, 'credentials.json'), scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(cred_dir, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    for i in range(100):
        raw_messages = get_raw_messages(q,service)
        if raw_messages:
            print("I've got mail!")
            messages_list = prep_messages_for_delete(raw_messages)
            batch_delete_messages(service, messages_list)
            i += 1
        else:
            sys.exit('No message found matching "{}"'.format(q))

    # Call the Gmail API
def get_raw_messages(query,service,userId='me'):
    response = service.users().messages().list(userId=userId,q=query).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(
            userId=userId,
            q=query,
            pageToken=page_token
        ).execute()
        messages.extend(response['messages'])
        if len(messages) > 999:
            break
    return messages

def prep_messages_for_delete(raw_messages):
    message = {
        'ids': []
    }

    message['ids'].extend([str(d['id']) for d in raw_messages])

    print("Returned {} ids".format(len(message['ids'])))
    return message


def batch_delete_messages(service, messages):
    print("ready to delete {} messages".format(len(messages['ids'])))
    user_id = "me"

    try:
        service.users().messages().batchDelete(
            userId=user_id,
            body=messages
        ).execute()

        print("I deleted stuff!")
    except errors.HttpError as error:
        print('An error occurred while batchDeleting: {}'.format(error))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gmail deleter')
    parser.add_argument('--scopes', metavar="['https://mail.google.com/']", required=True,
                        help='gmail scope',
                        const="https://mail.google.com/",
                        nargs='?',
                        type=str)
    parser.add_argument('--cred_dir', metavar='path', required=True,
                        help='directory of credentials')
    parser.add_argument('--q', metavar='older_than:1y category:forums -is:starred', required=True,
                        help='gmail query to find emails')
    args = parser.parse_args()
    main(scopes=args.scopes, cred_dir=args.cred_dir, q=args.q)
