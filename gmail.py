from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def main():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://mail.google.com/']

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    q = "older_than:15y"
    raw_messages = get_raw_messages(q,service)
    if raw_messages:
        print("got messages!")
        messages_list = prep_messages_for_delete(raw_messages)
        batch_delete_messages(service, messages_list)
    else:
        print('No message found matching "{0}"'.format(q))

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

    print("got {0} ids".format(len(message['ids'])))
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
        print('An error occurred while batchDeleting: {0}'.format(error))

if __name__ == '__main__':
    main()