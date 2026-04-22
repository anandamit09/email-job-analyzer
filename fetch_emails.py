from imapclient import IMAPClient
from email.parser import BytesParser
from email.policy import default
from datetime import datetime, timedelta
from utils import clean_html

EMAIL = "yourmail@gmail.com"
PASSWORD = "your_app_password_here"
IMAP_SERVER = "imap.gmail.com"

def fetch_emails(placement_email, start_date, end_date):
    emails_data = []

    with IMAPClient(IMAP_SERVER) as server:
        server.login(EMAIL, PASSWORD)
        server.select_folder("INBOX")

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

        messages = server.search([
            'FROM', placement_email,
            'SINCE', start,
            'BEFORE', end
        ])

        for uid in messages:
            raw_message = server.fetch([uid], ['BODY[]'])
            msg = BytesParser(policy=default).parsebytes(raw_message[uid][b'BODY[]'])

            subject = msg.get('Subject', '')
            body = msg.get_body(preferencelist=('plain', 'html')).get_payload(decode=True).decode()
            
            if msg.get_content_type() == 'text/html':
                body = clean_html(body)

            emails_data.append({
                "subject": subject,
                "body": body
            })

    return emails_data