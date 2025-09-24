import requests
import concurrent.futures
from requests.auth import HTTPBasicAuth
import os
import json
import pandas as pd
import datetime as dt
from dotenv import load_dotenv
import time
import numpy as np
import logging
from email_content import html_content  # Confidential HTML content

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("survey_sender.log"),
        logging.StreamHandler()
    ]
)

def get_contact(email, session):
    """Check if the email exists as a contact in Envoke."""
    url = f"https://e1.envoke.com/v1/contacts?email={email}&limit=1"
    headers = {'Accept': 'application/json'}
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            logging.info(f"Contact found for email: {email}")
            return data[0]  # assuming single contact returned
        else:
            logging.info(f"No contact found for email: {email}")
            return None
    except Exception as e:
        logging.error(f"Error retrieving contact {email}: {e}")
        return None

def send_survey(recip, contact_name, html_content, session):
    """Send the survey email via Envoke API."""
    url = "https://e1.envoke.com/api/v4legacy/send/SendEmails.json"

    payload = {
        "SendEmails": [
            {
                "EmailDataArray": [
                    {
                        "email": [
                            {
                                "to_email": recip,
                                "to_name": contact_name,
                                "from_email": "from_email",
                                "from_name": "from_name",
                                "reply_email": "from_email",
                                "reply_name": "No reply",
                                "message_subject": "We Want Your Feedback!",
                                "message_html": html_content
                            }
                        ]
                    }
                ]
            }
        ]
    }

    headers = {'Content-Type': 'application/json'}
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info(f"Survey sent to {recip} ({contact_name})")
        return response
    except Exception as e:
        logging.error(f"Failed to send survey to {recip}: {e}")
        return None

def main():
    contact_list = ["email@address1.com", "email@address2.com"]

    with requests.sessions.Session() as session:
        session.auth = (os.getenv("USERNAME"), os.getenv("PASSWORD"))

        for contact_email in contact_list:
            logging.info(f"Processing contact: {contact_email}")
            contact_data = get_contact(contact_email, session)

            if contact_data is None:
                # TODO: Create contact if needed
                logging.warning(f"Contact not found: {contact_email} Creation logic not implemented.")
                continue
            else:
                first_name = contact_data.get("first_name", "")
                last_name = contact_data.get("last_name", "")
                contact_name = f"{first_name} {last_name}".strip()

                response = send_survey(contact_email, contact_name, html_content, session)
                if response and response.status_code == 200:
                    logging.info(f"Successfully sent survey to {contact_email}")
                else:
                    logging.error(f"Survey failed for {contact_email}")

if __name__ == "__main__":
    main()
