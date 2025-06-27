import requests
import re
import csv
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = 'TELEGRAM_API_TOKEN_HERE'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
OFFSET_FILE = 'offsets.csv'

# Regex patterns for URL and message modification
URL_PATTERN = re.compile(r'(?:\?igsh=|\?si=|\?t=|\&igsh=|\&si=|\&t=)[a-z0-9_-]+', re.IGNORECASE)
URL_PATTERN_2 = re.compile(r'(https?://[^\s]+)')

def load_offsets():
    logging.info("Loading offsets")
    offsets = {}
    try:
        if os.path.exists(OFFSET_FILE):
            with open(OFFSET_FILE, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    chat_id, offset = row
                    offsets[chat_id] = offset
    except Exception as e:
        logging.info("Error loading offsets: " + str(e))
    return offsets

def save_offsets(offsets):
    logging.info("Saving offsets " + str(offsets))
    try:
        with open(OFFSET_FILE, 'w') as f:
            writer = csv.writer(f)
            for chat_id, offset in offsets.items():
                writer.writerow([chat_id, offset])
    except Exception as e:
        logging.info("Error saving offsets: " + str(e))

def get_updates(offset=None):
    logging.info("Checking for new messages at offset " + str(offset))
    try:
        params = {'timeout': 5000, 'offset': offset}
        response = requests.get(f'{BASE_URL}/getUpdates', params=params)
    except Exception as e:
        logging.info("Error getting updates: " + str(e))

    return response.json()

def send_message(chat_id, text, reply_to_message_id):
    logging.info("Responding to message " + str(reply_to_message_id))
    try:
        params = {
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id
        }
        requests.get(f'{BASE_URL}/sendMessage', params=params)
    except Exception as e:
        logging.info("Error responding to message " + str(reply_to_message_id) + ": " + str(e))

def process_updates():
    logging.info("Running ...")

    try:
        while True:
            offsets = load_offsets()
            for entry in offsets:
                offset = offsets[entry]
                updates = get_updates(offset)
                for update in updates.get('result', []):
                    message = update.get('message', {})
                    chat_id = message.get('chat', {}).get('id')
                    offset = update['update_id'] + 1
    
                    text = message.get('text', '')
                    updated_text = URL_PATTERN.sub('', text)

                    match = URL_PATTERN_2.search(updated_text)
                    new_message = "Let me fix that for you: " + match.group(1) if match else None
    
                    if updated_text != text:
                        logging.info("Found updated text")
                        send_message(chat_id, new_message, message['message_id'])

                    logging.info("Updating offset to " + str(offset))
                    offsets[entry] = offset

            save_offsets(offsets)
            # Sleep whatever arbitrary time tbh, should probably be event-driven rather than polling
            time.sleep(5)
    except Exception as e:
        logging.info("Error in main execution: " + str(e))

if __name__ == '__main__':
    logging.info("Telegram Link Sanitizer 1.0")
    process_updates()
