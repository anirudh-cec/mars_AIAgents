#!/usr/bin/env python3
"""
Mars AI Agents - Gmail Data Retrieval Module
Connects to Gmail API to check for new emails and download attachments
"""

import os
import io
import base64
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailDataRetriever:
    """Class to handle Gmail API operations for retrieving email attachments"""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize Gmail API client
        
        Args:
            credentials_file: Path to Gmail API credentials file
            token_file: Path to store authentication token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.target_email = "demotest.tcs@gmail.com"
        self.data_folder = "data"
        
        # Ensure data folder exists
        os.makedirs(self.data_folder, exist_ok=True)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    return False
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"Error: Gmail API credentials file '{self.credentials_file}' not found.")
                    print("Please download credentials.json from Google Cloud Console.")
                    return False
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}")
                    return False
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            # Check which account we're authenticated as
            self._check_authenticated_account()
            return True
        except Exception as e:
            print(f"Error building Gmail service: {e}")
            return False
    
    def _check_authenticated_account(self):
        """Check which Gmail account we're authenticated as"""
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            email_address = profile.get('emailAddress', 'Unknown')
            print(f"Debug: Authenticated as Gmail account: {email_address}")
            
            if email_address != self.target_email:
                print(f"Warning: Authenticated as {email_address} but target is {self.target_email}")
                print(f"Note: Will search inbox of {email_address} for emails")
            else:
                print(f"Info: Correctly authenticated as target account {self.target_email}")
                
        except Exception as e:
            print(f"Warning: Could not check authenticated account: {e}")
    
    def get_recent_emails(self, hours_back: int = 24) -> List[str]:
        """
        Get recent emails to the target email address (checking inbox)
        
        Args:
            hours_back: Number of hours to look back for emails
            
        Returns:
            List of message IDs
        """
        try:
            # Calculate date filter (emails from the last 24 hours)
            date_filter = datetime.now() - timedelta(hours=hours_back)
            date_str = date_filter.strftime('%Y/%m/%d')
            
            print(f"Debug: Searching for emails after {date_str}")
            print(f"Debug: Looking for emails TO {self.target_email}")
            
            # Search query for emails TO target address with attachments
            # Note: This assumes we're authenticated as the target Gmail account
            query = f'has:attachment after:{date_str}'
            
            print(f"Debug: Using query: {query}")
            
            # Get message list
            result = self.service.users().messages().list(
                userId='me', 
                q=query,
                maxResults=10
            ).execute()
            
            messages = result.get('messages', [])
            print(f"Debug: Found {len(messages)} messages")
            
            # If no messages found with attachments, try without attachment filter
            if not messages:
                print("Debug: No messages with attachments found, trying without attachment filter...")
                query_no_attachment = f'after:{date_str}'
                result_no_attachment = self.service.users().messages().list(
                    userId='me',
                    q=query_no_attachment,
                    maxResults=5
                ).execute()
                messages_no_attachment = result_no_attachment.get('messages', [])
                print(f"Debug: Found {len(messages_no_attachment)} total messages (without attachment filter)")
            
            return [msg['id'] for msg in messages]
            
        except HttpError as error:
            print(f'Gmail API error occurred: {error}')
            return []
        except Exception as e:
            print(f'Error retrieving emails: {e}')
            return []
    
    def get_message_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific message
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Message details dictionary or None if error
        """
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id
            ).execute()
            return message
        except HttpError as error:
            print(f'Error retrieving message {message_id}: {error}')
            return None
    
    def download_attachments(self, message_id: str) -> List[str]:
        """
        Download all attachments from a message
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            List of downloaded file paths
        """
        downloaded_files = []
        
        try:
            message = self.get_message_details(message_id)
            if not message:
                return downloaded_files
            
            # Save files directly in data folder (no date subfolders)
            download_path = self.data_folder
            
            # Process message parts to find attachments
            parts = self._get_message_parts(message)
            
            for part in parts:
                if part.get('filename') and part.get('body', {}).get('attachmentId'):
                    filename = part['filename']
                    attachment_id = part['body']['attachmentId']
                    
                    # Download attachment
                    attachment = self.service.users().messages().attachments().get(
                        userId='me',
                        messageId=message_id,
                        id=attachment_id
                    ).execute()
                    
                    # Decode and save file
                    file_data = base64.urlsafe_b64decode(attachment['data'])
                    file_path = os.path.join(download_path, filename)
                    
                    # Handle duplicate filenames with timestamp
                    if os.path.exists(file_path):
                        timestamp = int(message['internalDate']) / 1000
                        time_str = datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M%S')
                        base_name, extension = os.path.splitext(filename)
                        filename = f"{base_name}_{time_str}{extension}"
                        file_path = os.path.join(download_path, filename)
                        
                        # If still duplicate, add counter
                        counter = 1
                        while os.path.exists(file_path):
                            new_filename = f"{base_name}_{time_str}_{counter}{extension}"
                            file_path = os.path.join(download_path, new_filename)
                            counter += 1
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                    
                    downloaded_files.append(file_path)
                    print(f"Downloaded: {file_path}")
            
        except HttpError as error:
            print(f'Error downloading attachments: {error}')
        except Exception as e:
            print(f'Unexpected error: {e}')
        
        return downloaded_files
    
    def _get_message_parts(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Recursively extract all parts from a message
        
        Args:
            message: Gmail message object
            
        Returns:
            List of message parts
        """
        parts = []
        payload = message.get('payload', {})
        
        if 'parts' in payload:
            for part in payload['parts']:
                parts.extend(self._extract_parts(part))
        else:
            parts.append(payload)
        
        return parts
    
    def _extract_parts(self, part: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Recursively extract parts from nested message structure
        
        Args:
            part: Message part
            
        Returns:
            List of parts
        """
        parts = []
        if 'parts' in part:
            for subpart in part['parts']:
                parts.extend(self._extract_parts(subpart))
        else:
            parts.append(part)
        return parts
    
    def process_new_emails(self) -> Dict[str, Any]:
        """
        Main method to check for new emails and download attachments
        
        Returns:
            Dictionary with processing results
        """
        result = {
            'success': False,
            'message': 'No new records to display',
            'files_downloaded': [],
            'emails_processed': 0,
            'error': None
        }
        
        try:
            # Authenticate
            if not self.authenticate():
                result['error'] = 'Failed to authenticate with Gmail API'
                return result
            
            # Get recent emails
            message_ids = self.get_recent_emails()
            
            if not message_ids:
                result['message'] = 'No new emails with attachments found'
                return result
            
            # Process each email
            all_downloaded_files = []
            for message_id in message_ids:
                downloaded_files = self.download_attachments(message_id)
                all_downloaded_files.extend(downloaded_files)
            
            if all_downloaded_files:
                result['success'] = True
                result['message'] = f'Successfully downloaded {len(all_downloaded_files)} attachment(s) from {len(message_ids)} email(s)'
                result['files_downloaded'] = all_downloaded_files
                result['emails_processed'] = len(message_ids)
            else:
                result['message'] = 'Emails found but no attachments to download'
            
        except Exception as e:
            result['error'] = f'Unexpected error during processing: {str(e)}'
        
        return result

# Main execution function
def test_gmail_search():
    """Test function to debug Gmail search queries"""
    print("Gmail Search Debug Test")
    print("=" * 30)
    
    retriever = GmailDataRetriever()
    
    # Authenticate
    if not retriever.authenticate():
        print("Authentication failed!")
        return
    
    print("\n=== Testing different search queries ===")
    
    # Test queries to try
    test_queries = [
        'has:attachment',  # All emails with attachments
        'after:2025/01/01 has:attachment',  # Recent emails with attachments
        'after:2025/01/01',  # All recent emails
        'in:inbox has:attachment',  # Inbox emails with attachments
        'newer_than:1d',  # Emails from last day
        'newer_than:1d has:attachment',  # Recent emails with attachments
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        try:
            result = retriever.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=5
            ).execute()
            messages = result.get('messages', [])
            print(f"  Found: {len(messages)} messages")
            
            # Show details of first message if any
            if messages:
                first_msg = retriever.get_message_details(messages[0]['id'])
                if first_msg:
                    headers = first_msg.get('payload', {}).get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
                    from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'No sender')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No date')
                    print(f"  Sample email - From: {from_addr[:50]}...")
                    print(f"  Sample email - Subject: {subject[:50]}...")
                    print(f"  Sample email - Date: {date}")
                    
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n=== Search test completed ===\n")

def main():
    """Main function for standalone execution"""
    print("Mars AI Agents - Gmail Data Retrieval")
    print("=" * 40)
    
    # Ask user what they want to do
    print("\nOptions:")
    print("1. Test Gmail search queries (debug)")
    print("2. Process emails normally")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        test_gmail_search()
    else:
        retriever = GmailDataRetriever()
        result = process_gmail_data()
        
        print(f"\nResult: {result['message']}")
        if result.get('error'):
            print(f"Error: {result['error']}")
        
        if result.get('files_downloaded'):
            print(f"\nDownloaded files:")
            for file_path in result['files_downloaded']:
                print(f"  - {file_path}")

def process_gmail_data() -> Dict[str, Any]:
    """
    Function to be called by Flask API
    
    Returns:
        Processing results dictionary
    """
    retriever = GmailDataRetriever()
    return retriever.process_new_emails()

if __name__ == "__main__":
    main()