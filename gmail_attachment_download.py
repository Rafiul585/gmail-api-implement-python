# [Gmail Attachment Download]
from __future__ import print_function
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Creating a token.json file with authentication details
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():

    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    # Check if it exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Use try-except to avoid any Errors
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # request a list of all the messages
        # results = service.users().messages().list(userId='me').execute()

        # Pass maxResults to get any number of emails. Like this:
        # results = service.users().messages().list(maxResults=2, userId='me').execute()

        # Getting all the unread messages from Inbox
        # labelIds can be changed accordingly
        results = service.users().messages().list(maxResults=2, userId='me', labelIds=['INBOX', 'UNREAD']).execute()

        messages  = results.get('messages')

        # messages is a list of dictionaries where each dictionary contains a message id.

        # iterate through all the messages
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            for part in txt['payload']['parts']:

                if part['filename']:

                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=msg['id'], id=att_id).execute()
                    data = att['data']

                    # decoding from Base64 to UTF-8
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = part['filename']

                    # write attachment to csv file
                    with open(path, 'wb') as f:
                        f.write(file_data)


    except HttpError as error:
        # Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
# [END Gmail Attachment Download]