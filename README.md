## Telegram Link Sanitizer 1.0

### Overview
I got tired of the tracking params that companies have begin adding to links. I wrote this scrappy script to take care of the issue on Telegram.

### Requirements
- Python 3.x
- pip
- pipreqs
- Telegram API key from `@BotFather`

You will want to use venv as well.

### Usage
1. Setup the config.json file by adding the appropriate offset and chat group IDs, you can have as many groups as you like.
2. Add your Telegram token from `@BotFather` to the Python file
3. Make sure you have Python3, pip, pipreqs installed
4. Install the required dependencies via `pip install -r requirements.txt`
5. Run the thing: `python3 telegram_link_sanitizer.py`
