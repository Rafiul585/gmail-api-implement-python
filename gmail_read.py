# [START GMAIL READ]
from __future__ import print_function
import os.path
import base64
from bs4 import BeautifulSoup
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
        results = service.users().messages().list(userId='me').execute()

        messages  = results.get('messages')

        # messages is a list of dictionaries where each dictionary contains a message id.

        # iterate through all the messages
        for msg in messages:
            temp_dict = {}
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']
    
                # Look for Subject and Sender Email in the headers
                for d in headers:
                    # getting the Subject
                    if d['name'] == 'Subject':
                        msg_subject = d['value']
                        temp_dict['Subject'] = msg_subject

                    # getting the Sender
                    if d['name'] == 'From':
                        msg_sender = d['value']
                        temp_dict['Sender'] = msg_sender

                    # getting the date
                    if d['name'] == 'Date':
                        msg_date = d['value']
                        temp_dict['Date'] = msg_date

                
                # Fetching message body
                mssg_parts = payload['parts'][0]['parts'][0]['body']['data'] # fetching data from the body
                clean_one = mssg_parts.replace("-","+") # decoding from Base64 to UTF-8
                clean_two = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                clean= base64.b64decode (bytes(clean_two, 'UTF-8')) # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean, "lxml")
                # mssg_body is a readible form of message body
		        # depending on the end user's requirements, it can be further cleaned 
		        # using regex, beautiful soup, or any other method
                mssg_body = soup.body()
                temp_dict['Message_body'] = mssg_body


            except Exception as e:
                print('except', e)
        
    except HttpError as error:
        # Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
# [END GMAIL READ]