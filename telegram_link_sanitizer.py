import requests
import re
import json
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = '<YOUR_TOKEN_HERE>'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
CONFIG_FILE = 'config.json'

# Regex pattern for URL modification
URL_PATTERN = re.compile(r'(?:\?|\&)(?:igsh=|si=|t=)[a-z0-9_-]+', re.IGNORECASE)
URL_PATTERN_2 = re.compile(r'(https?://[^\s]+)', re.IGNORECASE)

def load_offset_and_groups():
    offset = 0
    groups = []

    if not os.path.exists(CONFIG_FILE):
        logging.error(f"Config file {CONFIG_FILE} not found.")
        exit(1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)

            if 'offset' in data:
                try:
                    offset = int(data['offset'])
                except (ValueError, TypeError):
                    logging.warning(f"Invalid offset value: {data['offset']}, defaulting to 0.")

            if 'groups' in data:
                if isinstance(data['groups'], list):
                    groups = data['groups']
                else:
                    logging.error(f"Invalid groups format: {data['groups']}, no default applied.")
                    exit(1)

    except Exception as e:
        logging.error(f"Exception while loading offsets and groups: {e}")

    return offset, groups

def save_offset_and_groups(offset, groups):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'offset': offset, 'groups': groups}, f, indent=4)
    except Exception as e:
        logging.error(f"Exception while saving offsets and groups: {e}")

def get_updates(offset, group):
    logging.info(f"Checking [{group}] for new messages at offset {offset}")
    try:
        params = {'timeout': 3000, 'offset': offset}
        response = requests.get(f'{BASE_URL}/getUpdates', params=params)
    except Exception as e:
        logging.error(f"Error getting updates: {e}")
        pass

    return response.json()

def send_message(chat_id, text, reply_to_message_id):
    logging.info(f"Responding to message " + str(reply_to_message_id))
    try:
        params = {
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id
        }
        requests.get(f'{BASE_URL}/sendMessage', params=params)
    except Exception as e:
        logging.error(f"Error responding to message {reply_to_message_id}: {e}")
        pass

def process_updates():
    logging.info("Running ...")

    try:
        while True:
            offset, groups = load_offset_and_groups()
            for group in groups:
                updates = get_updates(offset, group)
                for update in updates.get('result', []):
                    message = update.get('message', {})
                    chat_id = message.get('chat', {}).get('id')
                    chat_title = message.get('chat', {}).get('title')
                    og_user = message.get('from', {}).get('username')
                    
                    if str(chat_id) not in groups:
                        continue

                    logging.info(f"Checking group [{group}] {chat_title}, offset: [{offset}]")
                    offset = update['update_id'] + 1
                    text = message.get('text', '')
                    updated_text = URL_PATTERN.sub('', text)

                    if updated_text != text:
                        logging.info("Found updated text")
                        logging.info("Reformatting message")
                        match = URL_PATTERN_2.search(updated_text)
                        new_message = "hey, " + og_user + ", lmftfy: " + match.group(1) if match else None
                        send_message(chat_id, new_message, message['message_id'])

                    logging.info(f"Updating offset to {offset}")

            save_offset_and_groups(offset, groups)
            time.sleep(3)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        pass

if __name__ == '__main__':
    logging.info("Telegram Link Sanitizer 1.0")
    process_updates()
