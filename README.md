## Telegram Link Sanitizer 1.0

### Overview
I got tired of the tracking params that companies have begin adding to links. I wrote this scrappy script to take care of the issue on Telegram. It's not optimized, lacks some input validation and error correction, but it works well enough, addressing my pet peeve.

### Requirements
- Python 3.x
- pip
- pipreqs
- Telegram API key from `@BotFather`

You will want to use venv as well.

### Usage
1. Update the offsets.csv file by removing the placeholder text and adding the group chat ID and the latest message offset (`chatid,offset`). You can have as many groups and offsets as you like.
2. Add your Telegram token from `@BotFather` to the Python file
3. Make sure you have Python3, pip, pipreqs installed
4. Install the required dependencies via `pip install -r requirements.txt`
5. Run the thing: `python3 telegram_link_sanitizer.py`
