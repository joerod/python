# thsi script checks gmail for emails from streeteasy gets the person who is interested email and sends a template email then marks the email as read
import os.path
import re
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email import message_from_bytes

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.modify']


def authenticate_gmail():
    """Authenticates with Gmail API and returns the service object."""
    creds = None
    if os.path.exists('/home/joerod/token.json'):
        creds = Credentials.from_authorized_user_file('/home/joerod/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/joerod/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('/home/joerod/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def search_emails_with_subject(service, subjects):
    subject_query = ' OR '.join([f'subject:"{subject}"' for subject in subjects])
    query = f'is:unread ({subject_query})'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found with subjects:', subjects)
    else:
        unique_emails = set()
        for message in messages:
            msg_id = message['id']
            msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = message_from_bytes(msg_str)
            email_body = get_email_body(mime_msg)
            extract_and_store_unique_emails(email_body, unique_emails)

            # Mark the email as read
            mark_as_read(service, msg_id)

        # Remove specific email address if present
        unique_emails.discard('joerod@gmail.com')

        if unique_emails:
            print("Unique email addresses found:", unique_emails)
            for email in unique_emails:
                send_email(service, email)
        else:
            print("No unique email addresses found.")

def get_email_body(mime_msg):
    """Extracts the body from the email message"""
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            if part.get_content_type() == "text/html":
                return part.get_payload(decode=True).decode()
    else:
        if mime_msg.get_content_type() == "text/plain":
            return mime_msg.get_payload(decode=True).decode()
    return ""

def extract_and_store_unique_emails(text, email_set):
    """Extracts email addresses from text and stores unique ones in the set"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_addresses = re.findall(email_pattern, text)
    for email in email_addresses:
        email_set.add(email)

def create_message(to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(service, to_email):
    """Send an email to the specified address."""
    subject = "21-28 35th Street #4E Astoria"
    body = """Hello,

Thanks for your interest in my apartment, my name is Joe and I am the owner of this unit.

I am having an open house this Sunday 5/19/24 between 12PM and 1:30PM. Feel free to come by then to view the apartment and fill out an application if you’re interested.

Thanks,
Joe Rodriguez
(212) 877-0591"""

    message = create_message(to_email, subject, body)
    sent_message = service.users().messages().send(userId="me", body=message).execute()
    print(f'Email sent to {to_email}')

def mark_as_read(service, msg_id):
    """Mark an email as read."""
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
    print(f'Marked message {msg_id} as read.')

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    subjects = ["New Zillow Group Rentals Contact: 21-28 35th St #4E",
                "21-28 35th Street #4E StreetEasy Inquiry"]
    search_emails_with_subject(service, subjects)

if __name__ == '__main__':
    main()
